# coding: utf-8

import re
from os.path import splitext, basename

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def slugify(value):
    if not isinstance(value, str):
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[<>/\\:"|?*]', '-', value).strip().lower()
    return value

def date_to_string(value):
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H-%M-%S')

def parse_filename(format, tokens, url):
    disassembled = urlparse(url)
    file = basename(disassembled.path)
    file = re.sub(':(?:thumb|small|medium|large|orig)$', '', file)
    filename, ext = splitext(file)
    replaced = format.replace('%date%', slugify(date_to_string(tokens['date']))) \
        .replace('%original_date%', slugify(date_to_string(tokens['original_date']))) \
        .replace('%filename%', slugify(filename)) \
        .replace('%ext%', slugify(ext[1:]))
    for key in ['tweet_id', 'original_tweet_id', 'user_id', 'original_user_id', 'user_name', 'original_user_name', 'user_screen_name', 'original_user_screen_name', 'type']:
        if key in tokens:
            replaced = replaced.replace('%' + key + '%', slugify(tokens[key]))
    return replaced

def generate_results(data, filename_format):
    results = {
        'files': {},
        'urls': {
            'periscope': [],
            'instagram': [],
            'others': []
        },
        'text': []
    }

    for media in data['media']:
        # Text
        if media['text']:
            results['text'].append(media['text'])

        # Urls
        for url_type in media['urls']:
            for url in media['urls'][url_type]:
                results['urls'][url_type].append(url)

        # Files
        for url in media['images'] + media['videos']:
            filename = parse_filename(filename_format, media, url)
            results['files'][filename] = url

    return results
