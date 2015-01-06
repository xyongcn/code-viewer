iframe全屏模式切换
======
1.在xblock的/static/js/src/codebrowser_view.js中的点击事件中添加如下代码

    var frame = document.getElementById("myvideo");
    if (frame.requestFullscreen) {
        frame.requestFullscreen();
    } else if (frame.mozRequestFullScreen) {
        frame.mozRequestFullScreen();
    } else if (frame.webkitRequestFullscreen) {
        frame.webkitRequestFullscreen();
    }




2.该全屏函数的浏览器支持如下

| 特性            | Chrome        | Firefox (Gecko)  | Internet Explorer  | Opera         | Safari    |
| --------------- |:-------------:| ----------------:|:------------------:|:-------------:| ---------:|
|基本支持属性     |15 -webkit     |9.0 (9.0) -moz    |?                   |12.10          |5.0 -webkit|
|fullscreenEnabled|20 -webkit     |10.0 (10.0) -moz  |?                   |12.10          |5.1 -webkit|


3.[参考链接](https://developer.mozilla.org/zh-CN/docs/DOM/Using_fullscreen_mode)
