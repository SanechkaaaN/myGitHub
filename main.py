import os
import sys
import shutil

MYGIT_DIR = ".mygit"
COMMITS_DIR = os.path.join(MYGIT_DIR, "commits")
SEQUENCE_FILE = os.path.join(MYGIT_DIR, ".sequence")
IGNORE_FILE = ".mygitignore"


def get_ignored_patterns():
    # то что не копировать
    ignored = {MYGIT_DIR, IGNORE_FILE}
    if os.path.exists(IGNORE_FILE):
        with open(IGNORE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    ignored.add(name)
    return ignored


def is_ignored(path, ignored_set):
    parts = path.split(os.sep)  # сплитим путь на части: ['folder', 'sub', 'file.txt']
    for part in parts:
        if part in ignored_set:
            return True
    return False


def init():
    if os.path.exists(MYGIT_DIR):
        print("Repository already initialized")
        return
    os.makedirs(COMMITS_DIR)
    with open(SEQUENCE_FILE, "w") as f:
        f.write("1")
    print("Initialized empty mygit repository")


def commit(message):
    if not os.path.exists(MYGIT_DIR):
        print("Error: Repository not initialized")
        return

    # Читаем номер коммита
    with open(SEQUENCE_FILE, "r") as f:
        commit_id = f.read().strip()

    ignored = get_ignored_patterns()
    dest_path = os.path.join(COMMITS_DIR, commit_id, "root")

    files_count = 0

    # Проходим по всем файлам проекта
    for root, dirs, files in os.walk("."):
        for file in files:
            # Склеиваем полный путь к файлу
            full_path = os.path.join(root, file)
            # убираем '.' в начале
            rel_path = os.path.relpath(full_path, ".")

            # ПРОВЕРКА: если файл или любая папка в его пути (в игноре) — пропускаем
            if is_ignored(rel_path, ignored):
                continue

            # Копируем
            dst_file = os.path.join(dest_path, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(full_path, dst_file)
            files_count += 1

    # Сохраняем описание
    msg_path = os.path.join(COMMITS_DIR, commit_id, "message.txt")
    with open(msg_path, "w", encoding="utf-8") as f:
        f.write(message)

    # Обновляем счетчик
    with open(SEQUENCE_FILE, "w") as f:
        f.write(str(int(commit_id) + 1))

    print(f"Committed as {commit_id}. Files saved: {files_count}")



def checkout(commit_id):
    commit_root = os.path.join(COMMITS_DIR, str(commit_id), "root")
    if not os.path.exists(commit_root):
        print(f"Error: Commit {commit_id} not found")
        return

    # Очистка текущей папки
    ignored = get_ignored_patterns()
    for item in os.listdir("."):
        if item == MYGIT_DIR:
            continue

        # удаляем только то, что НЕ в игноре
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

    # достаем из архива
    for root, dirs, files in os.walk(commit_root):
        rel_root = os.path.relpath(root, commit_root)
        target_dir = os.path.join(".", rel_root)

        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            shutil.copy2(src, dst)

    print(f"Switched to commit {commit_id}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python mygit.py [init|commit|checkout] [args]")
        return
    cmd = sys.argv[1]
    if cmd == "init":
        init()
    elif cmd == "commit" and len(sys.argv) > 2:
        commit(sys.argv[2])
    elif cmd == "checkout" and len(sys.argv) > 2:
        checkout(sys.argv[2])
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()