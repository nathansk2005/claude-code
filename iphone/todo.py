"""A small password-protected to-do list for the terminal. Runs in a-Shell, iSH, or any Python 3.

Usage:
    python3 todo.py                 show the list
    python3 todo.py add Buy milk    add a task
    python3 todo.py done 2          mark task 2 as done
    python3 todo.py remove 2        delete task 2
    python3 todo.py clear           delete all finished tasks

Tasks are saved encrypted in todo.enc next to this script. You choose a password
the first time and type it each time you run the script. To skip typing it for
the rest of a terminal session, run: export TODO_PASSWORD='your password'

There is no way to recover the list if you forget the password.

An unencrypted todo.json from an older version is encrypted and deleted on the
first run.
"""

import getpass
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path

OLD_FILE = Path(__file__).with_name("todo.json")
TODO_FILE = Path(__file__).with_name("todo.enc")

# File layout: MAGIC | salt | nonce | ciphertext | tag.
# Only the Python standard library is available everywhere this runs, and it has
# no AES, so the cipher is HMAC-SHA256 in counter mode with encrypt-then-MAC.
MAGIC = b"TODO1"
SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 32
ITERATIONS = 300_000


class WrongPassword(Exception):
    pass


def derive_keys(password, salt):
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS, dklen=64)
    return key[:32], key[32:]


def keystream_xor(key, nonce, data):
    out = bytearray()
    for block in range(0, len(data), 32):
        counter = (block // 32).to_bytes(8, "big")
        pad = hmac.new(key, nonce + counter, hashlib.sha256).digest()
        chunk = data[block:block + 32]
        out += bytes(a ^ b for a, b in zip(chunk, pad))
    return bytes(out)


def encrypt(keys, salt, plaintext):
    enc_key, mac_key = keys
    nonce = os.urandom(NONCE_SIZE)
    body = MAGIC + salt + nonce + keystream_xor(enc_key, nonce, plaintext)
    return body + hmac.new(mac_key, body, hashlib.sha256).digest()


def decrypt(password, blob):
    """Return (keys, salt, plaintext) so the caller can save again without re-deriving."""
    if not blob.startswith(MAGIC) or len(blob) < len(MAGIC) + SALT_SIZE + NONCE_SIZE + TAG_SIZE:
        raise ValueError(f"{TODO_FILE.name} is not a to-do file or is damaged.")
    body, tag = blob[:-TAG_SIZE], blob[-TAG_SIZE:]
    salt = body[len(MAGIC):len(MAGIC) + SALT_SIZE]
    nonce = body[len(MAGIC) + SALT_SIZE:len(MAGIC) + SALT_SIZE + NONCE_SIZE]
    ciphertext = body[len(MAGIC) + SALT_SIZE + NONCE_SIZE:]
    keys = derive_keys(password, salt)
    if not hmac.compare_digest(hmac.new(keys[1], body, hashlib.sha256).digest(), tag):
        raise WrongPassword
    return keys, salt, keystream_xor(keys[0], nonce, ciphertext)


def ask_password(new):
    password = os.environ.get("TODO_PASSWORD")
    if password:
        return password
    if not new:
        return getpass.getpass("Password: ")
    print("Choose a password for your to-do list. If you forget it, the list cannot be recovered.")
    while True:
        password = getpass.getpass("New password: ")
        if not password:
            print("The password cannot be empty.")
        elif password != getpass.getpass("Type it again: "):
            print("The passwords did not match. Try again.")
        else:
            return password


def load():
    """Return (tasks, keys, salt), asking for the password."""
    if TODO_FILE.exists():
        password = ask_password(new=False)
        keys, salt, plaintext = decrypt(password, TODO_FILE.read_bytes())
        return json.loads(plaintext), keys, salt
    salt = os.urandom(SALT_SIZE)
    keys = derive_keys(ask_password(new=True), salt)
    tasks = json.loads(OLD_FILE.read_text()) if OLD_FILE.exists() else []
    return tasks, keys, salt


def save(tasks, keys, salt):
    TODO_FILE.write_bytes(encrypt(keys, salt, json.dumps(tasks).encode()))
    if OLD_FILE.exists():
        OLD_FILE.unlink()
        print(f"Encrypted your old list and deleted {OLD_FILE.name}.")


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
    command = args[0] if args else "list"
    rest = args[1:]
    if command not in ("list", "add", "done", "remove", "clear"):
        print(__doc__)
        return

    try:
        tasks, keys, salt = load()
    except WrongPassword:
        print("Wrong password.")
        return
    except ValueError as error:
        print(error)
        return

    if command == "add":
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

    save(tasks, keys, salt)
    print()
    show(tasks)


if __name__ == "__main__":
    main(sys.argv[1:])
