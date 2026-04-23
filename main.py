import os
import sys
import shutil

MYGIT_DIR = ".mygit"
COMMITS_DIR = os.path.join(MYGIT_DIR, "commits")


def init():
    if os.path.exists(MYGIT_DIR):
        print("Repository already initialized")
        return

    os.makedirs(COMMITS_DIR)
    print("Initialized empty mygit repository")
