import subprocess

def lockScreen():
  try:
    subprocess.check_call(["gnome-screensaver-command", "--lock"])
  except (subprocess.CalledProcessError, OSError):
    subprocess.call(["slock"])


if __name__ == '__main__':
  lockScreen()
