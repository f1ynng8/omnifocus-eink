# Calendar-omnifocus
## Hardware:
1. A Mac running Omnifocus
2. A Raspberry PI
3. [E-ink display module](https://www.waveshare.net/wiki/6inch_e-Paper_HAT)

## Software
1. Omnifocus running on Mac
2. An applescript running on Mac to fetch tasks from the specified perspectives of the Omnifocus
3. The applescript puts tasks into an ini file and send it via scp to Raspberry PI
4. A Python scrpit runing on Raspberry PI process the ini file and render it into a bmp file
5. The epd.so written in C is used to display the bmp file to E-ink display

![显示效果](/img/calendar-omnifocus.png)
