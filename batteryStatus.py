import subprocess

PATH_TO_BATTERY_INFO = "/proc/acpi/battery/"

CHARGING_KEY = "charging state"
DISCHARGING = "discharging"


def getBatteryStatusFile():
  ls_output = subprocess.check_output(["ls", PATH_TO_BATTERY_INFO])
  files = ls_output.split()
  return PATH_TO_BATTERY_INFO + files[0] + "/state"


def parseBatteryStatusFile(statFile=None):
  batteryStatus = {}
  if not statFile:
    statFile = getBatteryStatusFile()
  with open(statFile, "r") as f:
    for line in f:
      key, value = line.split(":")[0:2]
      batteryStatus[key] = value.strip()
  return batteryStatus


def isCharging():
  batteryStatus = parseBatteryStatusFile()
  return batteryStatus[CHARGING_KEY] != DISCHARGING

if __name__ == '__main__':
  print isCharging()
