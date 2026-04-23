

MYGIT_DIR = ".mygit"
COMMITS_DIR = os.path.join(MYGIT_DIR, "commits")
MESSAGE_DIR = os.path.join(MYGIT_DIR, ".message")
SEQUENCE_FILE = os.path.join(MYGIT_DIR, ".sequence")
IGNORE_FILE = ".mygitignore"


def get_ignored_files():
    import os
    ignored = set()

    if os.path.exists(IGNORE_FILE):
        with open(IGNORE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    ignored.add(line)

    ignored.add(MYGIT_DIR)
    return ignored


def should_ignore(path, ignored):
    for item in ignored:
        if path.startswith(item):
            return True
    return False


def init():
    import os
    if os.path.exists(MYGIT_DIR):
        print("Repository already initialized")
        return

    os.makedirs(COMMITS_DIR)
    os.makedirs(MESSAGE_DIR)

    with open(SEQUENCE_FILE, "w") as f:
        f.write("1")

    print("Initialized empty mygit repository")


def get_next_commit_id():
    with open(SEQUENCE_FILE, "r") as f:
        return int(f.read())


def collect_files(ignore):
    all_files = []

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ignore]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, ".")

            if not should_ignore(rel_path, ignore):
                all_files.append((file_path, rel_path))

    return all_files


def commit(message):
    import os
    import shutil
    if not os.path.exists(MYGIT_DIR):
        print("Repository not initialized")
        return

    ignore = get_ignored_files()
    commit_id = get_next_commit_id()

    commit_path = os.path.join(COMMITS_DIR, str(commit_id))
    os.makedirs(commit_path)

    # сохраняем сообщение отдельно
    with open(os.path.join(MESSAGE_DIR, str(commit_id)), "w") as f:
        f.write(message)

    files = collect_files(ignore)

    for src, rel in files:
        dst = os.path.join(commit_path, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    # обновляем sequence
    with open(SEQUENCE_FILE, "w") as f:
        f.write(str(commit_id + 1))

    print(f"Committed as {commit_id}")
