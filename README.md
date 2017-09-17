# Sector Alarm Library

## Information
A simple library for Sector Alarm.

## Installation
Install with pip
```
$ sudo pip install sectoralarm
```

## Code examples
### Current status
Getting the current alarm status
```python
#!/usr/bin/env python
import sectoralarm

email = "name@example.com"
password = "SuperSecretPassword!"
site_id = "01234567"

sector_alarm = sectoralarm.connect(email, password, site_id)

current_status = sector_alarm.status()
if current_status:
    print("Status: %d W" % current_status)
```
Example output:
```
Status: Armed
```