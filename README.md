# Coach Tools
A set of video tools for use in athletic coaching. Coach Tools takes a video feed and displays it on a user-adjustable delay. Video can also be paused, and the user can then move forward or backward frame-by-frame.

# Controls:
During video:

P: pause

M: menu

Arrow keys: Increase/decrease video delay length by 1 second increments

Q: exit program



While paused:

P: unpause

Up/down: Move forward/backward by one second

Left/right: Move forward/backward by one frame
  
# Known issues/to-do:
This was originally written to run on a very specific set of hardware, and as such has not been thoroughly tested on with differing resource constraints. As such, it may bug or crash if you don't have enough RAM, or if your processor cannot process each frame fast enough to keep up with the camera.

The application runs best on a Linux system. It works on Windows, but the display may be stretched if there is a mismatch in the aspect ratio between your monitor and your camera. It has not been tested on Mac -- in theory it should run, but there may be bugs I haven't run into yet.

# Other stuff:
If you're running on a system with an SSD, you might consider setting self.use_hard_drive = True on line 20 of app.py. This will allow a considerably longer maximum delay, since hard drives tend to offer more storage space than RAM. The app will delete all saved frames when closing.
