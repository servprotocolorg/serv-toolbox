import argparse
from config import print_stuff, config
from shared import (
    parse_flags,
    loader_intro,
    load_var_file,
    get_node_status,
    display_node_info,
    finish_node,
)
from install import install_check


def app():
    # Load env
    load_var_file(config.dotenv_file)

    # Run parser if flags added
    parser = argparse.ArgumentParser(
        description="SERV Validator Toolbox - Help Menu by EasyNode.pro"
    )
    parse_flags(parser)

    # Clear screen, show logo
    loader_intro()

    # Check Installation Status
    install_check()

    # Run stats cause why not atm?
    # Get node status
    node_status = get_node_status()

    # Display node info
    display_node_info(node_status)

    # Goodbye for now!
    finish_node()


if __name__ == "__main__":
    app()
