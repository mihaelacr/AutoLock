
BATTERY_STATUS_FILE = "/proc/acpi/battery/BAT0/state"

CHARGING_KEY = "charging state"
DISCHARGING = "discharging"


def parseBatteryStatusFile(statFile=None):
  batteryStatus = {}
  if not statFile:
    statFile = BATTERY_STATUS_FILE
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
