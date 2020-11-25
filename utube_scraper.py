#!/usr/bin/env python3

"""Library imports"""
import json
import os.path
import pickle
import requests

from bs4 import BeautifulSoup

"""FILE Names"""
_CHANNEL = f'{os.path.expanduser("~")}/.local/utube/channels.txt'
_DATA = f'{os.path.expanduser("~")}/.local/utube/data.txt'

"""Functions"""

def downloadPage(url):
    """Download the url and return its content."""
    response = requests.get(url)
    return response.content

def filterData(content):
    """Filter the html page and return only the json data containing videos info."""
    soup = BeautifulSoup(content, 'html.parser')
    script = soup.body.find_all('script')[1].string
    elem = script.strip().split('\n')[0].strip(';')
    trim = elem.index('=')
    elem = json.loads(elem[trim+1:])
    elem = elem['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
    return elem

def parseData(content):
    """Parse the json and return a list of basic video info."""
    videos = []
    for entry in content:
        video = {}
        data = entry['gridVideoRenderer']
        video['id'] = data['videoId']
        video['title'] = data['title']['runs'][0]['text']
        video['published'] = data['publishedTimeText']['simpleText']
        video['duration'] = data['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
        videos.append(video)
    return videos

def saveData(filename, data):
    """Save the data in the given filename."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def getData(filename):
    """Return data from given filename."""
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def addChannel(url):
    """Add a channel to the channels.txt."""
    channels = []
    if os.path.isfile(_CHANNEL):
        channels = getData(_CHANNEL)
    channel = url.split('/')[-2]
    if channel in channels:
        return
    channels.append(channel)
    saveData(filename, channels)

def getChannelInfo(channel):
    """Parse and return all the video info of the given channel."""
    url = f'https://www.youtube.com/c/{channel}/videos'
    content = downloadPage(url)
    filteredData = filterData(content)
    parsedData = parseData(filteredData)
    return parsedData

def storeAllChannelsInfo():
    """Store video data of every channel in data.txt."""
    channels = []
    if os.path.isfile(_CHANNEL):
        channels = getData(_CHANNEL)
    else:
        print('please add a channel to the list before starting app.')
        return
    data = {}
    for channel in channels:
        data[channel] = getChannelInfo(channel)
    saveData(_DATA, data)

if __name__ == '__main__':
    storeAllChannelsInfo()
    #data = getData(_CHANNEL)
    #print(data)
