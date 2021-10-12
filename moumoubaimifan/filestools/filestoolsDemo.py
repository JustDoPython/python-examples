from watermarker.marker import add_mark

from filediff.diff import file_diff_compare

from curl2py.curlParseTool import curlCmdGenPyScript

# add_mark(r"D:\0.png", "学 python，看 python 技术公众号", angle=15, size=20, space=40, color='#c5094d')

# file_diff_compare(r"D:\一线城市.log", r"D:\一线城市2.log", diff_out="diff_result.html", max_width=70, numlines=0, no_browser=True)

curl_cmd = """curl 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/mancard/img/side/qrcode@2x-daf987ad02.png' \
  -H 'sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"' \
  -H 'Referer: https://www.baidu.com/' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --compressed"""
output = curlCmdGenPyScript(curl_cmd)
print(output)
