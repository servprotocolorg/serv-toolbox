#!/bin/bash
HOME_DIR=$(echo ~)

# Check if the serv-toolbox directory exists
if [ -d "$HOME_DIR/serv-toolbox" ]; then
  # If it exists, go into it and pull updates
  cd ~/serv-toolbox
  git pull --quiet > /dev/null 2>&1
else
  # If it doesn't exist, clone the repository
  git clone https://github.com/ServProtocolOrg/serv-toolbox.git ~/serv-toolbox > /dev/null 2>&1
  # Go into the new directory, we already have updates
  cd ~/serv-toolbox
fi

# Install requirements for both
pip3 install -r requirements.txt --quiet > /dev/null 2>&1

# Start toolbox, with flags if passed
python3 ~/serv-toolbox/src/app.py "$@"
