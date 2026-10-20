"""Genera workshop.tex a partir de workshop.src.tex.

Los listados de ficheros (pixi.toml, Dockerfile, package.xml...) se escriben en
la fuente entre marcadores:

    %%CODE toml
    [workspace]
    channels = ["conda-forge"]
    %%END

(`%%CODE xml tiny` usa letra más pequeña, para listados anchos en dos columnas.)

Aquí se colorean con pygmentize, para que compilar las slides no necesite
-shell-escape ni minted. Los colores están en pygments-style.tex.

    pixi run slides     # regenera workshop.tex y compila workshop.pdf
"""

import re
import subprocess
from pathlib import Path

here = Path(__file__).parent
source = (here / "workshop.src.tex").read_text(encoding="utf-8")


def colorize(match: re.Match) -> str:
    lexer, size, code = match.group(1), match.group(2), match.group(3)
    latex = subprocess.run(
        ["pygmentize", "-l", lexer, "-f", "latex"],
        input=code,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    font = f"\\{size}\n" if size else ""
    return "\\begin{filelisting}\n" + font + latex.rstrip("\n") + "\n\\end{filelisting}"


output = re.sub(r"^%%CODE (\S+)(?: (\S+))?\n(.*?)^%%END$", colorize, source, flags=re.S | re.M)
header = "% GENERADO por generar.py a partir de workshop.src.tex: edita ese fichero.\n"
(here / "workshop.tex").write_text(header + output, encoding="utf-8")
