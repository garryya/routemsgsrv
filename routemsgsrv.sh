#!/bin/bash

if [ "$1" == "" ]; then
    echo Please specify method: greedy or greedy2
    exit 1
fi

# 1 recipient
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["111-111-1111"]}' http://54.158.140.192:8080/$1
echo
# 10 recipient
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["650-556-6501","650-556-6502","650-556-6503","650-556-6504","650-556-6505","650-556-6506","650-556-6511","650-556-6512","650-556-6513","650-556-6514","650-556-6515","650-556-6516"]}' http://54.158.140.192:8080/$1
echo
# 16 recipient
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["650-556-6501","650-556-6502","650-556-6503","650-556-6504","650-556-6505","650-556-6506","650-556-6511","650-556-6512","650-556-6513","650-556-6514","650-556-6515","650-556-6516","650-557-6511","650-557-6512","650-557-6513","650-557-6514"]}' http://54.158.140.192:8080/$1
echo
