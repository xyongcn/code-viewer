使用woboq生成ucore浏览页面：
======

前言
======
ucore需要json格式的完整的编译命令方可确定各模块之间的关系

默认使用cmake方式,

使用cmake方式时使用下述命令即可在当前目录生成compile_commands.json,省略第一步

  cmake . -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

当使用其他方式(make,qmake等),其提供了一个脚本来写入compile_commands.json

脚本位置:  /home/zyu/woboq_codebrowser/scripts/fake_compiler.sh

1)生成compile_commands.json
======
1.1)输出所需的环境变量
>
>  export COMPILATION_COMMANDS=/home/zyu/woboq_codebrowser/compile_commands.json
>
>  export FORWARD_COMPILER=gcc

>ucore的Makefile已固定使用gcc,需要将编译器变量修改为提供的脚本
>将
>
>TARGET_CC := $(CROSS_COMPILE)gcc
>
>改为TARGET_CC := /home/zyu/woboq_codebrowser/scripts/fake_compiler.sh
>
>(应可使用环境变量,但不知道什么原因环境变量无效，暂时直接改成路径，待修改)

1.2)开始写入json文件:
>
>  echo "[" > $COMPILATION_COMMANDS
>
>(以下为ucore的make命令)

>  cd ucore
>
>  make ARCH=i386 defconfig

>  make

>  make sfsimg

>  echo " { \"directory\": \".\", \"command\": \"true\", \"file\": \"/dev/null\" } ]" >>$COMPILATION_COMMANDS

>至此compile_commands.json写入完成



2)使用生成器生成静态页面
======
  ./generator/codebrowser_generator -b $PWD -a -o ~/codebrowser/output -p ucore_plus:/home/zyu/ucore_plus

  ./indexgenerator/codebrowser_indexgenerator ~/codebrowser/output

将静态数据链入公共文件

  ln -s /home/zyu/woboq_codebrowser/data /home/zyu/codebrowser/

(具体参数选项请参考[woboq的github链接](https://github.com/woboq/woboq_codebrowser))

注:由于woboq根据make命令来确定关系,ucore中未参与构建的文件(即独立于项目的文件)将不予显示
