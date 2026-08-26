# 0.2 Data Access Accounts

The satellite data used in this course is free, but the providers require you to register. **Do this well before the tutorial sessions** — one of them is not instant.

Work through [0.2.1_Account_Check.ipynb](0.2.1_Account_Check.ipynb), which sets up each login and then proves it works by downloading a real file. This README is the written reference behind it: read it if a cell fails, or if you would rather see the whole picture first.

| Provider | Needed for | Register at | Approval |
|---|---|---|---|
| **NASA Earthdata** | PACE (2.1), SWOT (2.3), OSCAR (2.4) | <https://urs.earthdata.nasa.gov/users/new> | Immediate |
| **JAXA P-Tree** | Himawari SST (2.2) | <https://www.eorc.jaxa.jp/ptree/registration_top.html> | **Up to several working days** |
| **Copernicus Data Space** | Sentinel-2 (1.1, 1.2), Sentinel-1 (3.1) | <https://dataspace.copernicus.eu/> | Immediate |

## How the credentials are stored

All three providers want a username and password. You save them once in a **`.netrc`** file in your home directory, and every notebook in the course reads them from there — so you type them once, at the start of the course, and never again.

`.netrc` is a plain text file, one line per machine:

```
machine urs.earthdata.nasa.gov login myUsername password myPassword
machine ftp.ptree.jaxa.jp login myEmail_example.com password myPtreePassword
machine identity.dataspace.copernicus.eu login myEmail@example.com password myCopernicusPassword
```

[0.2.1_Account_Check.ipynb](0.2.1_Account_Check.ipynb) writes it for you, sets the permissions, and then verifies all three logins. It writes it in Python, via `Path.home() / ".netrc"`, so the same cells work in a Codespace, on macOS and on Windows — there is no shell command and no path to type.

It lives in your home directory, which is **outside this repository**, so it is never committed:

| Where you are running | The file |
|---|---|
| Codespace, Linux, macOS | `~/.netrc` |
| Windows | `C:\Users\you\.netrc` |

The permissions are set to `600` — readable by you and nobody else — on Linux and macOS. Windows has no equivalent bits, and Python's `netrc` module only checks them on Linux and macOS, so there is nothing to do there.

It survives kernel restarts, and in a Codespace it survives stopping and starting. Delete the codespace and create a new one, though, and it goes with it — run 0.2.1 again.

### What a password can contain

`.netrc` is an old and very simple format, and it cannot hold every password: a space stops the file parsing at all, a backslash is dropped silently, and an accented character works only on newer Pythons. `save_credentials()` therefore reads back what it has just written and refuses — leaving the file as it was — rather than storing something that would fail later as a wrong password. If that happens, change the password at the provider to one made of ordinary characters.

## NASA Earthdata

One account covers every NASA dataset in this course. Register at the Earthdata User Registration Service, <https://urs.earthdata.nasa.gov/home>, and confirm your email.

The notebooks log in with `earthaccess.login(strategy="netrc")`. Two things worth knowing:

- **Name the strategy.** The default, `strategy="all"`, falls back to an interactive username/password prompt when it finds no credentials — and in VS Code that prompt appears at the top of the window, where it is easy to miss, so the cell looks like it has hung.
- **This route checks your password immediately.** A wrong one raises `LoginAttemptFailure` at the login call rather than failing later as a 401 mid-download.

## JAXA P-Tree

P-Tree is JAXA's Himawari data portal. Registration is a form, and a human approves it — **this can take several working days**, so register as soon as you start the course, not the night before Tutorial 2.

When approved you receive an **FTP username and password**. These are separate from your P-Tree web login. The username is usually your email address with the `@` replaced by an underscore.

Details and FAQ: <https://www.eorc.jaxa.jp/ptree/faq.html>

`ftplib` does not read `.netrc` on its own, so the notebooks use the standard library's `netrc` module:

```python
import netrc
from ftplib import FTP

ftp_user, _, ftp_password = netrc.netrc().authenticators("ftp.ptree.jaxa.jp")

with FTP("ftp.ptree.jaxa.jp") as ftp:
    ftp.login(ftp_user, ftp_password)
```

## Copernicus Data Space Ecosystem

The Copernicus Data Space Ecosystem (CDSE) is ESA's portal for Sentinel data. Register at <https://dataspace.copernicus.eu/> — the avatar at the top right, then **REGISTER** — and confirm the email. It works straight away; there is nobody to wait for.

The login is the email address you registered with, and there is no separate download account of the kind P-Tree has.

CDSE does not accept your password on each request. You exchange it for an **access token**, valid for a few minutes, and downloads carry the token:

```python
import netrc

import requests

CDSE_HOST = "identity.dataspace.copernicus.eu"
login, _, password = netrc.netrc().authenticators(CDSE_HOST)

token = requests.post(
    f"https://{CDSE_HOST}/auth/realms/CDSE/protocol/openid-connect/token",
    data={"client_id": "cdse-public", "grant_type": "password",
          "username": login, "password": password},
).json()["access_token"]
```

Two things that catch people out:

- **Two-factor authentication.** If you have turned it on for this account, the token request needs a `totp` field as well, holding the current six-digit code from your authenticator app. The check cell in 0.2.1 has the line ready to uncomment.
- **The download hostname.** Products are searched for on `catalogue.dataspace.copernicus.eu` and fetched from `download.dataspace.copernicus.eu` — `zipper.dataspace.copernicus.eu` is an older name for the same download service and still works. Asking the catalogue host for the file redirects to the download host, and `requests` drops the `Authorization` header across a redirect to a different hostname, so the token is lost and you get a `401` that has nothing to do with your account.

## Keeping credentials out of GitHub

Your `~/.netrc` is in your home directory, not in this repository, so it is never committed.

The cells that **write** it are another matter: they are in the repository, and you type your real password into them. Section 4 of [0.2.1](0.2.1_Account_Check.ipynb) puts the placeholders back and clears the outputs for you — run it when you are done, and do not commit the notebook before you have.

If you do commit a password by accident, change it at the provider. Removing it from the latest commit is not enough; it stays in the history.

## Next

[Tutorial 2 overview](../2.0_Tutorial_2_Overview_and_Assignment/README.md)
