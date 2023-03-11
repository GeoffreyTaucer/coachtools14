# Coach Tools
A set of video tools for use in athletic coaching. Coach Tools takes a video feed and displays it on a user-adjustable delay. Video can also be paused, and the user can then move forward or backward frame-by-frame.
It also has a built-in hold timer, great for practicing yoga poses or strength holds. You can set a hold goal, and the app will play an audio cue to let you know when you've reached it.
It requires a usb camera.

# Controls (using an NES-style USB gamepad):
During video:

```
Start: pause
Select: menu
Up/Down: Increase/decrease video delay length by 1 second
```

While paused:

```
Start: unpause
Up/Down: Move forward/backward by one second
Left/Right: Move forward/backward by one frame
```

In menu:

```
Up/down: select parameter
Left/right: adjust parameter
A: confirm
```
  
# Known issues/to-do:
This was originally written to run on a very specific set of hardware, and as such has not been thoroughly tested on with differing resource constraints. The app assumes that you have a USB camera, that the camera is correctly reporting its own framerate, and that your computer is fast enough to keep up with that framerate. At present, the built-in system checks are limited and not thoroughly-tested.

The application runs best on a Linux system. It works on Windows, but the display may be stretched if there is a mismatch in the aspect ratio between your monitor and your camera. I have not tested it on a Mac -- in theory it should run, but there may be bugs. I have not tested it on any mobile platform, and it most likely would not run.

# Other stuff:
If you're running on a system with an SSD, you might consider setting self.use_hard_drive = True on line 20 of app.py. This will allow a much longer maximum delay.

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
Email me at geoffreytaucer@gmail.com, with as much info as you can about what you were doing with the app leading up to the crash. If the crash opens up a terminal with a crash report, screenshot it and include it in your email. Make sure you mention CoachTools14 in the subject line.

# It didn't crash, and was cool and helpful! What should I do?
You can send donations via paypal to geoffreytaucer@gmail.com.
