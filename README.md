
# 用 Python 获取 B 站播放历史记录

最近 B 站出了一个年度报告，统计用户一年当中在 B 站上观看视频的总时长和总个数。过去一年我居然在 B 站上看了 `2600+` 个视频，总计 `251` 个小时，居然花了这么多时间，吓得我差点把 Bilibili App 卸载了...

![](https://ws1.sinaimg.cn/large/c3a916a7gy1fzfksqinlgj208i07475z.jpg)

然而我又很好奇，到底我在 B 站上都看了些什么类型  ~~小姐姐~~ 的视频，用几行 Python 代码实现了一下。

## 获取请求 Api 接口与 Cookie

实现起来非常容易，获取 cookie 模拟请求即可

1. 使用 chrome 浏览器

2. 登陆 [B 站](https://www.bilibili.com)，进入历史记录 [https://www.bilibili.com/account/history](https://www.bilibili.com/account/history) 

3. 在网页任意位置，鼠标右键 `检查`

![](https://ws1.sinaimg.cn/large/c3a916a7gy1fzfkf5qyuqj20c009g765.jpg)

4. 按照下图所示，进入 `Network` 页面，筛选框输入 `history`，对结果进行筛选，页面滚轮往下即可看到浏览过程中的历史记录请求的 `Header`

![](https://ws1.sinaimg.cn/large/c3a916a7gy1fzfkc5s8scj21ga0nok4i.jpg)

5. 将 Header 下， cookie 一行的字符串复制出来到一个 `cookies.txt` 文本里

![](https://ws1.sinaimg.cn/large/c3a916a7gy1fzfkkj1adsj20ta07ita2.jpg)

## Python 代码实现

- 伪造浏览器请求

```python
import json
import requests


def read_cookies_file(filename):
    """read cookie txt file
    :param filename: (str) cookies file path
    :return: (dict) cookies
    """
    with open(filename, 'r') as fp:
        cookies = fp.read()
        return cookies


def get_header(filename):
    cookie = read_cookies_file(filename)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/account/history',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    return headers


def req_get(headers, url):
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)
```

- 使用 cookie 模拟请求

```python
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
```

- 代码非常简单，完整代码在 [https://github.com/wangshub/bilibili-history](https://github.com/wangshub/bilibili-history)

## 存在的问题

- 本来想拿到所有的播放记录，做一些统计和预测，但是经过实测，B 站只能获取到最近 `1000` 条或者最近 `3` 个月的播放记录

- 如果想获得更多，只能做一个监测程序，不停地从接口获取数据

## 安全问题

尽量不要使用不安全的 wifi 网络，有可能会被别有用心之人获取网络请求的 Package，易泄露个人隐私。
