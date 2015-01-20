#!/bin/bash
id=$1
dir=/edx/var/edxapp/staticfiles/ucore/$id/ucore_plus/ucore
echo $dir
cd $dir
##make command
make -B ARCH=i386 defconfig
make -B
make -B sfsimg
