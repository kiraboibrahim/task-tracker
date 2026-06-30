# Git Branching Lab: Task Tracker CLI

This lab uses `task_tracker.py`, a tiny task-tracker CLI, as the project you
branch, merge, and rebase against. Each part maps to a section of
"Git Branching" (chapter 3) in the Pro Git book.

Start by initializing the repo:

```console
$ git init task-tracker-lab
$ cd task-tracker-lab
# copy task_tracker.py into this folder
$ git add task_tracker.py
$ git commit -m "Initial commit: basic task tracker CLI"
```

---

## Part 1: Branches in a Nutshell (3.1)

1. Create a branch called `testing` without switching to it:
   `git branch testing`
2. Run `git log --oneline --decorate` and confirm `HEAD -> master, testing`
   both point at the same commit.
3. Switch to `testing` with `git checkout testing` (or `git switch testing`),
   add a trivial comment to the top of `task_tracker.py`, and commit.
4. Switch back to `master` and confirm the file no longer has your comment.
   This is the "switching branches changes your working directory" lesson.

---

## Part 2: Basic Branching and Merging (3.2)

You'll add a real feature on a topic branch while a "bug" comes in on a
hotfix branch, the same shape as the book's `iss53` / `hotfix` example.

**Feature branch: add a `priority` field to tasks**

```console
$ git checkout -b feature/priority
```

In `cmd_add`, extend the task dict to include a `priority` key (default
`"normal"`), and update `cmd_list` to show it, e.g. `[ ] #1 (normal)  Buy milk`.
Commit your work, but don't merge yet.

**Interrupt: a hotfix arrives**

```console
$ git checkout master
$ git checkout -b hotfix/duplicate-ids
```

Fix the id-assignment bug in `cmd_add`'s `new_id = len(tasks) + 1` line:
replace it with something based on the max existing id instead of the
count, so removing a task and adding a new one can't collide:

```python
new_id = max((t["id"] for t in tasks), default=0) + 1
```

Test it, commit, then ship it:

```console
$ git checkout master
$ git merge hotfix/duplicate-ids
$ git branch -d hotfix/duplicate-ids
```

Confirm this was a **fast-forward** merge (the log will say so).

**Resume the feature and merge it**

```console
$ git checkout feature/priority
# finish the work, commit
$ git checkout master
$ git merge feature/priority
```

This one is **not** a fast-forward (master moved during the hotfix), so Git
creates a real merge commit. Run
`git log --oneline --decorate --graph --all` to see the diverged-then-rejoined
shape from the book.

---

## Part 3: Branch Management (3.3)

```console
$ git branch -v
$ git branch --merged
$ git branch --no-merged
```

Create one more throwaway branch, `experiment/colors`, don't merge it, and
confirm it shows up under `--no-merged`. Then try `git branch -d
experiment/colors` (Git should refuse) followed by `git branch -D
experiment/colors` (force delete).

Practice the rename workflow: rename `master` to `main` locally with
`git branch --move master main` (skip the push steps if you don't have a
remote set up for this lab).

---

## Part 4: A Guaranteed Merge Conflict (3.2 again, on purpose)

This is the most useful exercise: a conflict you *cause* deliberately so you
can practice resolving one safely.

```console
$ git checkout -b feature/help-text
```

Edit the module docstring at the top of `task_tracker.py` (the `"""..."""`
block) to add a new usage example, e.g. a line documenting a `done` example.
Commit it.

```console
$ git checkout main
$ git checkout -b feature/help-text-v2
```

On this **second** branch, edit the *same* docstring lines but word them
differently, e.g. reorder the usage examples or change the wording.
Commit it, then merge both into `main` one after another:

```console
$ git checkout main
$ git merge feature/help-text
$ git merge feature/help-text-v2
```

The second merge will conflict. Open `task_tracker.py`, look for the
`<<<<<<<` / `=======` / `>>>>>>>` markers, hand-resolve them into one sensible
docstring, then:

```console
$ git add task_tracker.py
$ git commit
```

---

## Part 5: Branching Workflows (3.4)

Set up a tiny long-running-branch structure:

- `main`: stable
- `develop`: where finished feature branches land first

Create `develop` off `main`, then create two short-lived topic branches off
`develop` (e.g. `feature/due-dates` and `feature/search`) and merge both into
`develop` once "done." Only merge `develop` into `main` when you're happy
with both. This mirrors the book's silo diagram.

---

## Part 6: Remote Branches (3.5)

If you have access to a blank remote (GitHub/GitLab/a bare repo on disk),
practice:

```console
$ git remote add origin <url>
$ git push -u origin main
$ git push origin feature/priority
$ git fetch origin
$ git branch -vv
$ git push origin --delete feature/priority   # after it's merged
```

No remote handy? Simulate one locally:

```console
$ git init --bare ../task-tracker-remote.git
$ git remote add origin ../task-tracker-remote.git
$ git push -u origin main
```

---

## Part 7: Rebasing (3.6)

Create one more small branch, make 2-3 commits on it (e.g. incremental
improvements to `cmd_list`'s output formatting), then:

```console
$ git checkout your-branch
$ git rebase main
$ git checkout main
$ git merge your-branch    # should fast-forward
```

Compare `git log --oneline --graph` before and after rebasing to see the
linear history rebase produces versus the merge-commit shape from Part 2.

**Discussion prompt:** which of today's branches would have been safe to
rebase, and which would not have been (per the golden rule), if this had
been a shared remote repository with collaborators already pulling your
branches?
