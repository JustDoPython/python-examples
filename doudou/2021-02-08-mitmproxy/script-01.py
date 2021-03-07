def request(flow):
    print('request url is %s' % flow.request.url)
    flow.request.url = 'http://cn.bing.com'