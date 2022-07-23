# epiCalendar

The fork of a Python script that converts your personal SIES calendar to a csv format. Works best with EPI calendars.

## Requirements

- python3
- [requests](https://pypi.org/project/requests/)

## Usage


- Download [the script](https://raw.githubusercontent.com/miermontoto/epiCalendar/main/epiCalendar.py). (← right click, save link as)
- Run the script using python and input your `JSESSIONID` cookie.

```
> python3 epiCalendar.py
Enter JSESSIONID: 0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX
```

You can also run the script with the cookie as a parameter:
```sh
python3 epiCalendar.py 0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX
```

### Obtaining JSESSIONID

To obtain your personal and expiring `JSESSIONID`, login into SIES and press F12 (or Ctrl+Shift+I) and navigate to the "Storage" section. You should find at least two cookies. Copy the `JSESSIONID` from `/serviciosacademicos` and paste it into the script's input.

### Flags

The following flags can be provided as arguments:

- `[-h | --help]` to show the help dialog.
- `[-o | --output <filename>]` to change the name of the resulting csv file.
- `[--disable-location-parsing]` to disable location parsing specific to EPI.
- `[--disable-experimental-location-parsing]` to disable some experimental location parsing specific to EPI.
- `[--disable-class-type-parsing]` to disable class type parsing.

[epiCalendar](https://github.com/miermontoto/epiCalendar) © 2022 by [Juan Mier](https://github.com/miermontoto) is licensed under [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)
