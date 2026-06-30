# Task Tracker CLI: Git Branching Lab

A minimal task-tracker CLI used as the running example for the Git
Branching lab (maps to Pro Git chapter 3, sections 3.1-3.6).

## Files

- `task_tracker.py`: the program (`add`, `list`, `done`, `remove` commands)
- `LAB.md`: step-by-step branching/merging/rebasing exercises against this code
- `.gitignore`: ignores the generated `tasks.json` data file

## Quick start

```console
$ python3 task_tracker.py add "Buy milk"
$ python3 task_tracker.py add "Write Git lab"
$ python3 task_tracker.py list
$ python3 task_tracker.py done 1
$ python3 task_tracker.py list
$ python3 task_tracker.py remove 2
```

## Using this for the lab

Don't `git init` inside this folder as-is. Start fresh per `LAB.md` so
students get a clean, single initial commit to branch from:

```console
$ mkdir task-tracker-lab && cd task-tracker-lab
$ cp /path/to/task_tracker.py .
$ cp /path/to/.gitignore .
$ git init
$ git add task_tracker.py .gitignore
$ git commit -m "Initial commit: basic task tracker CLI"
```

Then follow `LAB.md` from Part 1.

Two things are intentionally embedded in the starter code for the exercises
in `LAB.md`:

1. A real bug in `cmd_add`'s id assignment (Part 2, hotfix exercise).
2. A docstring block worth editing two different ways on two branches
   (Part 4, guaranteed-conflict exercise).

