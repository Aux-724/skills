# skills

Personal collection of agent skills for daily workflows.

个人日常使用的 agent skills 集合。三个技能分别来自上游仓库，按原许可证保留。

## Included skills

| Folder | Purpose | Upstream |
| --- | --- | --- |
| [`scientific-figure-making/`](scientific-figure-making/SKILL.md) | Publication-ready matplotlib figures (bars, trends, heatmaps, multi-panel layouts) with the figures4papers house style. | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) |
| [`design-taste-frontend/`](design-taste-frontend/SKILL.md) | Anti-slop frontend skill for landing pages, portfolios, and redesigns. This is the taste-skill v2 default (`design-taste-frontend`). | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) |
| [`ppt-master/`](ppt-master/SKILL.md) | Workflow for editable PowerPoint decks: generate, beautify, template, and narrate PPTX files. | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) |

Licenses differ. See [ATTRIBUTION.md](ATTRIBUTION.md). `scientific-figure-making` is **CC BY-NC 4.0** (non-commercial). The other two skills are MIT, with extra notices for icons, sounds, and optional PyMuPDF.

## Use

### Path

Clone this repo and point your agent at a skill file, for example `scientific-figure-making/SKILL.md`. Demo figure scripts are not in this repo; [`scientific-figure-making/references/demos.md`](scientific-figure-making/references/demos.md) links to the upstream `figure_*` folders.

Or symlink a skill into the agent skills directory:

```bash
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/scientific-figure-making" ~/.cursor/skills/scientific-figure-making
ln -s "$(pwd)/design-taste-frontend" ~/.cursor/skills/design-taste-frontend
ln -s "$(pwd)/ppt-master" ~/.cursor/skills/ppt-master
```

Claude Code and Codex use `~/.claude/skills` and `~/.codex/skills` the same way.

### `npx skills add`

The [skills CLI](https://github.com/vercel-labs/skills) discovers each top-level `SKILL.md`. Install names are the frontmatter `name` values, which match the folder names.

```bash
npx skills add https://github.com/Aux-724/skills
npx skills add https://github.com/Aux-724/skills --skill scientific-figure-making
npx skills add https://github.com/Aux-724/skills --skill design-taste-frontend
npx skills add https://github.com/Aux-724/skills --skill ppt-master
```

## ppt-master

The package is the upstream `skills/ppt-master/` tree: `SKILL.md`, `workflows/`, `scripts/`, `references/`, and `templates/`. It is about **121 MB** and **13,000 files**, mostly SVG icon sets, interface WAV files, and style-comparison PNGs. No single file is over GitHub's 100 MB limit.

From this checkout:

```bash
python3 skills/ppt-master/scripts/project_manager.py init my_deck
pip install -r requirements.txt   # optional; see ppt-master/requirements.txt
```

`skills/ppt-master` points at `ppt-master/`, so those upstream-relative commands work here. Generated decks go in `projects/` (gitignored except `projects/README.md`). Set `SKILL_DIR` to the absolute `ppt-master` directory when an agent follows `SKILL.md`. Do not remove `LICENSE`, `SPONSORS.md`, or `SPONSORS_CN.md`; the skill stops if its attribution check fails.

`python3 ppt-master/scripts/update_repo.py` fast-forwards **this** repository. Most scripts use the Python standard library. Image, audio, and document converters need the packages listed in `ppt-master/requirements.txt`. PDF conversion uses PyMuPDF (AGPL-3.0) and is optional.
