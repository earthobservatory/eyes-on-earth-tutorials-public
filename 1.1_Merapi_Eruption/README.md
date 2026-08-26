# 1.1 Sentinel-2 Data Visualisation — Mount Merapi Eruption

> **Status: in preparation.**

| Notebook | |
|---|---|
| `1.1.1_Merapi_Eruption.ipynb` | [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/earthobservatory/eyes-on-earth-tutorials) |

## What you will do

Download and process Sentinel-2 L1C multispectral imagery of the Mount Merapi
eruption (11 March 2023), compute NDVI and a SWIR-RGB composite to visualise
pyroclastic flow deposits, and export georeferenced GeoTIFFs for analysis in QGIS.

## Requirements

- A free [Copernicus Dataspace](https://dataspace.copernicus.eu/) account
  (required to download Sentinel-2 scenes)
- [0.1 Setup](../0.1_Setup_and_Environment/) completed — rasterio, numpy,
  matplotlib and scikit-image all come from `environment.yml`, so there is
  nothing extra to install here

> **Note:** reading Sentinel-2 `.jp2` bands needs GDAL's `JP2OpenJPEG`
> driver, which conda-forge ships as a separate plugin package rather than
> inside `rasterio` itself. `environment.yml` therefore installs both
> `rasterio` and `libgdal-jp2openjpeg` from `conda-forge`. Without the plugin
> the first band fails with *"not recognized as being in a supported file
> format"*; install it with
> `conda install -c conda-forge libgdal-jp2openjpeg`.

## Data

| Property | Details |
|---|---|
| Sensor | Sentinel-2A MSI (Level-1C, Top of Atmosphere reflectance) |
| Scene date | 29 March 2023 (18 days post-eruption) |
| Tile | T49MDM — Central Java, Indonesia |
| Processing baseline | N0509 (DN offset: +1000; correction applied in notebook) |
| Spatial resolution | 10 m (B02–B04, B08), 20 m (B05–B07, B8A, B11, B12), 60 m (B01, B09, B10) |
| Source | [Copernicus Dataspace Browser](https://browser.dataspace.copernicus.eu/) |
| Download size | ~756 MB (`.SAFE` folder, unzipped) |

Download the scene from the Copernicus Dataspace browser, unzip it into
`data/`, and update the `data_file_path` variable in the configuration cell.
Anything under `data/` is gitignored — do not commit datasets.

> **Windows:** the `.SAFE` folder nests deeply and its filenames are long, so
> the full path to a band can pass the old 260-character limit and unzipping
> fails part-way with "path too long". Keep the repository somewhere short —
> `C:\ES4304\` rather than a nested folder under Documents or OneDrive — or
> enable long paths (*Settings → System → For developers → Enable Win32 long
> paths*). Use Windows' own *Extract All* or 7-Zip; some tools silently
> truncate instead.

The notebook writes the following output files to the working directory:

| File | Bands | Resolution |
|---|---|---|
| `B02_B03_B04_B08_10m.tif` | Blue, Green, Red, NIR | 10 m |
| `B05_B06_B07_B8A_B11_B12_20m.tif` | Red Edge, NIR narrow, SWIR | 20 m |
| `B01_B09_B10_60m.tif` | Coastal Aerosol, Water Vapour, Cirrus | 60 m |
| `NDVI_10m.tif` | Derived: (B08 − B04) / (B08 + B04) | 10 m |
| `SWIR-RGB_20m.tif` | B12 → R, B11 → G, B04 → B | 20 m |

## Background reading

- [Mount Merapi — Global Volcanism Program](https://volcano.si.edu/volcano.cfm?vn=263250)
- [ESA Sentinel-2 User Guide — Spectral Bands](https://sentinel.esa.int/en/web/sentinel/user-guides/sentinel-2-msi/resolutions/spectral)
- [ESA Sentinel-2 Naming Convention](https://sentiwiki.copernicus.eu/web/s2-products)
- [Copernicus Dataspace Browser](https://browser.dataspace.copernicus.eu/)
- [UN-SPIDER — Normalized Burn Ratio](https://www.un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail/normalized-burn-ratio)
