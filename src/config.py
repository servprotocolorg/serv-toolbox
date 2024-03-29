import socket, requests, json
from os import environ, path
from dotenv import load_dotenv
from colorama import Fore, Back, Style


def get_url(timeout=5) -> str:
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=timeout)
        response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful

        # Parse the JSON response
        ip_data = response.json()
        result = ip_data["ip"]
    except requests.exceptions.RequestException:
        try:
            response = requests.get("https://ident.me", timeout=timeout)
            response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
            result = response.text
        except requests.exceptions.RequestException as x:
            print(type(x), x)
            result = "0.0.0.0"
    return result


class print_stuff:
    def __init__(self, reset: int = 0):
        self.reset = reset
        self.print_stars = f"{Fore.MAGENTA}*" * 93
        self.reset_stars = self.print_stars + Style.RESET_ALL

    def printStars(self) -> None:
        p = self.print_stars
        if self.reset:
            p = self.reset_stars
        print(p)

    def stringStars(self) -> str:
        p = self.print_stars
        if self.reset:
            p = self.reset_stars
        return p

    @classmethod
    def printWhitespace(self) -> None:
        print("\n" * 8)


class Config:
    def __init__(self):
        self.easy_version = "1.0.0"
        self.server_host_name = socket.gethostname()
        self.user_home_dir = path.expanduser("~")
        self.dotenv_file = f"{self.user_home_dir}/.servvars.env"
        self.active_user = path.split(self.user_home_dir)[-1]
        self.serv_dir = path.join(self.user_home_dir, "serv")
        self.servnode = path.join(self.serv_dir, "servnode")
        self.serv_config_dir = path.join(self.user_home_dir, ".serv", "config")
        self.serv_conf = path.join(self.serv_config_dir, "config.toml")
        self.serv_client = path.join(self.serv_config_dir, "client.toml")
        self.serv_genesis = path.join(self.serv_config_dir, "genesis.json")
        self.priv_validator_key = path.join(
            self.serv_config_dir, "priv_validator_key.json"
        )
        self.toolbox_location = path.join(self.user_home_dir, "serv-toolbox")
        self.password_path = path.join(self.serv_dir, "passphrase.txt")
        self.servnode_service_file = path.join(
            self.toolbox_location, "src", "bin", "servnode.service"
        )
        self.external_ip = get_url()
        self.rpc_endpoints = ["https://rpc.serv.service"]
        self.rpc_endpoints_max_connection_retries = 10
        self.servnode_tmp_path = "/tmp/servnode"
        self.genesis_tmp_path = "/tmp/genesis.json"
        self.config_tmp_path = "/tmp/config.toml"

    def validate(self):
        essential_vars = [
            "easy_version",
            "server_host_name",
            "user_home_dir",
            "dotenv_file",
            "active_user",
            "serv_dir",
            "servnode",
            "serv_config_dir",
            "serv_conf",
            "serv_client",
            "serv_genesis",
            "priv_validator_key",
            "toolbox_location",
            "password_path",
            "servnode_service_file",
            "external_ip",
            "rpc_endpoints",
            "rpc_endpoints_max_connection_retries",
            "servnode_tmp_path",
            "genesis_tmp_path",
            "config_tmp_path",
        ]
        for var in essential_vars:
            if not getattr(self, var):
                raise ValueError(f"Environment variable {var} is not set!")


# Usage
config = Config()
config.validate()
