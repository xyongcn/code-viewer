#!/bin/bash
email=$1
pub_key=$2
username=$3
passwd="password"
title="ssh key for edx(please don't change)"

base_repo_dir="/home/git/repositories"

json=$(gitlab create_user $email $passwd "{username: $username, name: $username}")


# extract the id from json
user_id=$(echo $json | sed "s/.* id | \([0-9]*\).*/\1/")

#upload the public ssh key
gitlab create_user_ssh_key $user_id "$title" "$pub_key"

#initialiize ucore
gitlab create_project "ucore" "{user_id: $user_id}"
