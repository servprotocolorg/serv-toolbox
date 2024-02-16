import os
from config import print_stuff, config

# Setup print stuff from config class print_stuff
print_whitespace = print_stuff.printWhitespace
print_stars = print_stuff().printStars
string_stars = print_stuff().stringStars
print_stars_reset = print_stuff(reset=1).printStars
string_stars_reset = print_stuff(reset=1).stringStars

def install_check() -> None:
    print_stars()
    print("* Checking File Configuration")
    print_stars()
    if os.path.exists(config.dotenv_file):
        print(f"{config.dotenv_file} exists")
    else:
        print(f"{config.dotenv_file} does not exist")
    if os.path.exists(config.serv_dir):
        print(f"{config.serv_dir} exists")
    else:
        print(f"{config.serv_dir} does not exist")
    if os.path.exists(config.serv_config_dir):
        print(f"{config.serv_config_dir} exists")
    else:
        print(f"{config.serv_config_dir} does not exist")
    print_stars()