# 主要功能
- 输入某人的用户id，获取这个人的下面信息
    - 昵称、头像、个人简介等个人数据
    - 评论数、点赞数、转发数
    - 所有的即刻动态相关数据和图片信息
    - 输出到out目录下

# 支持平台
- macOs
- windows

# 说明
当前脚本在windows下运行需要关闭chrome应用，用于读取cookies，不然拿不到句柄

# 使用
在config.json中配置:
```
    "user_name":"", // 用户id
    "loop_count":-1, // 拉多少页的数据,-1代表拉取到没有下一页为止
    "need_pic": true // 是否需要拉帖子的图片
```
目标用户id在网页版即刻的主页中拿取，记得运行脚本之前在chrome浏览器中登录一次网页版即刻，后续将会自动获取cookie并拉取，无需额外配置

依赖:

```
browser_cookie3
```
然后运行：

```
python3 main.py
```
