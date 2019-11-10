#!/bin/bash

red="\e[0;31m"
blue="\e[0;94m"
green="\e[0;32m"
off="\e[0m"

#main
echo -e "======= NITRX INSTALL ======="
echo -e "$red [$green+$red]$off Nitrx Will Be Installed In Your System";
echo -e "$red [$green+$red]$off Installing Packages ...";
pip install -r ./requirements.txt
echo -e "$red [$green+$red]$off Checking directories ..."
echo -e "$red [$green+$red]$off Installing ...";
chmod +x Nitrx.py
echo -e "$red [$green+$red]$off Tool successfully installed and will start in 5s!";
echo -e "$red [$green+$red]$off You can execute tool by typing python Nitrx.py";
sleep 5;
python Nitrx.py
