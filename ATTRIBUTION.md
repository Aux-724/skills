# Attribution

This collection vendors copies of upstream skill packages for personal and workflow use. It does not claim authorship of those skills. Each package stays under the upstream license named below. Copyright remains with the upstream authors.

Collection-only files are `README.md`, `ATTRIBUTION.md`, `.gitignore`, the `skills/ppt-master` symlink, the checkout-root notes in `requirements.txt`, and `ppt-master/scripts/repo_layout.py` plus the small root-resolution edits that call it. Copies were taken on 2026-09-24 from the commits below. No upstream release tag was current for these snapshots; the commit is the pin.

## scientific-figure-making

- Upstream: https://github.com/ChenLiu-1996/figures4papers
- Upstream path: `scientific-figure-making/`
- Commit: [`3c181f85e82c6f24948fcaaf3be6696102b41d8d`](https://github.com/ChenLiu-1996/figures4papers/commit/3c181f85e82c6f24948fcaaf3be6696102b41d8d) (2026-09-06, "Create LICENSE")
- License: Creative Commons Attribution-NonCommercial 4.0 International. Full text: [`scientific-figure-making/LICENSE`](scientific-figure-making/LICENSE). Deed: https://creativecommons.org/licenses/by-nc/4.0/
- Owner: Chen Liu ([ChenLiu-1996](https://github.com/ChenLiu-1996))
- What was copied: `SKILL.md` and `references/` only. Demo scripts and figure assets stay in the upstream repository. [`references/demos.md`](scientific-figure-making/references/demos.md) links to those `figure_*` folders by URL.
- NonCommercial: sharing and adaptation are for non-commercial use, with attribution. Commercial use needs permission from the licensor.

## design-taste-frontend

- Upstream: https://github.com/Leonxlnx/taste-skill
- Upstream path: `skills/taste-skill/` (the v2 default skill; its frontmatter `name` is `design-taste-frontend`). The v1 skill was not copied.
- Commit: [`c184364c58658b2f131b4ae8bd3d206cabb3deee`](https://github.com/Leonxlnx/taste-skill/commit/c184364c58658b2f131b4ae8bd3d206cabb3deee) (2026-09-23)
- License: MIT License. Copyright (c) 2026 Leonxlnx. Full text: [`design-taste-frontend/LICENSE`](design-taste-frontend/LICENSE)
- Owner: Leonxlnx ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill))
- What was copied: `SKILL.md`, which is the entire upstream skill folder, plus the repository `LICENSE`.

## ppt-master

- Upstream: https://github.com/hugohe3/ppt-master
- Upstream path: `skills/ppt-master/`
- Commit: [`481e057ecd9f5ff094c9c789b17b2d1331e278e8`](https://github.com/hugohe3/ppt-master/commit/481e057ecd9f5ff094c9c789b17b2d1331e278e8) (2026-09-23)
- License: MIT License. Copyright (c) 2025-2026 Hugo He. Full text: [`ppt-master/LICENSE`](ppt-master/LICENSE). The skill's integrity check requires this file, `SPONSORS.md`, and `SPONSORS_CN.md` to stay unmodified.
- Owner: Hugo He ([hugohe3/ppt-master](https://github.com/hugohe3/ppt-master))
- Third-party assets shipped inside the skill package:
  - Icons: [`ppt-master/templates/icons/THIRD_PARTY_NOTICES.md`](ppt-master/templates/icons/THIRD_PARTY_NOTICES.md) (Tabler Icons, Phosphor, Simple Icons, CHUNK Icons, and others)
  - Sounds: [`ppt-master/templates/sounds/THIRD_PARTY_NOTICES.md`](ppt-master/templates/sounds/THIRD_PARTY_NOTICES.md)
- Optional PDF conversion imports PyMuPDF (AGPL-3.0). It is not vendored here. See the note in [`ppt-master/requirements.txt`](ppt-master/requirements.txt).

## lab-cluster-1

- Upstream: https://github.com/black-yt/skills
- Source URL: https://github.com/black-yt/skills/tree/main/lab-cluster-1
- Upstream path: `lab-cluster-1/`
- Commit: [`dbf510f2105da21561e8e114a963a6e36885cd46`](https://github.com/black-yt/skills/commit/dbf510f2105da21561e8e114a963a6e36885cd46) (2026-09-22, "Add LaTeX migration project startup instructions")
- License: none. The upstream repository has no `LICENSE`, `NOTICE`, or `COPYING` file, no SPDX header in this skill, and the GitHub repository license field is empty. This collection does not add a license of its own. Copyright stays with the upstream author. Redistribution and reuse are not granted by a license text from that project.
- Owner: [black-yt](https://github.com/black-yt). The upstream README describes the repository as skills maintained by 徐望瀚 for daily work.
- What was copied: the entire `lab-cluster-1/` folder (`SKILL.md`, `references/`, and `scripts/hf_cache_to_model_dir.py`). No other skills from that repository were copied.

### Layout adaptation

Upstream Python treats the skill as `<repo>/skills/ppt-master` and sets the checkout root two directories above the skill (`projects/`, root `requirements.txt`, `git pull`). In this collection the package lives at `ppt-master/`.

These files now call `scripts/repo_layout.py` so both layouts resolve:

- `scripts/project_management/paths.py`
- `scripts/config.py`
- `scripts/update_repo.py`
- `scripts/apply_template.py`

`skills/ppt-master` is a symlink to `../ppt-master`, so upstream-relative commands (`python3 skills/ppt-master/scripts/...`) and the root requirements include still work. Each `SKILL.md` keeps its upstream frontmatter; a one-line source note sits under that frontmatter and does not replace the upstream metadata. When the skill is installed into a directory named `skills` (the usual `npx skills add` location), root detection matches upstream.
