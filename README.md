# skills

Personal collection of agent skills for daily workflows.

个人日常使用的 agent skills 集合。技能分别来自上游仓库，按原许可证保留；未声明许可证的上游会在下文写明。

## Included skills

This collection copies third-party skill packages. It does not claim authorship. Full owner, path, commit, and license details are in [ATTRIBUTION.md](ATTRIBUTION.md).

### scientific-figure-making

Publication-ready matplotlib figures (bars, trends, heatmaps, multi-panel layouts) with the figures4papers house style.

- Source: https://github.com/ChenLiu-1996/figures4papers (`scientific-figure-making/`)
- License: [CC BY-NC 4.0](scientific-figure-making/LICENSE) (non-commercial)

### design-taste-frontend

Anti-slop frontend skill for landing pages, portfolios, and redesigns. This is the taste-skill v2 default. The install name is `design-taste-frontend`; the upstream folder is `skills/taste-skill/`.

- Source: https://github.com/Leonxlnx/taste-skill (`skills/taste-skill/`)
- License: [MIT](design-taste-frontend/LICENSE)

### ppt-master

Workflow for editable PowerPoint decks: generate, beautify, template, and narrate PPTX files.

- Source: https://github.com/hugohe3/ppt-master (`skills/ppt-master/`)
- License: [MIT](ppt-master/LICENSE), plus icon and sound notices inside the package

### lab-cluster-1

Lab cluster 1 / PJLAB workflow for paths, proxies, model weights, raw `rlaunch`/`rjob` commands, service access, and troubleshooting. **Localized on 2026-09-24 for the ailab-ai4solver project** (same H cluster, different team): the upstream author's account, dev hosts, partitions, namespaces, and paths were replaced with locally verified values, and the SSH-relay workflow was rewritten for agents that run directly on the dev-machine workspace pod. See the localization note at the top of [`lab-cluster-1/SKILL.md`](lab-cluster-1/SKILL.md).

- Source: https://github.com/black-yt/skills/tree/main/lab-cluster-1 (`lab-cluster-1/`), modified as described above
- License: none published. [black-yt/skills](https://github.com/black-yt/skills) has no `LICENSE` file, and GitHub reports no license. The base skill's copyright stays with the upstream author. See [ATTRIBUTION.md](ATTRIBUTION.md).

### nature-polishing

Polish, translate, or tighten existing academic prose while preserving facts, terminology, and evidence boundaries, including manuscript LaTeX layout fixes. Drafting new sections is the upstream `nature-writing` skill, which is not in this collection.

- Source: https://github.com/Yuan1z0825/nature-skills (`skills/nature-polishing/`)
- License: [Apache-2.0](nature-polishing/LICENSE)
- Depends on [`nature-shared/`](nature-shared/) as a sibling. `SKILL.md` and `manifest.yaml` load `../nature-shared/core/...` (and deeper fragments load the same package). Those relative paths are unchanged.

### nature-ref-verifier

Cross-check scholarly references field by field (authors, title, year, volume, issue, pages) and flag conflicts such as volume-year versus DOI-year, author order, and page drift. Works on a full bibliography or a single citation.

- Source: https://github.com/Yuan1z0825/nature-skills (`skills/nature-ref-verifier/`)
- License: [Apache-2.0](nature-ref-verifier/LICENSE)

### nature-shared

Shared dependency used by `nature-polishing` (and by other upstream Nature skills that are not copied here). Not a standalone user-facing skill: [`nature-shared/SKILL.md`](nature-shared/SKILL.md) says to load only the specific `core/` or `journal-formats/` file another Nature skill requests, and not to invoke this package as its own workflow.

- Source: https://github.com/Yuan1z0825/nature-skills (`skills/nature-shared/`)
- License: [Apache-2.0](nature-shared/LICENSE)

## Use

### Path

Clone this repo and point your agent at a skill file, for example `scientific-figure-making/SKILL.md`. Demo figure scripts are not in this repo; [`scientific-figure-making/references/demos.md`](scientific-figure-making/references/demos.md) links to the upstream `figure_*` folders.

Or symlink a skill into the agent skills directory:

```bash
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/scientific-figure-making" ~/.cursor/skills/scientific-figure-making
ln -s "$(pwd)/design-taste-frontend" ~/.cursor/skills/design-taste-frontend
ln -s "$(pwd)/ppt-master" ~/.cursor/skills/ppt-master
ln -s "$(pwd)/lab-cluster-1" ~/.cursor/skills/lab-cluster-1
ln -s "$(pwd)/nature-polishing" ~/.cursor/skills/nature-polishing
ln -s "$(pwd)/nature-ref-verifier" ~/.cursor/skills/nature-ref-verifier
ln -s "$(pwd)/nature-shared" ~/.cursor/skills/nature-shared
```

`nature-shared` should sit beside `nature-polishing`. The polishing skill resolves `../nature-shared/...` from its own directory.

Claude Code and Codex use `~/.claude/skills` and `~/.codex/skills` the same way.

### `npx skills add`

The [skills CLI](https://github.com/vercel-labs/skills) discovers each top-level `SKILL.md`. Install names are the frontmatter `name` values, which match the folder names.

```bash
npx skills add https://github.com/Aux-724/skills
npx skills add https://github.com/Aux-724/skills --skill scientific-figure-making
npx skills add https://github.com/Aux-724/skills --skill design-taste-frontend
npx skills add https://github.com/Aux-724/skills --skill ppt-master
npx skills add https://github.com/Aux-724/skills --skill lab-cluster-1
npx skills add https://github.com/Aux-724/skills --skill nature-polishing
npx skills add https://github.com/Aux-724/skills --skill nature-ref-verifier
npx skills add https://github.com/Aux-724/skills --skill nature-shared
```

`nature-shared` should sit beside `nature-polishing` in the same skills directory so `../nature-shared/...` resolves. It is a shared dependency, not a standalone workflow. `nature-ref-verifier` does not load it.

## ppt-master

The package is the upstream `skills/ppt-master/` tree: `SKILL.md`, `workflows/`, `scripts/`, `references/`, and `templates/`. It is about **121 MB** and **13,000 files**, mostly SVG icon sets, interface WAV files, and style-comparison PNGs. No single file is over GitHub's 100 MB limit.

From this checkout:

```bash
python3 skills/ppt-master/scripts/project_manager.py init my_deck
pip install -r requirements.txt   # optional; see ppt-master/requirements.txt
```

`skills/ppt-master` points at `ppt-master/`, so those upstream-relative commands work here. Generated decks go in `projects/` (gitignored except `projects/README.md`). Set `SKILL_DIR` to the absolute `ppt-master` directory when an agent follows `SKILL.md`. Do not remove `LICENSE`, `SPONSORS.md`, or `SPONSORS_CN.md`; the skill stops if its attribution check fails.

`python3 ppt-master/scripts/update_repo.py` fast-forwards **this** repository. Most scripts use the Python standard library. Image, audio, and document converters need the packages listed in `ppt-master/requirements.txt`. PDF conversion uses PyMuPDF (AGPL-3.0) and is optional.
