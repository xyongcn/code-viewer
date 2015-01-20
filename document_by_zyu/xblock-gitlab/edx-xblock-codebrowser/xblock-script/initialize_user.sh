#!/bin/bash
id=$1
email=$2
ip=192.168.1.62
port=22
root=/var/www
base_dir=/edx/var/edxapp/staticfiles
key_file=$root/.ssh/id_rsa_$id
config_file=$root/.ssh/config


if [ ! -f $key_file ]
then
    ssh-keygen -b 2048 -t rsa -C $email -f $key_file -q -N ""

    pub_key=$(eval "cat ${key_file}'.pub'")

    #extract username from email
    username=$(echo $email | sed "s/\(\)@.*/\1/")

    $base_dir/xblock-script/initialize_user.exp  $email "$pub_key" $username

    #initialize ssh config file and add ucore project to new user
    config="Host $id\n HostName $ip\n User git\n Port $port\n IdentityFile $key_file\n\n"
    echo -e $config >>  $config_file
 
    cd $base_dir/ucore
    mkdir $id
    cp -r $root/ucore_plus $base_dir/ucore/$id/

    cd $base_dir/ucore/$id/ucore_plus
    ssh-add $key_file

    git remote remove origin$id

    git remote add origin$id git@$id:$username/ucore.git

    sleep 1
    git push -u origin$id master
fi
