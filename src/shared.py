import subprocess
import os
import json
import time
import dotenv
from os import environ
from datetime import datetime, timezone
from colorama import Fore
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
    print(Fore.MAGENTA)
    print_stars()
    print("* SERV Node Management Toolbox - EasyNode.pro")
    print_stars()
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
        # Get node status
        node_status = get_node_status()

        # Display node info
        display_node_info(node_status)

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
    raise SystemExit(0)


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


def run_command(command: str, shell=True, print_output=True) -> (bool, str):
    try:
        # Use Popen for interactive commands
        process = subprocess.Popen(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output, error = process.communicate()

        if print_output:
            print(output)

        if process.returncode == 0:
            return True, output
        else:
            print(
                f"* Error executing command. Return code: {process.returncode}. Error: {error}"
            )
            return False, None

    except Exception as e:
        print(f"* Exception while executing command: {e}")
        return False, None


def get_node_status(retry_limit=3, retry_delay=2):
    for attempt in range(1, retry_limit + 1):
        try:
            command = f"{config.servnode} status"
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            if attempt < retry_limit:
                print(
                    f"* Attempt {attempt}: Command failed with return code {e.returncode}. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
            else:
                print(
                    f"* Retry limit reached. Posting failure code. Last error message: {e}"
                )
                return None


def parse_block_time(timestamp_str):
    try:
        # Parse timestamp without fractional seconds
        timestamp_without_fraction = timestamp_str.split(".")[0]
        timestamp = datetime.strptime(timestamp_without_fraction, "%Y-%m-%dT%H:%M:%S")

        # Extract and convert fractional seconds if present
        fraction_seconds_str = (
            timestamp_str.split(".")[1][:-1] if "." in timestamp_str else "0"
        )
        fraction_seconds = int(fraction_seconds_str) / 10 ** len(fraction_seconds_str)

        timestamp = timestamp.replace(microsecond=int(fraction_seconds * 1e6))

        return timestamp.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def display_node_info(node_status):
    if node_status is not None:
        sync_info = node_status.get("SyncInfo", {})
        node_info = node_status.get("NodeInfo", {})
        moniker = node_info.get("moniker", "Unknown")
        latest_block_height = sync_info.get("latest_block_height", "N/A")
        latest_block_time_str = sync_info.get("latest_block_time", "N/A")
        catching_up = sync_info.get("catching_up", False)

        # Convert the latest_block_time to a readable format
        latest_block_time = parse_block_time(latest_block_time_str)
        latest_block_time_str = (
            latest_block_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            if latest_block_time
            else "N/A"
        )

        print(f"* Current Stats For {moniker}")
        print(f"* Latest Block Height: {latest_block_height}")
        print(f"* Latest Block Time: {latest_block_time_str}")
        print(f"* Catching Up: {catching_up}")
    else:
        print("* Failed to retrieve node status.")


# check if a var exists in your .env file, unset and reset if exists to avoid bad stuff
def set_var(env_file, key_name, update_name):
    if environ.get(key_name):
        dotenv.unset_key(env_file, key_name)
    dotenv.set_key(env_file, key_name, update_name)
    load_var_file(env_file)
    return
