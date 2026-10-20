# [Project title]

> **Starting from the AISS template?** Do these four things, then delete this box.
>
> 1. Click **Use this template** → **Create a new repository**. Make it **Private**.
> 2. Clone it, then copy `.env.example` to `.env` and fill in your data folder, Stata path and API keys.
> 3. Run `uv sync` to install the Python environment ([install uv](https://docs.astral.sh/uv/getting-started/installation/) first if needed).
> 4. Run `uv run python run.py`. It checks your setup and tells you what is missing.
>
> Then fill in the sections below and the *Project specifics* part of `AGENTS.md`.

## Question

[Two sentences: what this project wants to learn, and why it matters.]

## How to run

```bash
uv sync                    # same Python packages, same versions, on any machine
uv run python run.py       # every script, in order: raw data in, tables and figures out
```

`run.py` lists every script in the order it runs, Python and Stata alike. Stata scripts need `STATA_PATH` in `.env`.
To run part of the pipeline: `uv run python run.py build` runs only the steps whose path contains "build".

## Data

Data never goes into Git. It lives on lab storage, and each machine sets its location as `DATA_DIR` in `.env`.
Every source is documented in [`data/README.md`](data/README.md): origin, date, who downloaded it, licence.

## Structure

```
README.md        what the project is and how to run it
AGENTS.md        standing instructions for AI coding agents (CLAUDE.md points to it)
run.py           the single entry point
pyproject.toml   Python packages requested    ─┐ changed only
uv.lock          exact versions installed      ─┘ through uv
.env.example     secrets and machine paths the project needs, without values

data/            ignored by Git, except data/README.md
  raw/           as received: never edited, never overwritten
  llm_cache/     prompts and raw model responses: written once, never deleted
  interim/       working files, rebuildable
  clean/         analysis-ready, rebuildable; the only data analysis reads

code/
  00_setup.do    Stata settings; every do-file runs it first
  01_build/      raw → clean (no estimation)
  02_analysis/   clean → output (reads only data/clean)
  lib/           shared Python functions, including paths.py
  ado/           project-local Stata packages, committed

output/          written by code only, never by hand
  tables/        tracked: a changed number shows up in the pull request
  figures/       tracked
  logs/          ignored

docs/
  log/           research log, one file per person, newest entry on top
  updates/       weekly update to the PI, one file per week

paper/           draft and slides; tables and figures come from output/
scratch/         your sandbox, ignored; nothing may depend on it
```

## Team

| Role | Name |
|:--|:--|
| PI | [name] |
| RA | [name] |

---
<sub>Built from the [AISS research template](https://github.com/aiss-unibocconi-eu/research-template) · AI in Social Sciences Lab, Bocconi University</sub>
