#!/usr/bin/env python3

import curses
import locale
import subprocess

from curses import wrapper
from utube-scraper import _DATA, _CHANNEL, getData

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
#stdscr = curses.initscr()

def showList(stdscr, data, current):
    """Print the list data on screen."""
    stdscr.clear()
    for index, item in enumerate(data):
        if index == current:
            stdscr.addstr(index, 0, f' {item} ', curses.color_pair(2) | curses.A_STANDOUT | curses.A_BOLD)
        else:
            stdscr.addstr(index, 0, f' {item} ', curses.color_pair(1))
    stdscr.refresh()

def showVideoList(stdscr, data, current):
    """Print the video list on screen."""
    stdscr.clear()
    stdscr.addstr(0, 0, f'     Time  Title', curses.color_pair(2) | curses.A_BOLD)
    for index, item in enumerate(data):
        if index == current:
            stdscr.addstr(index+1, 0, f' {item["duration"]:>8}  {item["title"]} {item["published"]} ', curses.color_pair(2) | curses.A_STANDOUT | curses.A_BOLD)
        else:
            stdscr.addstr(index+1, 0, f' {item["duration"]:>8}  {item["title"]} {item["published"]} ', curses.color_pair(1))
    stdscr.refresh()

def loadVideoList(stdscr, data):
    """Code for the video list of channel."""
    current = 0
    data_len = len(data)
    showVideoList(stdscr, data, current)

    while True:
        c = stdscr.getch()
        if c == ord('h') or c == ord('q'):
            return
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

def main(stdscr):
    """Start the UI."""
    stdscr.clear()
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    channels = getData(_CHANNEL)
    data = getData(_DATA)
    channel_len = len(channels)

    current = 0

    showList(stdscr, channels, current)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        elif c == ord('j'):
            if current < channel_len - 1:
                current += 1
            showList(stdscr, channels, current)
        elif c == ord('k'):
            if current > 0:
                current -= 1
            showList(stdscr, channels, current)
        elif c == ord('l'):
            loadVideoList(stdscr, data[channels[current]])
            showList(stdscr, channels, current)

if __name__ == '__main__':
    wrapper(main)
