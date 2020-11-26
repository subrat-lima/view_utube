"""A TUI app to watch most recent videos of selected youtube channels."""
#!/usr/bin/env python3

import curses
import locale
import os.path
import subprocess

from curses import wrapper
from utube_scraper import _DATA, _CHANNEL, getData, addChannel, storeAllChannelsInfo

locale.setlocale(locale.LC_ALL, '')

def showList(stdscr, data, current):
    """Print the list data on screen."""
    stdscr.clear()
    str_channel = 'CHANNEL'
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f'{str_channel:<{cols}}', curses.color_pair(3) | curses.A_BOLD | curses.A_STANDOUT)
    for index, item in enumerate(data):
        if index == current:
            stdscr.addstr(index+1, 0, f'{item:<{cols}}', curses.color_pair(2) | curses.A_STANDOUT | curses.A_BOLD)
        else:
            stdscr.addstr(index+1, 0, f'{item:<{cols}}', curses.color_pair(1))
    stdscr.addstr(rows - 1, 0, f'{" q: quit":<{cols/3}}{" c: show channels":<{cols/3}}{" a: add channel":<{cols/3}}', curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT)
    stdscr.refresh()

def showVideoList(stdscr, data, current):
    """Print the video list on screen."""
    stdscr.clear()
    str_time = 'Time'
    str_published = 'Published'
    str_title = 'Title'
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f'{str_time:>9} {str_published:>14}    {str_title:<{cols - 28}}', curses.color_pair(3) | curses.A_BOLD | curses.A_STANDOUT)
    for index, item in enumerate(data):
        published = item['published'].split()
        if 'Streamed' in published:
            item['published'] = " ".join(published[1:])
        if index == current:
            stdscr.addstr(index+1, 0, f'{item["duration"]:>9}  {item["published"]:>14}   {item["title"]:<{cols - 28}}', curses.color_pair(2) | curses.A_STANDOUT | curses.A_BOLD)
        else:
            stdscr.addstr(index+1, 0, f'{item["duration"]:>9}  {item["published"]:>14}   {item["title"]:<{cols - 28}}', curses.color_pair(1))
    stdscr.addstr(rows - 1, 0, f'{" q: quit":<{cols/3}}{" c: show channels":<{cols/3}}{" a: add channel":<{cols/3}}', curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT)
    stdscr.refresh()

def loadVideoList(stdscr, data):
    """Code for the video list of channel."""
    current = 0
    data_len = len(data)
    showVideoList(stdscr, data, current)

    while True:
        c = stdscr.getch()
        if c == ord('h'):
            return 0
        elif c == ord('q'):
            return 1
        elif c == ord('g'):
            current = 0
            showVideoList(stdscr, data, current)
        elif c == ord('G'):
            current = data_len - 1
            showVideoList(stdscr, data, current)
        elif c == ord('j'):
            if current < data_len - 1:
                current += 1
            showVideoList(stdscr, data, current)
        elif c == ord('k'):
            if current > 0:
                current -= 1
            showVideoList(stdscr, data, current)
        elif c == ord('l'):
            video_id = data[current]['id']
            # run the user defined script 'utube' to handle the youtube link
            subprocess.run(['ytube', f'https://www.youtube.com/watch?v={video_id}'])

def addChannelSubMenu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, f'Channel url: ', curses.color_pair(1))
    stdscr.refresh()
    url = stdscr.getstr()
    addChannel(url)

def addChannelMenu(stdscr):
    """Show the add channel menu."""
    curses.curs_set(True)
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, f'add a channel?[y/n]', curses.color_pair(1))

    while True:
        c = stdscr.getch()
        if c == ord('y'):
            addChannelSubMenu(stdscr)
        if c == ord('n'):
            break
        stdscr.addstr(0, 0, f'add a channel?[y/n]', curses.color_pair(1))


    stdscr.clear()
    curses.noecho()
    curses.curs_set(False)
    return

def showChannels(stdscr):
    """Show the list of channels."""
    channels = getData(_CHANNEL)
    channel_len = len(channels)
    current = 0
    showList(stdscr, channels, current)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            return 1
        elif c == ord('h'):
            return 0
        elif c == ord('g'):
            current = 0
            showList(stdscr, data, current)
        elif c == ord('G'):
            current = channel_len - 1
            showList(stdscr, data, current)
        elif c == ord('j'):
            if current < channel_len - 1:
                current += 1
            showList(stdscr, channels, current)
        elif c == ord('k'):
            if current > 0:
                current -= 1
            showList(stdscr, channels, current)


def main(stdscr):
    """Start the UI."""
    stdscr.clear()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    if not os.path.isfile(_CHANNEL):
        addChannelMenu(stdscr)
        return
    channels = getData(_CHANNEL)

    if not os.path.isfile(_DATA):
        stdscr.addstr(0, 0, f'Please wait, downloading data will take some time...', curses.color_pair(1))
        stdscr.refresh()
        subprocess.run(['utube-scraper.py'])
        #storeAllChannelsInfo()
    data = getData(_DATA)
    channel_len = len(channels)

    current = 0

    showList(stdscr, channels, current)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('a'):
            addChannelMenu(stdscr)
        elif c == ord('g'):
            current = 0
            showList(stdscr, data, current)
        elif c == ord('G'):
            current = channel_len - 1
            showList(stdscr, data, current)
        elif c == ord('j'):
            if current < channel_len - 1:
                current += 1
            showList(stdscr, channels, current)
        elif c == ord('k'):
            if current > 0:
                current -= 1
            showList(stdscr, channels, current)
        elif c == ord('l'):
            if loadVideoList(stdscr, data[channels[current]]) == 1:
                break
            showList(stdscr, channels, current)
        elif c == ord('r'):
            storeAllChannelsInfo()
        elif c == ord('c'):
            if showChannels(stdscr) == 1:
                break

if __name__ == '__main__':
    wrapper(main)
