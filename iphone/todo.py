"""A small to-do list for the terminal. Runs in a-Shell, iSH, or any Python 3.

Usage:
    python3 todo.py                 show the list
    python3 todo.py add Buy milk    add a task
    python3 todo.py done 2          mark task 2 as done
    python3 todo.py remove 2        delete task 2
    python3 todo.py clear           delete all finished tasks

Tasks are saved in todo.json next to this script.
"""

import json
import sys
from pathlib import Path

TODO_FILE = Path(__file__).with_name("todo.json")


def load():
    if not TODO_FILE.exists():
        return []
    return json.loads(TODO_FILE.read_text())


def save(tasks):
    TODO_FILE.write_text(json.dumps(tasks, indent=2))


def show(tasks):
    if not tasks:
        print("Nothing to do. Add a task with: python3 todo.py add <task>")
        return
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"{number}. [{mark}] {task['text']}")


def pick(tasks, args):
    """Return the index of the task numbered in args, or None if it is not valid."""
    if not args or not args[0].isdigit():
        print("Give a task number, for example: python3 todo.py done 1")
        return None
    index = int(args[0]) - 1
    if not 0 <= index < len(tasks):
        print(f"There is no task {args[0]}.")
        return None
    return index


def main(args):
    tasks = load()
    command = args[0] if args else "list"
    rest = args[1:]

    if command == "list":
        pass
    elif command == "add":
        text = " ".join(rest).strip()
        if not text:
            print("Write the task after add, for example: python3 todo.py add Buy milk")
            return
        tasks.append({"text": text, "done": False})
        print(f"Added: {text}")
    elif command == "done":
        index = pick(tasks, rest)
        if index is None:
            return
        tasks[index]["done"] = True
        print(f"Done: {tasks[index]['text']}")
    elif command == "remove":
        index = pick(tasks, rest)
        if index is None:
            return
        print(f"Removed: {tasks.pop(index)['text']}")
    elif command == "clear":
        before = len(tasks)
        tasks = [task for task in tasks if not task["done"]]
        print(f"Cleared {before - len(tasks)} finished task(s).")
    else:
        print(__doc__)
        return

    save(tasks)
    print()
    show(tasks)


if __name__ == "__main__":
    main(sys.argv[1:])
