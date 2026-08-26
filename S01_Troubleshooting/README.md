# S01 Troubleshooting

Common problems, in roughly the order they come up.

## Setup — any platform

**`ModuleNotFoundError` for xarray, cartopy, rioxarray…**

The setup cell did not finish, or you skipped it. Re-run it and watch for a red error in the install output. If pip reports a version conflict, note the package it names and tell your instructor.

In `0.1.1` the setup cell reports `MISSING` or `BROKEN` against `environment.yml`, and the repair cell below it installs what is named, in place. Run that rather than pip installing by hand. If the repair cell itself fails, send its output to your instructor — a solve conflict or a permissions error needs fixing at the environment level.

**The course repository has been updated and you already have work in it.**

Run the update script from a terminal in the repository:

```bash
python scripts/update.py
```

It commits your work, merges the course's changes, and — the part to read — prints any file where your edits and the course's touched the same lines, because there your version is kept and the update is *not* applied. It never leaves conflict markers in a notebook. Running a notebook does not count as an edit for this purpose: outputs and code merge independently, so you still get the fix.

It also puts back any course file that has gone missing from your folder — a whole module you deleted, or dragged to the bin by accident, comes back with the course's current version. Your own files are untouched, and `data/` is gitignored, so nothing you downloaded is disturbed.

It stops if your real credentials are still typed into `0.2.1` — the commit it makes would record them in your clone's history. Run section 4 of that notebook first.

**Your files end up somewhere unexpected.**

Every notebook writes to `os.getcwd()/data/`. Section 2 of the [setup notebook](../0.1_Setup_and_Environment/) prints the working directory — if it is not the folder the notebook lives in, that is why. In JupyterLab, open notebooks through the file browser rather than by path.

**The session runs out of memory.**

The Himawari full-disc grids are 6001 × 6001. Restart the kernel and run only the cells you need — do not hold several full-disc arrays at once. If a `pcolormesh` of one is what killed it, see the plotting section below.

## Codespaces

**The codespace won't start, or you get a billing error.**

Two usual causes. Your personal monthly allowance is exhausted — check <https://github.com/settings/billing>. Or, if this is an org-owned repository, the organisation's Codespaces spending limit is still at its **$0 default**, which blocks creation entirely; an org owner fixes that under *Settings → Billing → Spending limits*.

**It takes several minutes to start.**

Prebuilds are not enabled, so the conda environment is being solved from scratch. That is an instructor fix: *Settings → Codespaces → Set up prebuild*.

**You changed `environment.yml` and nothing happened.**

The environment is baked into the image at build time, so a running codespace does not see the edit. *Command Palette → Codespaces: Rebuild Container* is what updates the image for codespaces created afterwards.

To pick the change up in the codespace you are already in — and without waiting on a rebuild — run the repair cell in [0.1.1](../0.1_Setup_and_Environment/0.1.1_Setup_and_Check.ipynb). It `conda install`s whatever is missing, from `environment.yml`, into the environment you are running in. Do both: the repair cell fixes your session, the rebuild fixes everyone else's.

**You are being billed for codespaces you are not using.**

Stopping a codespace ends compute billing, but **storage keeps billing until you delete it**. Review them at <https://github.com/codespaces> and delete the ones you have finished with. Shortening the idle timeout in <https://github.com/settings/codespaces> stops a forgotten browser tab from burning hours.

## Windows

The notebooks themselves are cross-platform — every path is built with `pathlib` or `os.path`, and nothing shells out — so these are environment problems rather than notebook ones.

**`conda activate` says the shell is not initialised.**

Use the **Anaconda Prompt** (or Miniforge Prompt) from the Start menu rather than PowerShell or `cmd`. It is the same conda, in a shell that has been initialised for it. `conda init powershell` is the alternative, and needs a new window afterwards.

**Unzipping a Sentinel-2 `.SAFE` folder fails with "path too long".**

