# 0.1 Setup and Environment

Run this module **once, before your first tutorial**.

Notebook: `0.1.1_Setup_and_Check.ipynb`

It confirms that everything imports, draws a test map, and proves the NetCDF → GeoTIFF chain works. In a Codespace it takes seconds.

## The setup cell

**In `0.1.1`** the setup cell reads the package list straight out of [`environment.yml`](environment.yml), imports each one, and reports. If anything is missing or broken, the repair cell underneath it runs `conda env update` against that same file, into whatever environment the kernel is using — the codespace's `base` or a local `eyes-on-earth`. No container rebuild, and the same cell works either way.

**In every tutorial notebook** the setup cell is a short `REQUIRED` dict of just the packages that notebook needs, which pip-installs anything missing. That is a mid-course safety net: better than an `ImportError` in front of a class.

There is no repository clone and no path configuration. Data goes to `os.getcwd()/data/`, which is the notebook's own module folder.

If a tutorial needs a new package, add it to [`environment.yml`](environment.yml) **and** to that notebook's `REQUIRED` dict, so it reaches both the pre-built image and anyone who has not rebuilt yet. The `0.1.1` check picks it up from `environment.yml` on its own.

## GitHub Codespaces

A Codespace gives you a browser-based JupyterLab with the environment **already built** and the repository **already present** — no clone, no install, no waiting. The setup cell in each notebook detects that everything imports and does nothing.

*Code → Codespaces → Create codespace on main* from the repository page. Then open any `X.Y.Z_*.ipynb`.

The environment is defined in [`.devcontainer/`](../.devcontainer/), built from the same `environment.yml` used locally. If you add a dependency, add it there and it flows to Codespaces, local conda, and prebuilds together.

**Instructors:** turn on **prebuilds** (*Settings → Codespaces → Set up prebuild*) before the course. Without them, the first launch runs the full conda solve and takes several minutes; with them it is seconds. Prebuilds consume Actions minutes and storage — check the current allowances for your account type.

Codespaces bills against a monthly core-hour allowance per user. `.devcontainer/devcontainer.json` asks for 16 GB of memory, and the smallest machine that offers it has 4 cores, so a codespace consumes 4 core-hours per wall-clock hour. **A codespace keeps billing while idle until it times out**, so tell students to stop theirs when they finish (*Codespaces → Stop codespace*). The default idle timeout is 30 minutes and can be shortened in user settings.

## Running locally instead

The course runs in Codespaces; this route is mainly for instructors testing a tutorial before a session. The notebooks assume only that each one sits in its own module folder, which is what Jupyter gives you when you open it from there.

**Use conda.** Cartopy, rasterio and netCDF4 wrap compiled GEOS/PROJ/GDAL/HDF5 libraries; conda-forge ships those as binaries, so this is far less painful than pip locally.

```bash
conda env create -f 0.1_Setup_and_Environment/environment.yml
```

```bash
conda activate eyes-on-earth
```

```bash
jupyter lab
```

Then open any `X.Y.Z_*.ipynb` and run it.

Pip into a venv can work, but expect to fight the geospatial wheels on some platforms — `environment.yml` is the supported route.

## Next

- [0.2 Data Access Accounts](../0.2_Data_Access_Accounts/) — register before the sessions
- [S01 Troubleshooting](../S01_Troubleshooting/) — if something breaks
