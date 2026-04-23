

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
