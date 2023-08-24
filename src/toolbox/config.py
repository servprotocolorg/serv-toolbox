import socket, requests, json
from os import environ, path
from dotenv import load_dotenv

load_dotenv(f"{path.expanduser('~')}/.servproto.env")


def get_url(timeout=5) -> str:
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=timeout)
        response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful

        # Parse the JSON response
        ip_data = response.json()
        result = ip_data["ip"]
    except requests.exceptions.RequestException as x:
        try:
            response = requests.get("https://ident.me", timeout=timeout)
            response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
            result = response.text
        except requests.exceptions.RequestException as x:
            print(type(x), x)
            result = "0.0.0.0"
    return result


class EnvironmentVariables:
    easy_version = "1.2.3"
    server_host_name = socket.gethostname()
    user_home_dir = path.expanduser("~")
    dotenv_file = f"{user_home_dir}/.servproto.env"
    active_user = path.split(user_home_dir)[-1]
    harmony_dir = environ.get("HARMONY_DIR") or f"{user_home_dir}/harmony"
    bls_key_file = path.join(harmony_dir, "blskey.pass")
    hmy_app = path.join(harmony_dir, "hmy")
    harmony_conf = path.join(harmony_dir, "harmony.conf")
    bls_key_dir = path.join(harmony_dir, ".hmy", "blskeys")
    hmy_wallet_store = path.join(user_home_dir, ".hmy_cli", "account-keys", active_user)
    toolbox_location = path.join(user_home_dir, "harmony-toolbox")
    validator_data = path.join(toolbox_location, "metadata", "validator.json")
    password_path = path.join(harmony_dir, "passphrase.txt")
    external_ip = get_url()
    main_menu_regular = path.join(toolbox_location, "src", "messages", "regularmenu.txt")
    # Update endpoints for SERV
    rpc_endpoints = ["https://api.s0.t.hmny.io", "https://api.harmony.one", "https://rpc.ankr.com/harmony"]
    rpc_endpoints_max_connection_retries = 10
    hmy_tmp_path = "/tmp/hmy"
    harmony_tmp_path = "/tmp/harmony"
    folder_checks = ["harmony", "harmony0", "harmony1", "harmony2", "harmony3", "harmony4"]

    @staticmethod
    def get_working_endpoint(endpoints):
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    return endpoint
            except requests.exceptions.RequestException:
                pass  # We'll just move on to the next endpoint
        return None  # If we get here, none of the endpoints worked

    @property
    def working_rpc_endpoint(self):
        return self.get_working_endpoint(self.rpc_endpoints)
