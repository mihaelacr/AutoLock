import platform
import subprocess

MAC = "darwin"
LINUX = "linux"


PATH_TO_BATTERY_INFO_LINUX = "/proc/acpi/battery/"

CHARGING_KEY_LINUX = "charging state"
DISCHARGING_LINUX = "discharging"
DISCHARGING_MAC = "No adapter attached"

class UnsupportedOsException(Exception):

  def __init__(self, os):
    self.message = "AutoLock: Unsupported OS %s" % os

def lockScreen():
  os = getOS()
  if os == LINUX:
    try:
      subprocess.check_call(["gnome-screensaver-command", "--lock"])
    except (subprocess.CalledProcessError, OSError):
      # TODO what happens is slock is not installed?
      subprocess.call(["slock"])
  elif os == MAC:
    try:
      subprocess.check_call(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
    except (subprocess.CalledProcessError, OSError):
      pass


def parseBatteryStatusFileLinux(statFile=None):
  def getBatteryStatusFile():
    ls_output = subprocess.check_output(["ls",       PATH_TO_BATTERY_INFO_LINUX])
    files = ls_output.split()
    return PATH_TO_BATTERY_INFO_LINUX + files[0] + "/state"

  batteryStatus = {}
  if not statFile:
    statFile = getBatteryStatusFile()
  for line in open(statFile):
    key, value = line.split(":")[0:2]
    batteryStatus[key] = value.strip()
  return batteryStatus


def isCharging():
  os = getOS()
  if os == LINUX:
    batteryStatus = parseBatteryStatusFileLinux()
    return batteryStatus[CHARGING_KEY_LINUX] != DISCHARGING_LINUX
  elif os == MAC:
     batteryStatus = subprocess.check_output(["pmset", "-g", "adapter"])
     if batteryStatus.find(DISCHARGING_MAC) == -1:
       return True
     else:
       return False


def isSupportedOS(os):
  return os in [MAC, LINUX]

def getOS():
  os = platform.system().lower()
  if isSupportedOS(os):
    return os
  raise UnsupportedOsException(os)

