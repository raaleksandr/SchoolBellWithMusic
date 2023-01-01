# School-Bell-With-Music
A program that rings school bells and plays music in a recess.

# General description
School bell desktop application which can both ring a bell (play sounds) and play music in a flow for certain time.
It can be used for daily schedules, events, exams and recurring schedules. This program is intended to facilitate school administration in managing the time to ring the bell for a given schedule. 
Also it is possible to turn on a music during a recess by specifying a folder. The music will be played in a time range.
The program is easily installed and needs no SQL server or anything else.

# Download
You can download a ready windows installer from the latest release [here.](https://github.com/raaleksandr/SchoolBellWithMusic/releases)
Feel free to download and complile source code at any time.

# Compatibility
The program was tested on windows, but was written with the use of QT and there is a chance to make it to work in a different operating systems.

# Documentation
## The main screen
![Main screen](https://github.com/raaleksandr/SchoolBellWithMusic/blob/main/assets/screenshot_main_window.PNG?raw=true)
Fig. 1 - the main screen

On the main screen you see the list of scheduled records and buttons to Add, Edit or Delete a record.

## The dialog for andding or editing of a record
For each schedule record you can switch between 2 modes:
1. Play single file once;
2. Play all files in folder with rotation during time (music).

### The mode 'Play single file once'
![Play single sound](https://github.com/raaleksandr/SchoolBellWithMusic/blob/main/assets/screenshot_single_sound.PNG?raw=true)
Fig. 2 - set up a schedule to play a single sound

This mode is default. You can switch to this mode at any time by choosing the option 'Play single file once'.
You need to fill following fields:
1. Description (optional) - here you can enter any text, which describes a record;
2. Start day of week - the first day of week when sound will be played;
3. End day of week - the last day of week when sound will be played;
4. Time - time of a day when the sound will be played;
5. Sound file - the file to play. You cannot enter it directly, but rather you should use the button with '...' caption to choose the file with a dialog.

Also you can preview your sound with the 'Play' button.

For example on the figure 2 the sound will be played every week from monday till friday at 9 AM.

### THe mode 'Play all files in folder with rotation during time (music)'
![Play music from folder](![image](https://user-images.githubusercontent.com/69163585/210179822-84dcb7f0-bf12-41c4-ac53-91360cb82b73.png)
)
