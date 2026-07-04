#!/usr/bin/env python3
"""
Task Tracker CLI

A small command-line task tracker used as the running example for the Git
Basics and Git Branching labs. Tasks are stored in a local JSON file
(tasks.json) so the data changes alongside the code as commits are made,
which makes diffs and merges feel realistic.

Usage:
    python task_tracker.py add "Buy milk"
    python task_tracker.py list
    python task_tracker.py done 1
    python task_tracker.py remove 1'
    python task_tracker.py done 3
"""

import json
import sys
from pathlib import Path

DB_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not DB_FILE.exists():
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def cmd_add(args):
    if not args:
        print("error: 'add' requires a task description")
        return 1

    description = " ".join(args)
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1

    tasks.append({
        "id": new_id,
        "description": description,
        "done": False,
        "priority": "normal"
    })
    save_tasks(tasks)
    print(f"Added task #{new_id}: {description}")
    return 0


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: task_tracker.py add \"...\"")
        return 0

    for task in tasks:
        box = "x" if task["done"] else " "
        print(f"[{box}] ({task["priority"]}) #{task['id']}  {task['description']}")
    return 0


def cmd_done(args):
    if not args:
        print("error: 'done' requires a task id")
        return 1

    task_id = int(args[0])
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task #{task_id} done")
            return 0

    print(f"error: no task with id {task_id}")
    return 1


def cmd_remove(args):
    if not args:
        print("error: 'remove' requires a task id")
        return 1

    task_id = int(args[0])
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]

    if len(remaining) == len(tasks):
        print(f"error: no task with id {task_id}")
        return 1

    save_tasks(remaining)
    print(f"Removed task #{task_id}")
    return 0


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "remove": cmd_remove,
}


def print_help():
    print(__doc__)


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print_help()
        return 0

    command, *args = argv
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"error: unknown command '{command}'")
        print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
