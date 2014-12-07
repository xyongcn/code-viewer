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
 
参考文献
============

 * [edX Platform Developer Documentation](http://edx-developer-guide.readthedocs.org/en/latest/overview.html)
 * [x-module的列表](https://github.com/edx/edx-platform/tree/master/common/lib/xmodule/xmodule)
