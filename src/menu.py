import argparse
from toolbox.config import EnvironmentVariables
from toolbox.library import loader_intro, first_env_check, load_var_file
from toolbox.toolbox import safety_defaults, start_regular_node, parse_flags

load_var_file(EnvironmentVariables.dotenv_file)

def app():
    first_env_check(EnvironmentVariables.dotenv_file)
    # This section is for hard coding new settings for current users.
    safety_defaults()
    # Run parser if flags added
    parser = argparse.ArgumentParser(description="Harmony Validator Toolbox - Help Menu by EasyNode.pro")
    parse_flags(parser)
    # Run regular validator node
    start_regular_node()

if __name__ == "__main__":
    # Clear screen, show logo
    loader_intro()
    app()
