#!/usr/bin/env bash

# Install Snippy.
# pip uninstall snippy --yes
# make clean-db
# pip install . --user

# Clear existing resources.
# cd ~/snippy
# cp ~/devel/snippy/docs/release/record-asciinema.sh ../
# chmod 755 ../record-asciinema.sh
# rm -f ../snippy.cast
# sudo docker stop snippy
# sudo docker rm snippy
# rm ./*
# clear

# Disable and enable terminal linewrap
# printf '\033[?7l'
# printf '\033[?7h'

# Start recording.
# asciinema rec ../snippy.cast -c ../record-asciinema.sh

# Play recording.
# asciinema play ../snippy.cast

# Upload recording
# asciinema upload ../snippy.cast

COMMANS=(
        'snippy --help'
        'snippy search --sall .'
        'snippy import --defaults --all'
        'snippy search --sall security'
        'snippy search --sall compress'
        'snippy export -d 61014e2d1ec56a9a'
        'ls -al'
        'cat snippets.mkdn'
        "snippy search --solution --sall kafka | grep -Ev '[^\s]+:'"
        'ls -al'
        'snippy export -d 1abc5d4fe9022429'
        'ls -al'
        'snippy import -d 1abc5d4fe9022429 -f kubernetes-docker-log-driver-kafka.mkdn'
        'sudo docker run -d --net="host" --name snippy heilaaks/snippy --server-host 127.0.0.1:8080 --log-json -vv'
        'curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/"'
        'curl -s -X GET "http://127.0.0.1:8080//api/snippy/rest/uuid/1/brief"'
        'curl -v -X OPTIONS "http://127.0.0.1:8080/api/snippy/rest/snippets"'
        'curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?limit=0" -H "accept: application/vnd.api+json"'
        'curl -s -X GET "http://127.0.0.1:8080/api/snippy/rest/snippets?sall=security&limit=1" -H "accept: application/vnd.api+json"'
        'sudo docker logs snippy | head -n 5'
        'sudo docker stop snippy'
        'sudo docker rm snippy'
        'exit'
)

printf "[heilaaks@localhost snippy]$ "
sleep 1

# Run commands that are recorded.
for i in "${COMMANS[@]}"; do
        printf "${i}"
        sleep 1s
        printf "\n"
        eval ${i}
        printf "[heilaaks@localhost snippy]$ "
        sleep 2.1s
done
