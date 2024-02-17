import os
from config import print_stuff, config
from shared import finish_node, ask_yes_no, process_command

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
    if os.path.isdir(config.serv_dir) and os.path.isdir(config.serv_config_dir) and os.path.isfile(config.serv_conf) and os.path.isdir(config.toolbox_location):
        print(f"* SERV Node is already installed at {config.serv_dir}")
        return
    else:
        print(f"* SERV Node is not installed at {config.serv_dir}")
        answer = ask_yes_no("* Would you like to install SERV Node now?")
        if answer:
            # Install SERV Node
            print_stars()
            print("* Installing SERV Node")
            print_stars()
            install_serv_node()
        else:
            print_stars()
            print("* Exiting SERV Node Installer")
    print_stars()
    finish_node()
    
def install_serv_node() -> None:
    if not os.path.isdir(config.serv_dir):
        os.makedirs(config.serv_dir)
        process_command(f"wget -O {config.servnode} rpc.serv.services/servnode")
        process_command(f"wget -O /tmp/genesis.json rpc.serv.services/genesis")
        process_command(f"wget -O /tmp/config.toml rpc.serv.services/config")
        process_command(f"chmod +x {config.servnode}")
        print(f"* Created {config.serv_dir} directory & files")
        # open genesis.json and config.toml to read & update
        short_name = input(f"* Pick a short name to identify your validator node (Example: SuperNode): ")
        if short_name:
            answer = ask_yes_no(f"* You picked {short_name} as your validator short code name, is this correct?")
            if answer:
                # Open file
                with open("/tmp/config.toml", "r") as file:
                    filedata = file.read()
                # Update settings
                filedata = filedata.replace('moniker = "Serv-0"', f'moniker = "{short_name}"')
                filedata = filedata.replace('log_level = "info"', 'log_level = "warn"')
                # Save file
                with open("/tmp/config.toml", "w") as file:
                    file.write(filedata)
                # Init network
                process_command(f"{config.servnode} init {short_name} --chain-id serv_43970-1")
                # Move custom files
                process_command(f"mv /tmp/genesis.json {config.serv_genesis}")
                process_command(f"mv /tmp/config.toml {config.serv_conf}")
                with open(config.serv_client, "r") as file:
                    filedata = file.read()
                filedata = filedata.replace('chain-id = ""', 'chain-id = "serv_43970-1"')
        print(f"* SERV Node installed at {config.serv_dir}")
        print_stars()
        print("* Creating wallet")
        answer = ask_yes_no(f"* Would you like to create a wallet for your validator node?")
        if answer:
            process_command(f"{config.servnode} keys add {config.active_user}")
        else:
            print(f"* Skipping wallet creation")
            answer = ask_yes_no(f"* Would you like to import a wallet now?")
            if answer:
                process_command(f'{config.servnode} keys add {config.active_user} --recover --algo="eth_secp256k1"')
                pass
    else:
        print(f"* {config.serv_dir} directory already exists, skipping!")