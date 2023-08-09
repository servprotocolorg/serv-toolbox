import subprocess
from pathlib import Path
from toolbox.config import EnvironmentVariables
from toolbox.library import loader_intro, print_stars

if __name__ == "__main__":
    loader_intro()
    subprocess.run(["clear"])
    print_stars()
    harmony_script_path = Path(EnvironmentVariables.user_home_dir) / "serv.sh"
    if harmony_script_path.is_file():
        print("* serv.sh already exists in ~/\n*\n* Launching the toolbox with help menu.")
        subprocess.run(["bash", "-x", str(harmony_script_path), "-h"])
    else:
        print("* Downloading serv.sh to ~/")
        subprocess.run(["wget", "-O", str(harmony_script_path), "https://raw.githubusercontent.com/ServProtocolOrg/serv-toolbox/main/src/bin/serv.sh"])
        harmony_script_path.chmod(0o755)
        subprocess.run([str(harmony_script_path)])
    print_stars()
