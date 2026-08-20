# ES4304 — Eyes on Earth

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/earthobservatory/eyes-on-earth-tutorials)

Course materials for ES4304. The tutorials run in a GitHub Codespace — there is nothing to install on your own machine.

## Getting started

Work through module `0.1` once, check your accounts in `0.2`, then follow the tutorials in numerical order.

| | How | Setup |
|---|---|---|
| **GitHub Codespaces** *(what the course uses)* | *Code → Codespaces → Create codespace on main*, or the badge above | None — the environment is pre-built and the repository is already here |
| **Local conda** | `conda env create -f 0.1_Setup_and_Environment/environment.yml` | One-time, on your own machine |

Use a Codespace unless you have a reason not to. The local route exists mainly for instructors testing a tutorial before a session.

The setup cell at the top of each tutorial notebook checks what is importable and installs anything missing, so it does nothing at all in a Codespace. `0.1.1` checks against `environment.yml`, and has a repair cell that updates your environment from that file if something is wrong.

**Stop your codespace when you finish** — *Codespaces → Stop codespace*. It bills against your monthly allowance while it idles. Delete it when the course ends; a stopped codespace still uses storage.

## Contents

### 0. Before the course

| Module | Contents |
|---|---|
| [0.1_Setup_and_Environment](0.1_Setup_and_Environment/) | Environment setup and check — **run this first** |
| [0.2_Data_Access_Accounts](0.2_Data_Access_Accounts/) | NASA Earthdata and JAXA P-Tree registration — **do this early**, one takes days to approve |

### 1. Tutorial 1

| Module | Contents |
|---|---|
| [1.0_Tutorial_1_Overview_and_Assignment](1.0_Tutorial_1_Overview_and_Assignment/) | *In preparation* |
| [1.1_TBD](1.1_TBD/) | *In preparation* |

### 2. Tutorial 2 — Ocean colour, temperature, topography

| Module | Contents | |
|---|---|---|
| [2.0_Tutorial_2_Overview_and_Assignment](2.0_Tutorial_2_Overview_and_Assignment/) | Handout, background, questions, assignment | |
| [2.1_Ocean_Colour_with_PACE_OCI](2.1_Ocean_Colour_with_PACE_OCI/) | Chlorophyll-a from PACE OCI | |
| [2.2_Sea_Surface_Temperature_with_Himawari](2.2_Sea_Surface_Temperature_with_Himawari/) | SST from Himawari-8/9 | |
| [2.3_Sea_Surface_Height_with_SWOT](2.3_Sea_Surface_Height_with_SWOT/) | Sea surface height anomalies from SWOT | |
| [2.4_Ocean_Surface_Currents_with_OSCAR](2.4_Ocean_Surface_Currents_with_OSCAR/) | Surface currents from OSCAR | |

### 3. Tutorial 3

| Module | Contents |
|---|---|
| [3.0_Tutorial_3_Overview_and_Assignment](3.0_Tutorial_3_Overview_and_Assignment/) | *In preparation* |
| [3.1_TBD](3.1_TBD/) | *In preparation* |

### 4. Tutorial 4

| Module | Contents |
|---|---|
| [4.0_Tutorial_4_Overview_and_Assignment](4.0_Tutorial_4_Overview_and_Assignment/) | *In preparation* |
| [4.1_TBD](4.1_TBD/) | *In preparation* |

### Supplementary

| Module | Contents |
|---|---|
| [S01_Troubleshooting](S01_Troubleshooting/) | Common errors and how to fix them |

## How the numbering works

`<tutorial>.<topic>_Descriptive_Name` — the first digit is the tutorial, the second is the topic within it. `X.0` is always the tutorial overview and assignment; `X.1`, `X.2`, … are the individual notebooks.

Supplementary material that does not belong to any one tutorial uses an `S##_` prefix and sits at the end. This lets you insert extra material without renumbering anything.

Each module folder is self-contained: its notebook(s), its `README.md`, and whatever it needs — `Figs/` for images, `data/` for inputs and outputs.

## For instructors and TAs

See [CONTRIBUTING.md](CONTRIBUTING.md) for the module template and conventions to follow when writing tutorials 1, 3 and 4.

## Licence

[GNU GENERAL PUBLIC LICENSE Version 3](LICENSE).
