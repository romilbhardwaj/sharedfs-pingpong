# sharedfs-pingpong

A simple utility to demo the power of sky.Storage.

This program implements coordination between two processes using a shared file
that they can access. The first process is called ping, and the second is pong
The ping process writes to the file, and the pong process reads from the file
Pong then writes to the file, and ping reads from the file. This continues
indefinitely until the user presses Ctrl-C.

Usage:
```
  python main.py --process-id 0 --shared-path /tmp/ --num-processes 2
  
  # In a new shell
  python main.py --process-id 1 --shared-path /tmp/ --num-processes 2
```