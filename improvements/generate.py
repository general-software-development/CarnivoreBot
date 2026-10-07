import yaml
from yaml import CSafeLoader

from pathlib import Path
import argparse

parser = argparse.ArgumentParser("MDG")
parser.add_argument("path")
args = parser.parse_args()
path = Path(args.path)

with open(path, 'r') as f:
    data = f.read()

data: dict[str, dict] = yaml.load(data, CSafeLoader)

out = ""

for cb_id, cb_data in data.items():
    out += f"## {cb_id} ({str(cb_data['status']).capitalize()}) <!-- {cb_data['title']} -->\n\n"
    out += cb_data['date'] + "\n\n"
    out += f"Author: @{cb_data['author']}\n\n"
    out += f"Assigned: @{'@'.join(cb_data['assignees'])}\n\n"
    out += '\n'.join(map(lambda x: str(x) if x is not None else "", cb_data['description'])) if not isinstance(cb_data['description'], str) else cb_data['description']
    out += '\n\n'

print(out)
