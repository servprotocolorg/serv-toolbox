import subprocess
import os
from dotenv import load_dotenv
from config import print_stuff, config
from typing import Tuple

# Setup print stuff from config class print_stuff
print_whitespace = print_stuff.printWhitespace
print_stars = print_stuff().printStars
string_stars = print_stuff().stringStars
print_stars_reset = print_stuff(reset=1).printStars
string_stars_reset = print_stuff(reset=1).stringStars


def load_var_file(var_file):
    # load .env file or create it if it doesn't exist
    if os.path.exists(var_file):
        load_dotenv(var_file, override=True)
        return True
    else:
        subprocess.run(["touch", var_file])
        return False


def parse_flags(parser):
    # Add the arguments
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Will update and/or restart your SERV Node.",
    )

    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Run your stats if SERV is installed and running.",
    )

    parser.add_argument(
        "-c",
        "--claim",
        action="store_true",
        help="Claim all of your pending Unclaimed SERV.",
    )

    parser.add_argument(
        "--installer",
        action="store_true",
        help="Will run the toolbox installer setup for mainnet or testnet.",
    )

    parser.add_argument(
        "--register",
        action="store_true",
        help="Will register your validator on chain after server is synced and deposit is made.",
    )

    # parse the arguments
    args = parser.parse_args()

    # Add other args here
    if args.claim:
        # We'll do something here soon!
        finish_node()

    if args.installer:
        # We'll do something here soon!
        finish_node()

    if args.register:
        # We'll do something here soon!
        finish_node()

    if args.stats:
        status_command = f"{config.servnode} status | jq -r '.SyncInfo | \"Latest Block: \(.latest_block_height) Block Time: \(.latest_block_time | strptime(\"%Y-%m-%dT%H:%M:%S%Z\") | strftime(\"%Y-%m-%d %H:%M:%S\")) Catching Up: \(.catching_up)'"
        process_command(status_command)
        finish_node()

    if args.update:
        # We'll do something here soon!
        finish_node()

    return


# loader intro splash screen
def loader_intro():
    print_stars()
    p = """*
*
* ███████╗███████╗██████╗ ██╗   ██╗                           
* ██╔════╝██╔════╝██╔══██╗██║   ██║                           
* ███████╗█████╗  ██████╔╝██║   ██║                           
* ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝                           
* ███████║███████╗██║  ██║ ╚████╔╝                            
* ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝                             
*                                                             
* ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗
* ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝
*    ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝ 
*    ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗ 
*    ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
*    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
*
*     SERV Node Management
*     created by Patrick @ https://EasyNode.pro
*
*"""
    print(p)
    return


def finish_node() -> None:
    print_stars()
    print("* Goodbye!")
    print_stars()
    return


def ask_yes_no(question: str) -> bool:
    yes_no_answer = ""
    while not yes_no_answer.startswith(("Y", "N")):
        yes_no_answer = input(f"{question}: ").upper()
    if yes_no_answer.startswith("Y"):
        return True
    return False


def process_command(command: str, shell=True, print_output=True) -> Tuple[bool, str]:
    result = subprocess.run(
        command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Command was successful
    if result.returncode == 0:
        if print_output and result.stdout:
            print(result.stdout)
        return True, result.stdout

    # Command failed
    if print_output:
        print(f"Error executing command: {result.stderr}")
    return False, result.stderr


def run_command(command: str, shell=True, print_output=True) -> bool:
    try:
        if print_output:
            subprocess.run(command, shell=shell, check=True)
        else:
            # Suppress the output if print_output is set to False
            with open(os.devnull, "w") as fnull:
                subprocess.run(
                    command, shell=shell, check=True, stdout=fnull, stderr=fnull
                )
        return True
    except subprocess.CalledProcessError as e:
        if print_output:
            print(f"Error executing command: {e}")
        return False
