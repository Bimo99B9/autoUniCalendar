# epiCalendar

The fork of a Python script that converts your personal SIES calendar to a csv format.

This wouldn't be necessary if Universidad de Oviedo was a well-functioning organization.

[The original repository is probably what you're looking for if you're just interested in downloading your calendar.](https://github.com/Bimo99B9/autoUniCalendar)

## Requirements

- python3
- [requests](https://pypi.org/project/requests/)

## Run

- Download [the script](https://raw.githubusercontent.com/miermontoto/epiCalendar/main/epiCalendar.py) or clone the repo (`git clone https://github.com/miermontoto/epiCalendar`).

- Run the script with your `JSESSIONID` and `oam.Flash.RENDERMAP.TOKEN` cookies as parameters.

```python
python3 epiCalendar.py 0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXX XXXXXXXXX
```
