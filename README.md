code-viewer
===========

Code-viewer X-module for EDX

目标描述
============

开发一个EDX的X-module插件，在EDX中实现对大型源代码树的浏览功能，方便EDX的使用者进行源代码阅读和分析。即把函数调用图工具集成到EDX中。

实现思路
============

 1. 分析一个x-module的例子，了解x-module的接口；（可参考[x-module的列表](https://github.com/edx/edx-platform/tree/master/common/lib/xmodule/xmodule)）
 2. 实现从EDX的页面上获取用户信息和用户输入；
 3. 实现在EDX的页面上显示代码浏览服务器的分析结果；
 4. 实现从x-module通过web服务访问代码浏览服务器；

常用链接
========

 * [交流纪要](https://github.com/xyongcn/code-viewer/wiki/log)
 * [外部参考文献收集](https://github.com/xyongcn/code-viewer/blob/master/%E9%93%BE%E6%8E%A5%E6%95%B4%E7%90%86.md)：这个文档维护与edX部署、使用和开发相关的参考链接。

项目结果
===========
 * [edx在Ubuntu12.04 64上的部署文档](https://github.com/xyongcn/code-viewer/blob/master/%E9%83%A8%E7%BD%B2%E6%96%87%E6%A1%A3.md)：这是由张禹完成的edX实际部署过程描述。已确认是可工作的。
