#!/usr/bin/env python3
"""Bring your copy of the course repository up to date, keeping your own work.

Run it from anywhere inside the repository:

    python scripts/update.py

What it does, in order:

1. Fetches the course repository.
2. Puts back any course file missing from your folder - a module you deleted,
   or dragged to the bin by accident, comes back.
3. Commits whatever you have changed, so there is something to merge against.
4. Merges with `-X ours`. Where you and the course have both changed the same
   lines, yours win - so the merge never stops half-way and leaves you with
   conflict markers in a notebook.
5. Prints the files where that happened. Those are the ones where you did NOT
   get the course's version, and they are the only part of this you must read.

Step 5 is the point of the script. `-X ours` on its own resolves silently: a
notebook you have merely run has different `outputs` and `execution_count`
lines sitting next to the code, so a fix to that code can be dropped without
anything being said about it. The script checks each shared file for a real
overlap first, so what it prints is what you did not get - not just every file
you happen to have touched.

Plain Python rather than a shell script so it behaves the same on Windows.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ACCOUNT_NB = Path("0.2_Data_Access_Accounts/0.2.1_Account_Check.ipynb")

# What the write cells in 0.2.1 look like before anyone types real credentials
# into them. Section 4 of that notebook puts these back.
PLACEHOLDERS = {"myUsername", "myPassword",
                "myEmail_example.com", "myPtreePassword"}


def git(*args, check=True):
    """Run a git command in the repository and return its stdout, stripped."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def repo_root():
    root = git("rev-parse", "--show-toplevel")
    if not root:
        sys.exit("Not inside a git repository - open a terminal in the course "
                 "folder and try again.")
    return Path(root)


def credentials_are_typed_in(root):
    """True if 0.2.1 currently holds something other than the placeholders.

    Step 1 commits your working tree as it stands. If your Earthdata or P-Tree
    password is still sitting in a code cell, that commit records it in this
    clone's history, where deleting the line afterwards does not remove it.
    """
    path = root / ACCOUNT_NB
    if not path.exists():                     # renamed or removed - not our
        return False                          # business to guess

    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        for line in cell["source"]:
            if not line.lstrip().startswith("save_credentials("):
                continue
            # "save_credentials("host", "login", "password")" -> the arguments
            arguments = [part.strip().strip('"\'')
                         for part in line[line.index("(") + 1:
                                          line.rindex(")")].split(",")]
            if any(argument not in PLACEHOLDERS for argument in arguments[1:]):
                return True
    return False


def yours_would_win(root, base, remote_branch, paths):
    """Of `paths`, the ones where your version actually displaces the course's.

    Both sides changing the same file is not enough: git merges two edits to
    different parts of one notebook without either side losing anything, which
    is the common case. What matters is whether the two edits overlap, because
    that is where `-X ours` quietly drops the course's side.

    Each candidate is merged in a scratch copy first - `git merge-file` is the
    same three-way merge git is about to run, minus the automatic resolution -
    and a non-zero exit means it conflicted, so yours would win it.
    """
    losers = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for path in paths:
            versions = {}
            for name, revision in (("base", base), ("ours", "HEAD"),
                                   ("theirs", remote_branch)):
                blob = subprocess.run(["git", "show", f"{revision}:{path}"],
                                      capture_output=True, cwd=root)
                if blob.returncode != 0:
                    # Missing on one side: added or deleted there. git cannot
                    # merge that silently, so it always needs your attention.
                    versions = None
                    break
                versions[name] = tmp / name
                versions[name].write_bytes(blob.stdout)

            if versions is None:
                losers.append(path)
                continue

            merged = subprocess.run(
                ["git", "merge-file", "-p",
                 str(versions["ours"]), str(versions["base"]),
                 str(versions["theirs"])],
                capture_output=True, cwd=root)
            if merged.returncode != 0:        # conflicts, or an unmergeable
                losers.append(path)           # binary file
    return losers