`.SAFE` folders nest deeply and their filenames are long, so the full path to a band file can pass the old 260-character limit. Move the repository somewhere short — `C:\ES4304\` rather than a deep folder under Documents or OneDrive — or turn on *Settings → System → For developers → Enable Win32 long paths*.

**OneDrive-backed folders behave oddly.**

Files that OneDrive has made "online-only" are not on the disk, and rasterio or xarray opening one gets an error rather than data. Keep the repository outside your OneDrive folder, or mark the folder *Always keep on this device*.

**`PermissionError` when a cell deletes or overwrites a file.**

Windows will not remove a file that something still has open, and `xr.open_dataset`/`open_dataarray` hold the handle until closed. Close it first — `ds.close()`, or open it in a `with` block — then delete.

**Where is `~/.netrc`?**

`C:\Users\you\.netrc`. [0.2.1](../0.2_Data_Access_Accounts/0.2.1_Account_Check.ipynb) writes it there for you; you do not need to create it in Explorer, which makes leading-dot filenames awkward.

## Data access

**The `earthaccess.login()` cell runs forever and never finishes.**

It is waiting for you to type a username and password. This happens when a login call is left on the default `strategy="all"`, which falls back to an interactive prompt when it finds no credentials. In VS Code that prompt is a box at the **top-centre of the window**, not under the cell, so it is easy to miss entirely.

Interrupt the kernel — if the traceback ends in `getpass` or `input`, that was the cause. The notebooks all say `strategy="netrc"` precisely so this cannot happen; if yours does not, set up `.netrc` via [0.2.1](../0.2_Data_Access_Accounts/0.2.1_Account_Check.ipynb) and name the strategy.

**`LoginStrategyUnavailable`, or "No .netrc found".**

There is no `~/.netrc`, or it has no line for the host being asked for. Run [0.2.1](../0.2_Data_Access_Accounts/0.2.1_Account_Check.ipynb).

The usual cause is a **new codespace** — the file lives in your home directory, which goes when you delete a codespace. Stopping and restarting one keeps it; deleting and recreating does not.

**`LoginAttemptFailure` from `earthaccess.login()`.**

Earthdata rejected the username or password in your `.netrc`. Confirm them by logging in at <https://urs.earthdata.nasa.gov>, then re-run the write cell in 0.2.1. Each write cell replaces only its own provider's line, so the JAXA and Copernicus lines survive — there is nothing to run twice.

**JAXA: `TypeError: cannot unpack non-sequence NoneType`.**

`netrc.authenticators("ftp.ptree.jaxa.jp")` returned `None` — there is no P-Tree line in your `.netrc`. Run the JAXA write cell in 0.2.1.

**Copernicus: `401 Unauthorized` from the token request.**

The Copernicus Data Space rejected the email address or password in your `.netrc`. Confirm them by logging in at <https://dataspace.copernicus.eu/>, then re-run the Copernicus write cell in 0.2.1. If the account has two-factor authentication turned on, the request also needs a `totp` field holding the current six-digit code from your authenticator app — there is a commented-out line for it in the check cell of 0.2.1.

**Copernicus: `401 Unauthorized` on the download, with a token that just worked.**

The download host is `download.dataspace.copernicus.eu` (`zipper.…` is an older name for it). Asking `catalogue.dataspace.copernicus.eu` for the file redirects there, and `requests` drops the `Authorization` header when a redirect crosses hostnames, so the token never arrives. Request the download host directly.

**`ValueError: .netrc cannot hold this password`.**

The file format cannot store a password with a space in it, loses a backslash silently, and manages accented characters only on newer Pythons. `save_credentials()` reads back what it wrote, so it catches this at the point you run the cell rather than three notebooks later; nothing is saved and the rest of your `.netrc` is untouched. Change the password at the provider to one made of ordinary characters.

**A password containing a double quote.**

The write cells pass it as a double-quoted Python string, so a `"` in your password ends the string early and the cell raises `SyntaxError`. Wrap that one argument in single quotes instead: `'my"password'`.

**`earthaccess.search_data()` returns 0 granules.**

The `short_name` or `version` has probably changed — NASA does revise these, and a retired short name returns zero granules rather than an error, so it fails quietly. This has already happened once in this course: `PACE_OCI_L3M_CHL` v3.0 was retired and chlorophyll folded into `PACE_OCI_L3M_BGC` v3.2.

Search without the version filter to see what exists:

```python
results = earthaccess.search_data(short_name="PACE_OCI_L3M_BGC", count=5)
for r in results:
    print(r)
```

If that is also empty, the short name itself is gone. Search by keyword instead to find what replaced it:

```python
for c in earthaccess.search_datasets(keyword="PACE OCI chlorophyll", count=20):
    print(c["umm"]["ShortName"], c["umm"]["Version"])
```

**JAXA FTP: `530 Login incorrect`.**

The FTP credentials are not your P-Tree website login. The FTP username is usually your email with `@` replaced by an underscore. If your registration has not been approved yet, the login will fail — approval takes several working days. See [0.2](../0.2_Data_Access_Accounts/).

**JAXA FTP: the file you asked for does not exist.**

List the directory to see what is actually there:

```python
with FTP(FTP_SERVER) as ftp:
    ftp.login(ftp_user, ftp_password)
    ftp.cwd(REMOTE_DIR)
    print(sorted(ftp.nlst())[:20])
```

Check the satellite prefix (`H08` vs `H09`) and the year — Himawari-8 and -9 cover different periods.

## Plotting

**The map is empty, or `sel()` returns a zero-length array.**

Latitude ordering. If `lat` descends (north to south, which is common for these products) you must write `sel(lat=slice(25, -15))`, not `slice(-15, 25)`. A backwards slice returns nothing rather than raising an error. Check with:

```python
print(ds.lat.values[:3], ds.lat.values[-3:])
```

**The chlorophyll map is entirely dark blue.**

Chlorophyll-a spans orders of magnitude and needs a log scale. Use `norm=LogNorm(vmin=0.01, vmax=20)` rather than `vmin`/`vmax`.

**The tropical Pacific map is split down the middle.**

The region crosses the dateline. Use `ccrs.PlateCarree(central_longitude=180)` for the projection, keep `transform=ccrs.PlateCarree()` on the data, and express 60°W as 300 in the extent.

**Cartopy fails downloading coastlines.**

Cartopy fetches Natural Earth data on first use. If the download fails, retry — it is usually transient. Falling back to `resolution="110m"` uses a smaller file.

**Months are impossible to compare.**

Each plot autoscaled its own colour limits. Fix `vmin` and `vmax` to the same values across every plot, and in QGIS copy the style from one layer onto all the others.

## GeoTIFF and QGIS

**The GeoTIFF lands in the wrong place, or QGIS says it has no CRS.**

Both `set_spatial_dims` and `write_crs` must be called before `to_raster`:

```python
da = da.rio.set_spatial_dims(x_dim="lon", y_dim="lat")
da = da.rio.write_crs("EPSG:4326")
da.rio.to_raster(path)
```

Verify by reading it back — `check.rio.crs` and `check.rio.bounds()` should look sensible.

**The GeoTIFFs are enormous.**

A 5001 × 6001 float32 grid is about 120 MB. Compress them:

```python
da.rio.to_raster(path, compress="DEFLATE", tiled=True)
```

**QGIS shows the raster as flat grey.**

The default *Singleband gray* stretch. Switch to *Singleband pseudocolour* and set the min/max to the real data range — *Properties → Histogram → Compute Histogram* shows it.

## Still stuck?

Bring the **full error message**, not a description of it. The last few lines of a Python traceback usually name the problem exactly.
