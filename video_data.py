"""
Code to save and extract video info.

functions:
    save_video_info
    get_video_info
"""
#!/usr/bin/env python3

from config import _DATA_FILE
from storage import get_data, save_data


def save_video_info(parsed_data: list) -> None:
    """Save the video info.

    arguments:
        parsed_data

    return:
        None
    """
    save_data(_DATA_FILE, parsed_data)

def get_video_info() -> list:
    """Get the video info.

    return:
        [videos info]
    """
    return get_data(_DATA_FILE)


if __name__ == '__main__':
    print(get_video_info())
