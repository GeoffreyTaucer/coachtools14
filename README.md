# Coach Tools
A set of video tools for use in athletic coaching. Coach Tools takes a video feed and displays it on a user-adjustable delay. Video can also be paused, and the user can then move forward or backward frame-by-frame.

# Controls:
During video:
  -P: pause
  -M: menu
  -Arrow keys: Increase/decrease video delay length by 1 second increments
  -Q: exit program
  
 While paused:
  -P: unpause
  -Up/down: Move forward/backward by one second
  -Left/right: Move forward/backward by one frame
  
# Known issues:
This was originally written to run on a very specific set of hardware, and as such does not contain any system performance checks written into the software. As such, it may bug or crash if you don't have enough RAM, or if your processor cannot process each frame fast enough to keep up with the camera.

The application runs best on a Linux system. It works on Windows, but the display may be stretched if there is a mismatch in the aspect ratio between your monitor and your camera. It has not been tested on Mac -- in theory it should run, but there may be bugs I haven't run into yet.
