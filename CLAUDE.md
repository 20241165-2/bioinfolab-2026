# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A student's coursework repository for a bioinformatics lab course (생물정보학실험), run in GitHub Codespaces. It is not a software project: there is no build system, package manifest, test suite, or linter. Each `labNN/` folder is one week's exercises. All prose, comments, commit messages, and output strings are in Korean — keep new material in Korean to match.

## Layout conventions

- New weekly folders are created by copying the template: `cp -r lab-template labNN`. Each lab has:
  - `data/` — downloaded or generated input data (FASTA etc.)
  - `doc/` — reports, result summaries (`.md`, `.tsv`), figures
  - `src/` — the student's own `.sh` / `.py` scripts
- `resources/` holds shared practice data (`resources/data/*.txt`) and example scripts from the instructor.
- Sequencing data (`*.fastq`, `*.fq*`, `*.sra`) and assembler/annotation output dirs (shovill, spades, prokka, flye, FastQC reports) are gitignored on purpose — they are re-downloaded with `wget` when needed, never committed.
- Scripts within a week often have numbered successors (`countseq.py` → `countseq2.py`, `bug1.sh`…`bug3.sh` debugging exercises) and earlier weeks' scripts get re-implemented in later weeks (e.g. shell in lab05 → Python in lab06 → module-based in lab07). Don't "fix" or consolidate older lab folders; they are a record of the course progression.

## Running scripts

Scripts are run directly from the lab's `src/` folder with plain `python3`/`bash`, taking paths via `sys.argv` / `$1`:

```
cd lab07/src
python3 fasta.py ../data/seqs.fasta          # module self-test (prints len/GC, asserts reverse_complement)
python3 summary.py ../data/seqs.fasta ../doc/summary.tsv
python3 batchinfo.py ../data ../doc/batchinfo.tsv
```

Scripts in lab07 do `from fasta import ...`, so they must be run with `lab07/src` as the current directory (or with it on `PYTHONPATH`). `lab07/src/README.md` lists the functions in the `fasta.py` module (`read_fasta`, `gc_content`, `write_fasta`, `reverse_complement`, `length_stats`).

`lab*/src/check_codespace.sh` and `.devcontainer/check.sh` just report which tools are installed.

## Environment

Four devcontainer configs in `.devcontainer/` (chosen per week when creating the Codespace): `1-basic` (Python + Linux basics, weeks 2–7), `2-conda` (micromamba only), `3-seq` (seqkit, blast, mafft, iqtree, fastqc, fastp), `4-genome` (+ shovill, prokka). `$MYHOME` is set to the workspace root, and a bare `cd` returns there. Per the README, students should not install missing tools themselves (except during the conda week) — report them to the instructor instead.

## Code style

Match the course's beginner-level idiom: simple top-level scripts using `sys.argv`, explicit loops, string concatenation or f-strings, short Korean docstrings. Avoid introducing argparse, classes, third-party libraries, or other abstractions the exercises haven't covered unless asked.
