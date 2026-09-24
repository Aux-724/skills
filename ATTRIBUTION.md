# Attribution

This repository is a personal collection of third-party agent skills. Each skill is copied from its upstream project and remains under that project's license. Nothing in this collection changes upstream copyright. The files added here (`README.md`, `ATTRIBUTION.md`, `.gitignore`, the `skills/ppt-master` symlink, and the checkout-root notes in `requirements.txt`) are collection glue.

Pinned upstream commits (shallow copies made on 2026-09-24):

| Skill folder | Upstream | Commit | License |
| --- | --- | --- | --- |
| `scientific-figure-making/` | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) | [`3c181f85`](https://github.com/ChenLiu-1996/figures4papers/commit/3c181f85e82c6f24948fcaaf3be6696102b41d8d) | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| `design-taste-frontend/` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) `skills/taste-skill/` | [`c184364c`](https://github.com/Leonxlnx/taste-skill/commit/c184364c58658b2f131b4ae8bd3d206cabb3deee) | MIT |
| `ppt-master/` | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) `skills/ppt-master/` | [`481e057e`](https://github.com/hugohe3/ppt-master/commit/481e057ecd9f5ff094c9c789b17b2d1331e278e8) | MIT, plus third-party asset notices |

## scientific-figure-making

- Author: Chen Liu ([ChenLiu-1996](https://github.com/ChenLiu-1996))
- Source folder: `scientific-figure-making/` in [figures4papers](https://github.com/ChenLiu-1996/figures4papers)
- License text: [`scientific-figure-making/LICENSE`](scientific-figure-making/LICENSE) (Creative Commons Attribution-NonCommercial 4.0 International)
- What was copied: `SKILL.md` and `references/` only. Demo scripts and figure assets stay in the upstream repository. [`references/demos.md`](scientific-figure-making/references/demos.md) links to those `figure_*` folders by URL.
- NonCommercial: this skill may be shared and adapted for non-commercial use with attribution. Commercial use needs permission from the licensor.

## design-taste-frontend

- Author: Leonxlnx ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)), copyright 2026
- Source folder: `skills/taste-skill/` (install name `design-taste-frontend`, the current v2 default). The v1 skill was not copied.
- License text: [`design-taste-frontend/LICENSE`](design-taste-frontend/LICENSE) (MIT)
- What was copied: `SKILL.md`, which is the entire upstream skill folder, plus the repository `LICENSE`.

## ppt-master

- Author: Hugo He ([hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)), copyright 2025–2026
- Source folder: `skills/ppt-master/`
- License text: [`ppt-master/LICENSE`](ppt-master/LICENSE) (MIT). The skill's integrity check requires this file, `SPONSORS.md`, and `SPONSORS_CN.md` to stay unmodified.
- Third-party assets shipped inside the skill package:
  - Icons: [`ppt-master/templates/icons/THIRD_PARTY_NOTICES.md`](ppt-master/templates/icons/THIRD_PARTY_NOTICES.md) (Tabler Icons, Phosphor, Simple Icons, CHUNK Icons, and others)
  - Sounds: [`ppt-master/templates/sounds/THIRD_PARTY_NOTICES.md`](ppt-master/templates/sounds/THIRD_PARTY_NOTICES.md)
- Optional PDF conversion imports PyMuPDF (AGPL-3.0). It is not vendored here. See the note in [`ppt-master/requirements.txt`](ppt-master/requirements.txt).

### Layout adaptation

Upstream Python treats the skill as `<repo>/skills/ppt-master` and sets the checkout root two directories above the skill (`projects/`, root `requirements.txt`, `git pull`). In this collection the package lives at `ppt-master/`.

These files now call `scripts/repo_layout.py` so both layouts resolve:

- `scripts/project_management/paths.py`
- `scripts/config.py`
- `scripts/update_repo.py`
- `scripts/apply_template.py`

`skills/ppt-master` is a symlink to `../ppt-master`, so upstream-relative commands (`python3 skills/ppt-master/scripts/...`) and the root requirements include still work. `SKILL.md` is unchanged. When the skill is installed into a directory named `skills` (the usual `npx skills add` location), root detection matches upstream.
