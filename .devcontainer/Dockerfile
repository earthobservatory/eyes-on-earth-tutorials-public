# ES4304 course environment, baked into the image.
#
# Building the conda environment here (rather than in postCreateCommand) is
# deliberate: it lets GitHub Codespaces *prebuild* the image, so a student's
# codespace starts in seconds with everything already installed. If this moved
# to postCreateCommand, every student would wait through the conda solve.

FROM mcr.microsoft.com/devcontainers/miniconda:3

# environment.yml is the single source of truth for the environment, shared
# with anyone running locally via `conda env create`.
COPY 0.1_Setup_and_Environment/environment.yml /tmp/environment.yml

# Install into the base environment rather than a named one. A single
# environment means JupyterLab and the VS Code notebook editor find the right
# interpreter with no kernel-switching step for students to get wrong.
RUN conda env update -n base -f /tmp/environment.yml \
    && conda clean -afy \
    && rm /tmp/environment.yml

# Pre-download Cartopy's Natural Earth coastlines. Without this, the first
# plot in every notebook makes a network call to naturalearthdata.com, which
# is a bad thing to discover mid-lab with thirty students on one wifi network.
RUN python -c "\
import cartopy.io.shapereader as shp; \
[shp.natural_earth(resolution=r, category='physical', name=n) \
 for r in ('110m', '50m') for n in ('coastline', 'land', 'ocean')]"
