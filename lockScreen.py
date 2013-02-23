import subprocess

def lockScreen():
  try:
    subprocess.check_call(["gnome-screensaver-command", "--lock"])
  # TODO there should be no need for OS error but it seems
  # to raise it when the command above is altered
  except (subprocess.CalledProcessError, OSError):
    subprocess.call(["slock"])


if __name__ == '__main__':
  lockScreen()
