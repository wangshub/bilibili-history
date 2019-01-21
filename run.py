import os
import json
import time
from bili import bilibili

MAX_PAGE = 10000
PAGE_PER_NUM = 300
HISTORY_DIR = 'history/'


def save(data, filename):
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    with open(HISTORY_DIR+filename, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)


def get_all_bili_history(cookie_file):
    headers = bilibili.get_header(cookie_file)
    history = {'all': []}
    for page_num in range(MAX_PAGE):
        time.sleep(0.6)
        url = 'https://api.bilibili.com/x/v2/history?pn={pn}&ps={ps}&jsonp=jsonp'.format(pn=page_num, ps=PAGE_PER_NUM)
        result = bilibili.req_get(headers, url)
        print('page = {} code = {} datalen = {}'.format(page_num, result['code'], len(result['data'])))
        if len(result['data']) == 0:
            break
        history['all'].append(result)

    return history


if __name__ == '__main__':
    cookie = 'cookies.txt'
    history = get_all_bili_history(cookie)
    save(history, 'history.json')