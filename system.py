import platform
import subprocess

MAC = "darwin"
LINUX = "linux"


class UnsupportedOsException(Exception):

  def __init__(self, os):
    self.message = "AutoLock: Unsupported os %s" % os

class OsHandler(object):

  def __init__(self):
    self.os = getOS()

  def lockScreen(self):
    if self.os == LINUX:
      try:
        subprocess.check_call(["gnome-screensaver-command", "--lock"])
      except (subprocess.CalledProcessError, OSError):
       # TODO what happens is slock is not installed?
       subprocess.call(["slock"])
    elif self.os == MAC:
      try:
        subprocess.check_call(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
      except (subprocess.CalledProcessError, OSError):
         pass


def isSupportedOS(os):
  return os in [MAC, LINUX]


def getOS():
  os = platform.system().lower()
  if isSupportedOS(os):
    return os
  raise UnsupportedOsException(os)

