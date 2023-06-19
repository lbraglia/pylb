#!/usr/bin/env python3

import argparse
import os
import subprocess

from pathlib import Path

preamble = r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english, italian]{babel}
\usepackage{mypkg}
\usepackage{tikz}
\usetikzlibrary{arrows,snakes,backgrounds,calc}
\usepackage{wrapfig}
\usepackage{subfig}
\usepackage{rotating}
\usepackage{cancel}
\usepackage{hyperref}
\begin{document}
\tableofcontents
"""

outro = r"\end{document}"

def worker(what):
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", type = str, help="path to a tex or a dir")
    args = argparser.parse_args()
    inpath = Path(args.path)
    outfname = inpath.stem
    tmptex = Path("tmp_%s.tex" % outfname)
    tmppdf = Path("tmp_%s.pdf" % outfname)
    finalpdf = Path("%s.pdf" % outfname)
    if not inpath.exists():
        raise FileNotFoundError
    if inpath.is_dir():
        files = [f for f in list(inpath.iterdir()) if f.suffix == '.tex']
    else:
        files = [inpath]
    contents = []
    for tex in sorted(files):
        with tex.open() as f:
            contents.append(f.read())
    content = "\n".join(contents)
    full_content = r"""\documentclass{%s}""" % what + preamble + content + outro
    with tmptex.open("w") as f:
        f.write(full_content)
    # run pdflatex with output in /tmp
    pdflatex_cmd = ["pdflatex", "-output-directory", "/tmp", tmptex]
    subprocess.run(pdflatex_cmd)
    subprocess.run(pdflatex_cmd)
    # cleaning and renaming (removing "tmp_")
    tmptex.unlink()
    subprocess.run(["mv", Path("/tmp")/tmppdf, Path("/tmp")/finalpdf])
    



def article():
    worker("article")

def book():
    worker("book")
    
if __name__ == "__main__":
    book()
