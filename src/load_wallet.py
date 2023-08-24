import dotenv
from toolbox.config import EnvironmentVariables
from toolbox.library import loader_intro, set_wallet_env, ask_yes_no, print_stars, recover_wallet

if __name__ == "__main__":
    loader_intro()
    print("* Harmony ONE Validator Wallet Import")
    print_stars()
    question = ask_yes_no(
        "\n* You will directly utilize the harmony application interface"
        + "\n* We do not store any pass phrases  or data inside of our application"
        + "\n* Respond yes to recover your validator wallet via Mnemonic phrase now or say NO to create a new wallet post-install"
        + "\n* Restore an existing wallet now? (YES/NO) "
    )
    if question:
        dotenv.unset_key(EnvironmentVariables.dotenv_file, "VALIDATOR_WALLET")
        dotenv.unset_key(EnvironmentVariables.dotenv_file, "PASS_SWITCH")
        dotenv.unset_key(EnvironmentVariables.dotenv_file, "NODE_WALLET")
        recover_wallet()
        set_wallet_env()
