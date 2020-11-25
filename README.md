# utube
A simple python ncurses app to view suscribed youtube channel videos.
Doesn't use Youtube API, just basic web parsing.


## External dependencies
  *BeautifulSoup* - to parse youtube page
  *mpv* - to watch youtube video
  *youtube-dl* - to download youtube video

## usage
  Simply add the channels that you are interested in. The program runs a cron job every 12 hours to update the data. Watch or download as you like


## Installation
  1) clone the repo
  2) install BeautifulSoup
  3) run 'make' from the repo dir

## Controls

*j*   Move UP

*k*   Move Down

*l*   Enter SubMenu

*h*   Exit SubMenu

*q*   Quit Program

*g*   First item in the list

*G*   Last item in the list

*a*   To add channel
