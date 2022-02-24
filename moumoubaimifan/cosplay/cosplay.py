import requests

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Origin": "https://bbs.mihoyo.com",
        "Referer": "https://bbs.mihoyo.com/",
        "Host": "bbs-api.mihoyo.com"
    }

def request_get(url, ret_type):
    
    res = requests.get(url=url, headers=headers, timeout= 5)
    res.encoding = "utf-8"
    if ret_type == "text":
        return res.text
    elif ret_type == "image":
        return res.content
    elif ret_type == "json":
        return res.json()

def main(last_id):
    url = f"https://bbs-api.mihoyo.com/post/wapi/getForumPostList??game_id=5&gids=5&last_id={last_id}&list_type=0&page_size=20&topic_id=547"
    res_json = request_get(url, "json")
    if res_json["retcode"] == 0:
        for item in res_json["data"]["list"]:
            post_id = item["post"]["post_id"]
            detail(post_id)
                
    if res_json["data"]["last_id"] != "":
        return main(res_json["data"]["last_id"])

def detail(post_id):
    url = f"https://bbs-api.mihoyo.com/post/wapi/getPostFull?gids=5&post_id={post_id}&read=1"
    res_json = request_get(url, "json")
    if res_json["retcode"] == 0:
        image_list = res_json["data"]["post"]["image_list"]
        for img in image_list:
            img_url = img["url"]
            if (img_url.find("weigui")) < 0:
                save_image(img_url)


def save_image(image_src):
    r = requests.get(image_src)
    content = r.content
    name = image_src.split('/')[-1]
    with open('D://mhy//' + name, "wb") as f:
        f.write(content)





if __name__ == '__main__':
    main(18136074)
