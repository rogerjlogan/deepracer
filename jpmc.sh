#!/usr/bin/env bash
set -e

[[ "$1" =~ ^[a-zA-Z][0-9]{6}$ ]] || { echo "Usage: jpmc.sh SID" && exit; }
[[ -f ./pcl.exe ]] ||
  { echo "Get pcl.exe file from AWS Deepracer Sandbox access instructions and put it in this directory." && exit; }

./pcl aws --sandbox-user --domain NAEAST --sid "$1" -s -p adfs
