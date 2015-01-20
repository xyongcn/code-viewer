function button_fullscreen() {
  var frame = document.getElementById("codeview");
  if (frame.requestFullscreen) {
    frame.requestFullscreen();
  } 
  else if (frame.mozRequestFullScreen) {
    frame.mozRequestFullScreen();
  } 
  else if (frame.webkitRequestFullscreen) {
    frame.webkitRequestFullscreen();
  }
}
