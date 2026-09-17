import os
import subprocess

import pypandoc


def generate_legal_pdfs() -> None:
    output_dir = "public/Assets"
    os.makedirs(output_dir, exist_ok=True)

    pandoc = pypandoc.get_pandoc_path()

    files = (
        "LICENSE.md",
        "PrivacyPolicy.md",
    )

    for source in files:
        output = os.path.join(
            output_dir,
            f"{os.path.splitext(source)[0]}.pdf",
        )

        subprocess.run(
            [
                pandoc,
                source,
                "--from=gfm",
                "--pdf-engine=xelatex",
                "-o",
                output,
            ],
            check=True,
        )


if __name__ == "__main__":
    generate_legal_pdfs()