from lxml import etree
import requests
import os
import logging

log_format = '%(asctime)s => %(message)s '
url = 'https://music.163.com/discover/toplist'
hd = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

download_dir = os.path.join(os.getcwd(), "download_songs/")


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def down_song_by_song_id_name(id, name):
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    url = 'http://music.163.com/song/media/outer/url?id={}.mp3'
    r = requests.get(url.format(id), headers=hd)
    is_fail = False
    try:
        with open(download_dir + name + '.mp3', 'wb') as f:
            f.write(r.content)
    except:
        is_fail = True
        logger.info("%s 下载出错" % name)
    if (not is_fail):
        logger.info("%s 下载完成" % name)


def get_topic_ids():
    r = requests.get(url, headers=hd)
    html = etree.HTML(r.text)
    nodes = html.xpath("//ul[@class='f-cb']/li")
    logger.info('{}  {}'.format('榜单 ID', '榜单名称'))
    ans = dict()
    for node in nodes:
        id = node.xpath('./@data-res-id')[0]
        name = node.xpath("./div/p[@class='name']/a/text()")[0]
        ans[id] = name
        logger.info('{}  {}'.format(id, name))
    return ans


def get_topic_songs(topic_id, topic_name):
    params = {
        'id': topic_id
    }
    r = requests.get(url, params=params, headers=hd)
    html = etree.HTML(r.text)
    nodes = html.xpath("//ul[@class='f-hide']/li")
    ans = dict()
    logger.info('{} 榜单 {} 共有歌曲 {} 首 {}'.format('*' * 10, topic_name, len(nodes), '*' * 10))
    for node in nodes:
        name = node.xpath('./a/text()')[0]
        id = node.xpath('./a/@href')[0].split('=')[1]
        ans[id] = name
        logger.info('{}  {}'.format(id, name))

    return ans


def down_song_by_topic_id(id, name):
    ans = get_topic_songs(id, name)
    logger.info('{} 开始下载「{}」榜单歌曲，共 {} 首 {}'.format('*' * 10, name, len(ans), '*' * 10))
    for id in ans:
        down_song_by_song_id_name(id, ans[id])


logger = set_logger()


def main():
    ids = get_topic_ids()
    while True:
        print('')
        logger.info('输入 Q 退出程序')
        logger.info('输入 A 下载全部榜单歌曲')
        logger.info('输入榜单 Id 下载当前榜单歌曲')

        topic_id = input('请输入：')

        if str(topic_id) == 'Q':
            break
        elif str(topic_id) == 'A':
            for id_x in ids:
                down_song_by_topic_id(id_x, ids[id_x])
        else:
            print('')
            ans = get_topic_songs(topic_id, ids[topic_id])
            print('')
            logger.info('输入 Q 退出程序')
            logger.info('输入 A 下载全部歌曲')
            logger.info('输入歌曲 Id 下载当前歌曲')
            song_id = input('请输入：')
            if str(song_id) == 'Q':
                break
            elif str(song_id) == 'A':
                down_song_by_topic_id(topic_id, ids[topic_id])
            else:
                down_song_by_song_id_name(song_id, ans[song_id])


if __name__ == "__main__":
    main()

