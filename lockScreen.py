import subprocess

def lockScreen():
  subprocess.call(["gnome-screensaver-command", "--lock"])

if __name__ == '__main__':
  lockScreen()
