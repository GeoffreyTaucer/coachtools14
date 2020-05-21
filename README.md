# Coach Tools
A set of video tools for use in athletic coaching. Coach Tools takes a video feed and displays it on a user-adjustable delay. Video can also be paused, and the user can then move forward or backward frame-by-frame.
It also has a built-in hold timer, great for practicing yoga poses or strength holds. You can set a hold goal, and the app will play an audio cue to let you know when you've reached it.

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

The application runs best on a Linux system. It works on Windows, but the display may be stretched if there is a mismatch in the aspect ratio between your monitor and your camera. It has not been tested on Mac -- in theory it should run, but there may be bugs I haven't run into yet. I have not tested it on any mobile platform, and it most likely would not run.

# Other stuff:
If you're running on a system with an SSD, you might consider setting self.use_hard_drive = True on line 20 of app.py. This will allow a considerably longer maximum delay, since hard drives tend to offer more storage space than RAM. The app will delete all saved frames when closing.

# How to use this app, for those not familiar with python:
First, install python 3. You can get it at python.org
Second, clone the repo (green button above and to the right of this text field). If you downloaded it as a .zip, unzip it.
Open a command prompt in the folder you downloaded to and enter the following line:

```pip install -r requirements.txt```

The app should be ready to go. Depending on how everything is set up on your machine, one of the following three lines will run it:

```python3 App.py```

```py App.py```

```python App.py```

# It crashed! What should I do?
Email me at geoffreytaucer@gmail.com, with as much info as you can about what you were doing with the app leading up to the crash. If the crash opens up a terminal with a crash report, screenshot it and include it in your email.

# This is great! Is there anything I can do to support the programmer?
You can send donations via paypal to geoffreytaucer@gmail.com
