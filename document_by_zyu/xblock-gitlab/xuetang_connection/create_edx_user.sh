#!/bin/bash

email=$1
name=$2
passwd=$3

#add edx user
cd /edx/app/edxapp/edx-platform
/edx/bin/python.edxapp ./manage.py lms --settings aws create_user -e $email -u $name -p $passwd
