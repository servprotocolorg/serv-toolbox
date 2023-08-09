import subprocess, os
from toolbox.config import EnvironmentVariables
from toolbox.library import loader_intro, print_stars

if __name__ == "__main__":
    loader_intro()
    subprocess.run("clear")
    print_stars()
    if os.path.isfile(EnvironmentVariables.user_home_dir + "/serv.sh"):
        print(
            "* serv.sh already exists in ~/\n*\n* This will exit, please change to your home directory and run ./serv.sh to launch the toolbox.\n*\n* Run ./serv.sh -h for our new help menu!\n*"
        )
    else:
        print("* Downloading serv.sh to ~/")
        subprocess.run(
            "cd ~/ && wget -O serv.sh https://raw.githubusercontent.com/ServProtocolOrg/serv-toolbox/main/src/bin/serv.sh && chmod +x serv.sh && ./serv.sh",
            shell=True,
        )
    print_stars()
