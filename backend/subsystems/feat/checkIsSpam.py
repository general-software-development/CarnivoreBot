import os
import importlib
import shutil
import pathlib
from ..core.logManager import getLogger
from ..core import runtimeDataManager as RDM
from html import unescape

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = '1'

import torch
from torch import nn
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "BossBoss2021/spam-detection-ai"

def attempt_import(module_name):
    logger = getLogger("checkIsSpamInit")
    try:
        logger.debug(f"Importing {module_name}...")
        return importlib.import_module("torch")
    except ImportError as e:
        logger.error(e)

async def load_model():
    RDM.configSubsystem("feat:checkIsSpam:downloaded", maxSize = 4194304)

    if ai := await RDM.readData("feat:checkIsSpam:downloaded", "classifier"):
        if tkn := await RDM.readData("feat:checkIsSpam:downloaded", "tokenizer"):
            return ai, tkn

    logger = getLogger("checkIsSpam")
    logger.info(f"Downloading model: {model_name}")

    class Model(nn.Module):
        def __init__(self, vocab_dim, d_model=34, num_classes=2, num_cls_tokens=4):
            ...

        def forward(self, x):
            ...

    # The MLA and Model class definitions above are only for autocompletion and linting.
    # Below this comment is the code snippet that downloads the up-to-date class definitions from HF,
    # as well as the model
    utils_path = hf_hub_download(
        repo_id=model_name,
        filename="utils.py",
        local_dir=".",
        local_dir_use_symlinks=False,
    )
    shutil.move(utils_path, os.path.abspath(pathlib.Path(__file__).parent / "temp_utils.py"))
    _utils = importlib.import_module(".temp_utils", package="subsystems.feat")
    os.remove(os.path.abspath(pathlib.Path(__file__).parent / "temp_utils.py"))
    # Override class definitions with up-to-date classes to avoid future size missmatches.
    MLA = _utils.MLA
    Model = _utils.Model

    model_path = hf_hub_download(
        repo_id=model_name,
        filename="model.pth"
    )
    tokenizer = AutoTokenizer.from_pretrained(_utils.tokenizer)
    tokenizer.pad_token = tokenizer.eos_token

    ai_model = Model(len(tokenizer))
    ai_model.load_state_dict(torch.load(model_path))
    os.remove(model_path)

    MODEL = ai_model.to(get_device()).eval()
    quantize_dynamic = torch.quantization.quantize_dynamic
    if get_device() == "cpu":
        logger.warning(f"Running model on the CPU. This may have degraded performance. Applying int8 quantization..")
        MODEL = quantize_dynamic(MODEL, {torch.nn.Linear}, dtype=torch.qint8)
    else:
        logger.info(f"Running model on the GPU in float16.")
        MODEL = MODEL.to(dtype=torch.float16)

    await RDM.writeData("feat:checkIsSpam:downloaded", "classifier", MODEL)
    await RDM.writeData("feat:checkIsSpam:downloaded", "tokenizer", tokenizer)

    logger.success(f"Downloaded and loaded model {model_name}")

    return MODEL, tokenizer

from ..abstract.feature import CommandABC
from ..core import dcClient
from ..core import rateLimitManager
from ..core.featManager import detachAsync, queuedFunctionAsync, start_feat
import discord
import asyncio

class CheckIsSpamCommand(CommandABC):
    def __init__(self):
        dcClient.registerCommand("is_spam", self.onRunCommand)

    async def init(self):
        await rateLimitManager.createRateLimit("is_spam")
        detachAsync(self.onRunCommand.runForever())

    @queuedFunctionAsync()
    async def onRunCommand(self, message: discord.Message):
        model, tokenizer = await asyncio.to_thread(lambda: asyncio.run(load_model()))
        text = unescape(message.content)
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)["input_ids"].to(get_device())
        with torch.no_grad():
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=-1)
            spam_score = probs[0][1].item()  # assuming label 1 = spam

        isSpam = spam_score >= 0.00125

        if isSpam:
            await dcClient.runDiscord(message.reply(f"SPAM (score={round(spam_score * 100, 2)}%)"))
        else:
            await dcClient.runDiscord(message.reply(f"NOT SPAM (score={round(spam_score * 100, 2)}%)"))

def InitialiseCheckIsSpamCommand():
    start_feat("CheckIsSpam", CheckIsSpamCommand)
            