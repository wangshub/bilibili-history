import os


def read_cookies_file(filename):
    """read cookie txt file

    :param filename: (str) cookies file path
    :return: (dict) cookies
    """
    with open(filename, 'r') as fp:
        text = fp.read()
        text = text.replace(' ', '').split(';')
        cookies = {}

        for line in text:
            k, v = line.split('=')[0], line.split('=')[1]
            cookies[k] = v

        return cookies
