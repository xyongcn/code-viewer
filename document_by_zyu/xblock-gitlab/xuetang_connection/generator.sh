#!/bin/bash
id=$1
username=$2
lab=$3

ip=192.168.1.62
port=22

base="/edx/var/edxapp"
out_base=$base/staticfiles/codebrowser
woboq_base=$base/woboq_codebrowser
code_base=$base/staticfiles/ucore
output_dir=$out_base/$id/ucore_lab
data_dir=$out_base/"data"
key_file=/var/www/.ssh/id_rsa_$id
api_url="https://north.cs.tsinghua.edu.cn:1986/api/users"
config_file=/var/www/.ssh/config

#username=$(echo $email | sed "s/\(\)@.*/\1/")

COMPILATION_COMMANDS=$code_base/$id/compile_commands.json

#if there is not user info on the local,initialize it
if [ ! -f $key_file ]
then
    msg=$(eval "curl -k  '$api_url/$id?private_token=Gysy4D6M1-B6sTNtyu2S'")
    result=$(echo $msg | sed "s/.*\"result\":\([a-zA-Z]*\).*/\1/")
    private_key=$(echo $msg | sed "s/.*\"private_key\":\"\(.*\)\",.*/\1/")

    if [ "$result"x = "false"x ]
    then
        exit 1
    fi

    touch $key_file
    chmod 600 $key_file
    echo -e $private_key >> $key_file
    config="Host $id\n HostName $ip\n User git\n Port $port\n IdentityFile $key_file\n\n"
    echo -e $config >>  $config_file

    cd $code_base
    mkdir -p $id/ucore_lab
    cd $code_base/$id/ucore_lab
    git init
fi

##clone code from gitlab
cd $code_base/$id/ucore_lab
cp $woboq_base/scripts/fake_compiler.sh ../
sed -i "s/\$COMPILATION_COMMANDS/\/edx\/var\/edxapp\/staticfiles\/ucore\/$id\/compile_commands.json/g" ../fake_compiler.sh

ssh-add $key_file
git remote add origin$id git@$id:$username/ucore_lab.git
git pull origin$id master


if [ -d $output_dir ]
then
    rm -r $output_dir
fi

##echo "$output_dir"
##echo "$dir_commands"
##generate compile_commands.json
sed -i "s/\$(HOSTCC)/\/edx\/var\/edxapp\/staticfiles\/ucore\/${id}\/fake_compiler.sh/g" $code_base/$id/ucore_lab/labcodes/$lab/Makefile

sed -i "s/\$(CC)/\/edx\/var\/edxapp\/staticfiles\/ucore\/${id}\/fake_compiler.sh/g" $code_base/$id/ucore_lab/labcodes/$lab/Makefile

export FORWARD_COMPILER=gcc

echo “” > $COMPILATION_COMMANDS
echo "[" > $COMPILATION_COMMANDS

$base/staticfiles/xblock-script/make.sh $id $lab

#the compile_commands have error,modify it
sed -i "s/MM/c/g" $COMPILATION_COMMANDS
sed -i "s/MT/o/g" $COMPILATION_COMMANDS

echo " { \"directory\": \".\", \"command\": \"true\", \"file\": \"/dev/null\" } ]" >> $COMPILATION_COMMANDS

sed -i "s/\/edx\/var\/edxapp\/staticfiles\/ucore\/${id}\/fake_compiler.sh/\$(HOSTCC)/g" $code_base/$id/ucore_lab/labcodes/$lab/Makefile

sed -i "s/\/edx\/var\/edxapp\/staticfiles\/ucore\/${id}\/fake_compiler.sh/\$(CC)/g" $code_base/$id/ucore_lab/labcodes/$lab/Makefile

$woboq_base/generator/codebrowser_generator -b $code_base/$id -a -o $output_dir -p $lab:$code_base/$id/ucore_lab/labcodes/$lab

$woboq_base/indexgenerator/codebrowser_indexgenerator $output_dir

if [ ! -d $data_dir ]
then
    ln -s $woboq_base/data $out_base/$id/
fi
