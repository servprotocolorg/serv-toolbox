import os
from config import print_stuff, config
from shared import finish_node

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
    if os.path.isdir(config.serv_dir):
        print(f"* SERV Node is installed at {config.serv_dir}")
    else:
        print(f"* SERV Node is not installed at {config.serv_dir}")
    if os.path.isdir(config.serv_config_dir):
        print(f"* SERV Config is installed at {config.serv_config_dir}")
    else:
        print(f"* SERV Config is not installed at {config.serv_config_dir}")
    if os.path.isfile(config.serv_conf):
        print(f"* SERV Config File is installed at {config.serv_conf}")
    else:
        print(f"* SERV Config File is not installed at {config.serv_conf}")
    if os.path.isdir(config.toolbox_location):
        print(f"* SERV Toolbox is installed at {config.toolbox_location}")
    else:
        print(f"* SERV Toolbox is not installed at {config.toolbox_location}") 
    if os.path.isdir(config.serv_dir) and os.path.isdir(config.serv_config_dir) and os.path.isfile(config.serv_conf) and os.path.isdir(config.toolbox_location):
        print(f"* SERV Node is already installed at {config.serv_dir}")
    else:
        print(f"* SERV Node is not installed at {config.serv_dir}")
    print_stars()
    finish_node()