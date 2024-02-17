import os
import subprocess
import re
from colorama import Fore
from config import print_stuff, config
from shared import (
    ask_yes_no,
    process_command,
    run_command,
    set_var,
    finish_node,
    ask_for_wallet_password,
    get_bytes_address,
)

# Setup print stuff from config class print_stuff
print_whitespace = print_stuff.printWhitespace
print_stars = print_stuff().printStars
string_stars = print_stuff().stringStars
print_stars_reset = print_stuff(reset=1).printStars
string_stars_reset = print_stuff(reset=1).stringStars


def install_check() -> None:
    print_stars()
    if (
        os.path.isdir(config.serv_dir)
        and os.path.isdir(config.serv_config_dir)
        and os.path.isfile(config.serv_conf)
        and os.path.isdir(config.toolbox_location)
    ):
        # Already installed, return and run main app
        return
    else:
        # Not installed! Let's install it!
        print(f"* SERV Node is not installed at {config.serv_dir}")
        answer = ask_yes_no("* Would you like to install SERV Node now? (y/n)")
        if answer:
            # Install SERV Node
            print_stars()
            print("* Installing SERV Node")
            print_stars()
            install_serv_node()
            print(Fore.MAGENTA)
        else:
            print_stars()
            print("* Exiting SERV Node Installer")


def install_serv_node() -> None:
    if not os.path.isdir(config.serv_dir):
        os.makedirs(config.serv_dir)
        process_command(f"wget -O {config.servnode} rpc.serv.services/servnode")
        process_command(f"wget -O /tmp/genesis.json rpc.serv.services/genesis")
        process_command(f"wget -O /tmp/config.toml rpc.serv.services/config")
        process_command(f"chmod +x {config.servnode}")
        print(f"* Created {config.serv_dir} directory & files")
        # open genesis.json and config.toml to read & update
        short_name = input(
            f"* Pick a short name to identify your validator node (Example: SuperNode): "
        )
        if short_name:
            answer = ask_yes_no(
                f"* You picked {short_name} as your validator short code name, is this correct? (y/n)"
            )
            if answer:
                # Open file
                with open("/tmp/config.toml", "r") as file:
                    filedata = file.read()
                # Update settings
                filedata = filedata.replace(
                    'moniker = "Serv-0"', f'moniker = "{short_name}"'
                )
                filedata = filedata.replace('log_level = "info"', 'log_level = "warn"')
                # Save file
                with open("/tmp/config.toml", "w") as file:
                    file.write(filedata)
                # Init network
                process_command(
                    f"{config.servnode} init {short_name} --chain-id serv_43970-1"
                )
                # Move custom files
                process_command(f"mv /tmp/genesis.json {config.serv_genesis}")
                process_command(f"mv /tmp/config.toml {config.serv_conf}")
                # Update chain-id
                with open(config.serv_client, "r") as file:
                    filedata = file.read()
                filedata = filedata.replace(
                    'chain-id = ""', 'chain-id = "serv_43970-1"'
                )
        print(f"* SERV Node installed at {config.serv_dir}")
        print_stars()
        # Wallet Creation or Import
        print("* Creating/Importing SERV wallet")
        answer = ask_yes_no(
            f"* Would you like to create a wallet for your validator node? (y/n)"
        )
        if answer:
            wallet_password = ask_for_wallet_password()
            print(Fore.WHITE)
            result = run_command(
                f"yes {wallet_password} | {config.servnode} keys add {config.active_user}",
                print_output=True,
            )
            if result:
                set_address_vars(wallet_password)
                print(
                    f"{Fore.YELLOW}* Backup your mnemonic phrase above before proceeding any further. Do not give your phrase away or lose it!{Fore.MAGENTA}\n*\n"
                )
            else:
                print(
                    f"* Error creating wallet, please try again or import a wallet instead."
                )
                finish_node()

        else:
            answer = ask_yes_no(
                f"* Skipping wallet creation, would you like to import a wallet now instead? (y/n)"
            )
            if answer:
                wallet_password = ask_for_wallet_password()
                run_command(
                    f'yes {wallet_password} | {config.servnode} keys add {config.active_user} --recover --algo="eth_secp256k1"',
                    print_output=True,
                )
                set_address_vars(wallet_password)
            else:
                finish_node()
        # Service Configuration Stuff
        with open(config.servnode_service_file, "r") as file:
            filedata = file.read()
        filedata = filedata.replace("User=servuser", f"User={config.active_user}")
        filedata = filedata.replace(
            "WorkingDirectory=/home/servuser/serv",
            f"WorkingDirectory={config.serv_dir}",
        )
        filedata = filedata.replace(
            "ExecStart=/home/servuser/serv/servnode start",
            f"ExecStart={config.servnode} start",
        )
        # Save file in /tmp as we need to be sudo to move it to /etc/systemd/system
        with open("/tmp/servnode.service", "w") as file:
            file.write(filedata)
        # Move file to /etc/systemd/system
        subprocess.run(
            f"sudo mv /tmp/servnode.service /etc/systemd/system/servnode.service",
            shell=True,
            check=True,
        )
        # Enable service
        subprocess.run("sudo systemctl enable servnode.service", shell=True, check=True)
        # Start service
        subprocess.run("sudo systemctl start servnode.service", shell=True, check=True)
        result = run_command(f"{config.servnode} keys list", print_output=True)
    else:
        print(f"* {config.serv_dir} directory already exists, skipping!")


def set_address_vars(wallet_password) -> None:
    print("* Getting wallet address")
    address = run_command(
        f"yes {wallet_password} | {config.servnode} keys show {config.active_user} -a",
        print_output=False,
    )
    set_var(config.dotenv_file, "SERV_WALLET_ADDRESS", str(address))
    print("* Getting server address")
    server_address = run_command(
        f"yes {wallet_password} | {config.servnode} keys show {config.active_user} -a --bech val",
        print_output=False,
    )
    set_var(config.dotenv_file, "SERV_SERVER_ADDRESS", str(server_address))
    print("* Getting emv address")
    emv_address = get_bytes_address(str(address))
    set_var(config.dotenv_file, "SERV_EMV_ADDRESS", str(emv_address))
