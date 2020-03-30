import json

# 从浏览器中复制出来的 Cookie 字符串
cookie_str = "pgv_pvid=9551991123; pac_uid=89sdjfklas; XWINDEXGREY=0; pgv_pvi=89273492834; tvfe_boss_uuid=lkjslkdf090; RK=lksdf900; ptcz=kjalsjdflkjklsjfdkljslkfdjljsdfk; ua_id=ioje9899fsndfklsdf-DKiowiekfjhsd0Dw=; h_uid=lkdlsodifsdf; mm_lang=zh_CN; ts_uid=0938450938405; mobileUV=98394jsdfjsd8sdf; \
……中间部分省略 \
 EXIV96Zg=sNOaZlBxE37T1tqbsOL/qzHBtiHUNZSxr6TMqpb8Z9k="

cookie = {}
# 遍历 cookie 信息
for cookies in cookie_str.split("; "):
    cookie_item = cookies.split("=")
    cookie[cookie_item[0]] = cookie_item[1]
# 将cookies写入到本地文件
with open('cookie.txt', "w") as file:
    #  写入文件
    file.write(json.dumps(cookie))