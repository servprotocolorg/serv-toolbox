import argparse
from config import print_stuff, config
from shared import parse_flags, loader_intro
from install import install_check

def app():
    # Clear screen, show logo
    loader_intro()

    # Check Install Stats
    install_check()
    # Install SERV Node
    
    # Run parser if flags added
    parser = argparse.ArgumentParser(description="Serv Validator Toolbox - Help Menu by EasyNode.pro")
    parse_flags(parser)
    # Run regular validator node
    

if __name__ == "__main__":
    while True:
        app()
