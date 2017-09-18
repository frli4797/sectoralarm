# Sector Alarm Library

## Information
A simple library for Sector Alarm API written in Python 3.

The code is heavily based on this project: https://github.com/the-louie/sectoralarm

## Installation
Install with pip3
```
$ sudo pip3 install sectoralarm
```

## Code examples
### Current status
Getting the current alarm status. Returned values are 'armed', 'partialarmed' or 'disarmed'.
```python
#!/usr/bin/env python3
import sectoralarm

email = "name@example.com"
password = "SuperSecretPassword!"
site_id = "01234567"

sector_alarm = sectoralarm.connect(email, password, site_id)

current_status = sector_alarm.status()
if current_status:
    print(current_status)
```
Example output:
```
{"AlarmStatus": "disarmed"}
```
