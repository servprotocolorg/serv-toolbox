[![Discord Badge](https://img.shields.io/badge/chat-discord-purple?logo=discord)](https://discord.gg/Rcz5T6D9CV)
[![Stake Now Badge](https://img.shields.io/badge/stake-harmony-brightgreen)](https://bit.ly/easynode)

# SERV Toolbox by [EasyNode.PRO](http://EasyNode.PRO "EasyNode.PRO")

## Documentation

See our [guides site](https://guides.easynode.pro/serv/) for more information (Coming Soon).

## SERV Node Setup
Grab our serv.sh and run it on your fresh Ubuntu 22.04LTS server.

To grab `serv.sh` and setup requirements, run the following:

```
cd ~/ && sudo apt-get install dnsutils git python3-pip python3-dotenv unzip tmux -y && wget -O serv.sh https://raw.githubusercontent.com/ServProtocolOrg/serv-toolbox/main/src/bin/serv.sh && chmod +x serv.sh
```

Once you have the script setup on your server from now on you can simply run this to install or to launch the full toolbox:

```
./serv.sh
```

To see all of our options run:

```
./serv.sh -h
```

To see only your stats without the full toolbox:

```
./serv.sh -s
```
