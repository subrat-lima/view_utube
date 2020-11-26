"""
Code to scrape data.

functions:
    add_channel
    get_channels

constants:
    _CHANNEL_FILE
"""
#!/usr/bin/env python3

from json import loads
from os import remove
from os.path import isfile
from gazpacho import Soup
from channel import get_channels
from config import _BASE_DIR, _DATA_FILE
from config import _CHANNEL_VIDEO_START, _CHANNEL_VIDEO_END
from storage import get_data, save_data


def scrape_page(channel_id: str) -> None:
    """Scrape for json data from the given url.

    arguments:
        url

    return:
        None
    """
    url = _CHANNEL_VIDEO_START + channel_id + _CHANNEL_VIDEO_END
    soup = Soup.get(url)
    script = soup.find('body').find('script')[1].text
    elem = script.strip().split('\n')[0].strip(';')
    elem = loads(elem[elem.index('=')+1:])
    elem = elem['contents']['twoColumnBrowseResultsRenderer']['tabs'][1][
            'tabRenderer']['content']['sectionListRenderer']['contents'][
            0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
    file_name = _BASE_DIR + channel_id + '.json'
    save_data(file_name, elem)


def filter_video_info(file_name: str) -> list:
    """Filter video info from json file.

    arguments:
        file_name

    return:
        [video_info]
    """
    json_content = get_data(file_name)
    videos_info = []
    for entry in json_content:
        video = {}
        data = entry['gridVideoRenderer']
        video['id'] = data['videoId']
        video['name'] = data['title']['runs'][0]['text']
        video['date'] = data['publishedTimeText']['simpleText']
        video['len'] = data['thumbnailOverlays'][0][
                'thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
        videos_info.append(video)
    return videos_info


def parse_channels() -> None:
    """Parse channels and save video info.

    return:
        None
    """
    channels = get_channels()
    for channel in channels:
        file_name = _BASE_DIR + channel + '.json'
        if not isfile(file_name):
            scrape_page(channel)
    video_data = {}
    for channel in channels:
        file_name = _BASE_DIR + channel + '.json'
        video_data[channel] = filter_video_info(file_name)
    save_data(_DATA_FILE, video_data)
    for channel in channels:
        file_name = _BASE_DIR + channel + '.json'
        remove(file_name)


if __name__ == '__main__':
    pass
