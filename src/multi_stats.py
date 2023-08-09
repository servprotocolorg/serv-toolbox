import os
from os import environ
from toolbox.config import EnvironmentVariables
from toolbox.library import (
    load_var_file,
    set_var,
    loader_intro,
    finish_node,
    refreshing_stats_message,
    set_network,
    validator_stats_output,
)

load_var_file(EnvironmentVariables.dotenv_file)

user_home = f'{os.path.expanduser("~")}'

if not environ.get("VALIDATOR_WALLET"):
    while True:
        wallet = input("* If you'd like to use stats, we need a one1 or 0x address, please input your address now: ")
        if wallet.startswith("one1") or wallet.startswith("0x"):
            # Re-enter the wallet to verify
            verify_wallet = input("* Please re-enter your wallet address for verification: ")
            if wallet == verify_wallet:
                set_var(EnvironmentVariables.dotenv_file, "VALIDATOR_WALLET", wallet)
                break
            else:
                print("The entered wallets do not match. Please try again.")
        else:
            print("Invalid wallet address. It should start with one1 or 0x. Please try again.")


set_network("t")


if __name__ == "__main__":
    loader_intro()
    refreshing_stats_message()
    validator_stats_output()
    finish_node()
