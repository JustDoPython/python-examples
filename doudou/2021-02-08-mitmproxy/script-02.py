def response(flow):
    text = flow.response.get_text()
    for str in ['自学 Python', '自学Python', '自学 python', '自学python']:
        text = text.replace(str, '自学 Python，请关注「Python 技术」公众号')
    flow.response.set_text(text)