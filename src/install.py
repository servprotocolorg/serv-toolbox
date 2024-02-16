import os
from config import print_stuff, config

def install_check() -> None:
    if os.path.exists(config.dotenv_file):
        print(f"{config.dotenv_file} exists")
    else:
        print(f"{config.dotenv_file} does not exist")