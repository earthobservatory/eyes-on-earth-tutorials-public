# Contributing — for instructors and TAs

This describes how to add tutorials 1, 3 and 4 so the whole course looks like one thing rather than four.

[Tutorial 2](2.0_Tutorial_2_Overview_and_Assignment/) is the worked example. When in doubt, copy what it does.

## Folder naming

```
<tutorial>.<topic>_Descriptive_Name_With_Underscores/
```

- The first digit is the tutorial number, the second is the topic within it.
- `X.0` is always the **overview and assignment** — the handout, the figures, the questions. No notebook.
- `X.1`, `X.2`, … are the individual **topic modules**, one notebook each.
- Supplementary material that does not belong to a specific tutorial gets an `S##_` prefix and sorts to the end.

Numbering rather than "week 3" means you can insert `S02_Something` later without renumbering the course.

Notebooks inside a module are named `<tutorial>.<topic>.<n>_Title.ipynb` — e.g. `2.1.1_PACE_OCI_Chlorophyll_a.ipynb`. A module usually has one, but can have several.

## What goes in a module folder

Everything that module needs, and nothing else:

```
2.1_Ocean_Colour_with_PACE_OCI/
├── README.md                          always
├── 2.1.1_PACE_OCI_Chlorophyll_a.ipynb the notebook
├── data/                              inputs and outputs — gitignored
├── Figs/                              images used by the notebook or README
└── utils.py                           module-local helpers, only if genuinely needed
```

Modules are **self-contained**. There is no shared `src/` package. If two modules need the same 20-line helper, copy it — a student opening one notebook should not have to understand the repository layout to make it run.

## Every tutorial notebook starts with the same setup cell

Copy it verbatim from an existing tutorial notebook. **Change nothing** except the `DATA_DIR` line at the bottom, which names the subfolder your data goes in.

The cell checks what can be imported and installs only what is missing. It has no platform branching, no repository clone, and no path configuration. In a Codespace or a local conda env nothing is missing, so it prints one line and does nothing — it is there as a safety net for the gap between adding a dependency and rebuilding the image.

`0.1_Setup_and_Environment/0.1.1_Setup_and_Check.ipynb` is the one exception. Its setup cell parses the package list out of `environment.yml`, and a separate repair cell fixes any gap with `conda env update --prefix $(sys.prefix)` against the same file. Conda, not pip: that notebook is the one place that repairs a whole environment rather than topping up one package, and a pip wheel over conda's GEOS/PROJ/GDAL is how you turn a missing package into an unreadable crash. Do not copy either cell into a tutorial notebook — they depend on `environment.yml` being a sibling file.

`os.getcwd()` is the notebook's own folder, so `os.getcwd()/data/` is the module's `data/` folder. Do not reintroduce a `REPO_ROOT` or a platform branch for paths — it is not needed and it drifts.

**New package needed?** Two places, and they must stay in sync:

1. `0.1_Setup_and_Environment/environment.yml` — the environment, for both Codespaces and local conda
2. The `REQUIRED` dict in each tutorial notebook's setup cell that imports it

`0.1.1` needs no edit; it reads the list from `environment.yml`. If the package's conda name differs from its import name, add that one pair to `IMPORT_NAME` in its setup cell.

## The Codespaces badge lives in the root README only

```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/earthobservatory/eyes-on-earth-tutorials)
```

The badge points at the **repository**, not at a notebook, because a codespace opens the whole thing — so one badge in the root [README.md](README.md) is all it can usefully say. Do not add it to notebooks or module READMEs; a copy per module is six more places to leave a `YOUR-ORG` placeholder in.

Do add a row for the new module to the table in the root [README.md](README.md).

## The devcontainer

[`.devcontainer/`](.devcontainer/) builds the Codespaces image from `environment.yml`, so there is one environment definition rather than two. It also pre-downloads Cartopy's Natural Earth coastlines, which otherwise means a network call on the first plot of every notebook.

Building the env in the `Dockerfile` rather than `postCreateCommand` is deliberate — it lets Codespaces **prebuild** the image so students start in seconds. If you move it, you lose that.

**Turn prebuilds on** before the course: *Settings → Codespaces → Set up prebuild*. Without them the first launch runs the full conda solve.

## Notebook structure

Follow the shape of `2.1.1`:

1. **Title cell** — what you will do, what you need first, links to the accounts required.
2. **Setup cell** — the standard one.
3. **About the data** — the mission, the product, links, and any gotchas (units, grid extent, ordering).
4. **Get the data** — automated first, manual fallback second. `earthaccess`/`ftplib` keeps the download reproducible and scriptable, and does not depend on a student clicking through a portal correctly.
5. **Inspect** — open the file and print its metadata before any analysis, so students see what is actually in it.
6. **Analyse and plot.**
7. **Export** — GeoTIFF for QGIS, or saved figures.
8. **Questions to answer** — as a markdown cell at the end, matching the handout.

Cross-link to the next notebook at the bottom.

## Things worth being consistent about

**Credentials.** Tutorial notebooks must never prompt for, or hard-code, a username or password. They read `~/.netrc`, which [0.2.1](0.2_Data_Access_Accounts/0.2.1_Account_Check.ipynb) writes once — `earthaccess.login(strategy="netrc")` for NASA, `netrc.netrc().authenticators(host)` for anything using `ftplib`.

Always name the strategy. The default, `strategy="all"`, silently falls back to an interactive prompt, and in VS Code that prompt is off-screen enough that the cell reads as hung.

0.2.1 is the one exception: it writes the file, so real passwords are typed into its cells. Its last section restores the placeholders and clears the outputs, and it must stay that way.

**Data files.** Anything under `data/` is gitignored. Do not commit NetCDF, GeoTIFF or HDF5 files. For instructor-provided data, host it on Drive or as a release attachment and add the URL to the notebook.

**Large binaries.** Handout `.docx`/`.pdf` files are gitignored — their text belongs in the module README and their figures should be extracted into `Figs/` at a sensible size. A screenshot for documentation does not need to be 4400px wide.

**Colour scales.** When students compare across time periods, fix `vmin`/`vmax` across every plot. A per-plot autoscale makes the comparison meaningless, and this is the single most common way a tutorial silently teaches the wrong thing.

**Coordinate slicing.** Use `sel()` with coordinate values, not `isel()` with array indices. And check whether latitude ascends or descends before writing a slice — getting it backwards returns an empty array rather than an error.

**British spelling** in prose, to match the rest of the course material ("colour", "visualise").

## Before a session

- [ ] Run every notebook top to bottom in a **fresh** Codespace, with a restarted kernel. A stale kernel hides both missing packages and stale variables.
- [ ] Check that the root README badge opens the right thing, and that figures render.
- [ ] Check that any account with slow approval is flagged in the module README **and** in `0.2_Data_Access_Accounts`.
- [ ] Clear all outputs before committing (`jupyter nbconvert --clear-output --inplace *.ipynb`) — output cells bloat diffs and can leak paths or credentials.
- [ ] Confirm instructor-provided data is actually reachable by someone who is not you.
