import os
import subprocess
from colorama import Fore
from config import print_stuff, config
from shared import (
    ask_for_wallet_password,
    ask_yes_no,
    process_command,
    run_command,
    run_command_and_return_output,
    finish_node,
    set_address_vars,
    validate_env_var,
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
        # SERV Already installed, check for/collect variables, check for cosmovisor and return
        serv_wallet_address = os.environ.get("SERV_WALLET_ADDRESS")
        serv_server_address = os.environ.get("SERV_SERVER_ADDRESS")
        serv_evm_address = os.environ.get("SERV_EVM_ADDRESS")

        if not all(
            validate_env_var(var)
            for var in [serv_wallet_address, serv_server_address, serv_evm_address]
        ):
            print_stars()
            print(
                f"* Missing or invalid values for SERV_WALLET_ADDRESS, SERV_SERVER_ADDRESS, or SERV_EVM_ADDRESS in {config.dotenv_file}\n* We need to collect your information to run the toolbox properly.\n* Please enter your wallet password below to continue."
            )
            wallet_password = ask_for_wallet_password()
            set_address_vars(wallet_password)
            print_stars()
        return
    else:
        # Not installed! Let's install it!
        start_serv_install()


def start_serv_install() -> None:
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
        process_command(f"wget -O {config.genesis_tmp_path} rpc.serv.services/genesis")
        process_command(f"wget -O {config.config_tmp_path} rpc.serv.services/config")
        
        process_command(f"chmod +x {config.servnode}")
        print(f"* Created {config.serv_dir} directory & files")
        # open genesis.json and config.toml to read & update
        get_short_name()
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
                print(
                    f"{Fore.YELLOW}* Backup your mnemonic phrase above before proceeding any further. Do not give your phrase away or lose it!{Fore.MAGENTA}\n*\n"
                )
                set_address_vars(wallet_password)
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
                print(
                    "* Recovering wallet from mnemonic phrase, input your info below directly into servnode (we do not store or see your info)\n* Please enter your mnemonic below for recovery & re-enter the wallet password used previously as the keyring phrase:\n*"
                )
                run_command(
                    f"{config.servnode} keys add {config.active_user} --recover",
                    print_output=True,
                )
                set_address_vars(wallet_password)
            else:
                finish_node()
        # Service Configuration Stuff
        with open(config.servnode_service_file, "r") as file:
            filedata = file.read()
        if config.active_user == "root":
            filedata = filedata.replace("User=servuser", "User=root")
            filedata = filedata.replace(
                "WorkingDirectory=/home/servuser/serv",
                f"WorkingDirectory={config.serv_dir}",
            )
        else:
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
        result = run_command_and_return_output(
            f"yes {wallet_password} | {config.servnode} keys list"
        )
    else:
        print(f"* {config.serv_dir} directory already exists, skipping!")


def get_short_name() -> None:
    while True:
        short_name = input(
            f"* Pick a short name to identify your validator node (Example: SuperNode): "
        )
        if not short_name:
            print("* Please enter a non-empty short name.")
            continue

        answer = ask_yes_no(
            f"* You picked {short_name} as your validator short code name, is this correct? (y/n)"
        )

        if answer:
            setup_files(short_name)
            break  # Exit the loop if everything is successful
        else:
            print("* Please pick a different short name.")


def setup_files(short_name) -> None:
    # Open file
    with open(config.config_tmp_path, "r") as file:
        filedata = file.read()
    # Update settings
    filedata = filedata.replace('moniker = "Serv-0"', f'moniker = "{short_name}"')
    filedata = filedata.replace('log_level = "info"', 'log_level = "warn"')
    # Save file
    with open(config.config_tmp_path, "w") as file:
        file.write(filedata)
    # Init network
    process_command(f"{config.servnode} init {short_name} --chain-id serv_43970-1")
    # Move custom files
    process_command(f"mv {config.genesis_tmp_path} {config.serv_genesis}")
    process_command(f"mv {config.config_tmp_path} {config.serv_conf}")
    # Update chain-id
    with open(config.serv_client, "r") as file:
        filedata = file.read()
    filedata = filedata.replace('chain-id = ""', 'chain-id = "serv_43970-1"')
    return


def cosmovisor_check() -> None:
    cosmovisor_dir = os.path.join(config.serv_dir, "cosmovisor")
    if os.path.isdir(cosmovisor_dir) and os.path.isfile(os.path.join(cosmovisor_dir, "cosmovisor")):
        # Cosmovisor already installed, return
        print("* Cosmovisor is already installed.")
        return
    else:
        # Not installed! Let's install it!
        print("* Cosmovisor is not installed. Starting installation...")
        install_cosmovisor()

def install_cosmovisor() -> None:
    cosmovisor_dir = os.path.join(config.serv_dir, "cosmovisor")
    if not os.path.isdir(cosmovisor_dir):
        os.makedirs(cosmovisor_dir)
        process_command(f"wget -O {cosmovisor_dir}/cosmovisor https://github.com/cosmos/cosmos-sdk/releases/download/v0.42.9/cosmovisor_{platform}_{arch}")
        process_command(f"chmod +x {cosmovisor_dir}/cosmovisor")
        print(f"* Created {cosmovisor_dir} directory & files")
    os.environ["DAEMON_HOME"] = config.serv_dir
    os.environ["DAEMON_NAME"] = "servnode"
    os.environ["DAEMON_ALLOW_DOWNLOAD_BINARIES"] = "true"
    os.environ["DAEMON_RESTART_AFTER_UPGRADE"] = "true"
    result = run_command(f"{cosmovisor_dir}/cosmovisor version", print_output=True)
    if result:
        print("* Cosmovisor installed successfully")
    else:
        print("* Error installing Cosmovisor, please try again")