def restore_deleted(root, remote_branch):
    """Put back any course file that is missing from your folder.

    Deleting a module - or dragging one to the bin by accident - is otherwise
    permanent: the deletion becomes part of your commit, and a merge has no
    reason to undo it. Worse, if the course has since changed a file you
    deleted, git calls that a modify/delete conflict and stops the update.

    Two kinds of missing file, restored from different places:

    - Deleted since your last update: your own last version is in HEAD, and
      restoring from there keeps any edits you had made to it.
    - Deleted before an earlier update, so the deletion is already committed:
      HEAD does not have it either, so it comes from the course instead.

    Files you have never committed are not tracked and cannot go missing this
    way, and `data/` is gitignored, so nothing you downloaded is touched.
    """
    restored = []

    gone_from_worktree = git("ls-files", "--deleted").splitlines()
    if gone_from_worktree:
        git("checkout", "HEAD", "--", *gone_from_worktree)
        restored.extend(gone_from_worktree)

    course_files = git("ls-tree", "-r", "--name-only",
                       remote_branch).splitlines()
    never_arrived = [f for f in course_files if not (root / f).exists()]
    if never_arrived:
        git("checkout", remote_branch, "--", *never_arrived)
        restored.extend(never_arrived)

    return sorted(restored)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--branch", default="main",
                        help="course branch to merge from (default: main)")
    parser.add_argument("--force", action="store_true",
                        help="update even if 0.2.1 still holds real credentials")
    args = parser.parse_args()

    root = repo_root()
    os.chdir(root)                # so every path below is repository-relative
    remote_branch = f"origin/{args.branch}"

    if credentials_are_typed_in(root) and not args.force:
        sys.exit(
            f"Your credentials are still typed into {ACCOUNT_NB}.\n\n"
            "This script commits your work before merging, and that commit "
            "would put your\npassword into this clone's git history, where "
            "deleting the line later does not\nremove it.\n\n"
            "Run section 4 of that notebook first - it puts the placeholders "
            "back - then\nrun this again. Or pass --force if you know what you "
            "are doing.")

    # 1. Fetch first, so a file you deleted can be restored from the course
    #    even when your own history no longer has it either.
    print(f"Fetching {remote_branch} ...")
    git("fetch", "origin", args.branch)

    # 2. Put back anything of the course's that has gone missing, before it
    #    can be committed as a deletion or turn into a modify/delete conflict.
    restored = restore_deleted(root, remote_branch)
    if restored:
        print(f"\nRestored {len(restored)} course file(s) that were missing "
              "from your folder:")
        for path in restored[:10]:
            print("   ", path)
        if len(restored) > 10:
            print(f"    ... and {len(restored) - 10} more")
        print()

    # 3. Commit local work. Without a commit there is nothing to merge into,
    #    and git refuses to merge over modified files anyway.
    if git("status", "--porcelain"):
        git("add", "-A")
        git("-c", "user.email=you@example.com", "-c", "user.name=course work",
            "commit", "-m", "Work in progress, saved before a course update")
        print("Committed your changes.")
    else:
        print("Nothing of yours to commit.")

    # 4. Work out the overlap before merging: files the course changed since we
    #    last shared history, that you have also changed. After the merge these
    #    are indistinguishable from files only you touched.
    base = git("merge-base", "HEAD", remote_branch)
    upstream_changed = set(git("diff", "--name-only", base,
                               remote_branch).splitlines())
    if not upstream_changed:
        print("\nAlready up to date - the course has not changed since your "
              "last update.")
        return

    yours_changed = set(git("diff", "--name-only", base, "HEAD").splitlines())
    overlap = sorted(upstream_changed & yours_changed)
    displaced = yours_would_win(root, base, remote_branch, overlap)

    # 5. Merge. -X ours, not -s ours: -s would throw away the whole update.
    result = subprocess.run(
        ["git", "-c", "user.email=you@example.com", "-c",
         "user.name=course work", "merge", "-X", "ours", "--no-edit",
         remote_branch],
        capture_output=True, text=True, cwd=root)
    print(result.stdout.strip())

    if result.returncode != 0:
        print(result.stderr.strip())
        sys.exit("\nThe merge stopped. This usually means a file was deleted "
                 "on one side and\nedited on the other. Show this output to "
                 "your instructor rather than guessing.")

    print(f"\nUpdated {len(upstream_changed)} file(s) from the course.")

    if displaced:
        print("\n" + "=" * 70)
        print("READ THIS. You had edited the same lines the course changed, so")
        print("your version was kept and its changes were NOT applied here:\n")
        for path in displaced:
            print("   ", path)
        print("\nTo see what you did not get, for any one of them:")
        print(f"    git diff HEAD {remote_branch} -- <file>")
        print("\nTo take the course's version instead, throwing away your")
        print("changes to that file:")
        print(f"    git checkout {remote_branch} -- <file>")
        print("=" * 70)
    elif overlap:
        print(f"{len(overlap)} file(s) you had edited were updated as well, "
              "and both sets of\nchanges survived - nothing of yours was lost, "
              "and nothing was withheld.")
    else:
        print("None of the updated files clashed with your own work.")


if __name__ == "__main__":
    main()
