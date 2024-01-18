import json
import src.jike_utils as jike_utils
import time

sql_path = "https://web-api.okjike.com/api/graphql"

total_post_count = 0  # 总帖子数
has_next = True  # 是否有下一页
cur_page_count = 1  # 当前页数
loop_count = -1  # 循环次数
pic_list = [] # 图片列表
total_image_count = 0 # 图片总数
config_data = {
    "user_name":"",
    "loop_count":-1, # -1 代表一直获取直到没有下一页
    "need_pic":False # 是否需要下载图片
}

# 设置 GraphQL 查询和变量
operationName = "UserFeeds"
cookies = {}
variables = {
    "username":"wenhao1996",
}
def is_need_pic():
    return config_data["need_pic"]

# 设置请求头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/json",
    "Origin": "https://web.okjike.com",
    "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
query = "query UserFeeds($username: String!, $loadMoreKey: JSON) {\n  userProfile(username: $username) {\n    username\n    feeds(loadMoreKey: $loadMoreKey) {\n      ...BasicFeedItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasicFeedItem on FeedsConnection {\n  pageInfo {\n    loadMoreKey\n    hasNextPage\n    __typename\n  }\n  nodes {\n    ... on ReadSplitBar {\n      id\n      type\n      text\n      __typename\n    }\n    ... on MessageEssential {\n      ...FeedMessageFragment\n      __typename\n    }\n    ... on UserAction {\n      id\n      type\n      action\n      actionTime\n      ... on UserFollowAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        allTargetUsers {\n          ...TinyUserFragment\n          following\n          statsCount {\n            followedCount\n            __typename\n          }\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        __typename\n      }\n      ... on UserRespectAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        targetUsers {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        content\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FeedMessageFragment on MessageEssential {\n  ...EssentialFragment\n  ... on OriginalPost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...RootMessageFragment\n    ...UserPostFragment\n    ...MessageInfoFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...UserPostFragment\n    ...RepostFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    ...UserPostFragment\n    __typename\n  }\n  ... on OfficialMessage {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...MessageInfoFragment\n    ...RootMessageFragment\n    __typename\n  }\n  __typename\n}\n\nfragment EssentialFragment on MessageEssential {\n  id\n  type\n  content\n  shareCount\n  repostCount\n  createdAt\n  collected\n  pictures {\n    format\n    watermarkPicUrl\n    picUrl\n    thumbnailUrl\n    smallPicUrl\n    width\n    height\n    __typename\n  }\n  urlsInText {\n    url\n    originalUrl\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment LikeableFragment on LikeableMessage {\n  liked\n  likeCount\n  __typename\n}\n\nfragment CommentableFragment on CommentableMessage {\n  commentCount\n  __typename\n}\n\nfragment RootMessageFragment on RootMessage {\n  topic {\n    id\n    content\n    __typename\n  }\n  __typename\n}\n\nfragment UserPostFragment on MessageUserPost {\n  readTrackInfo\n  user {\n    ...TinyUserFragment\n    __typename\n  }\n  __typename\n}\n\nfragment TinyUserFragment on UserInfo {\n  avatarImage {\n    thumbnailUrl\n    smallPicUrl\n    picUrl\n    __typename\n  }\n  isSponsor\n  username\n  screenName\n  briefIntro\n  __typename\n}\n\nfragment MessageInfoFragment on MessageInfo {\n  video {\n    title\n    type\n    image {\n      picUrl\n      __typename\n    }\n    __typename\n  }\n  linkInfo {\n    originalLinkUrl\n    linkUrl\n    title\n    pictureUrl\n    linkIcon\n    audio {\n      title\n      type\n      image {\n        thumbnailUrl\n        picUrl\n        __typename\n      }\n      author\n      __typename\n    }\n    video {\n      title\n      type\n      image {\n        picUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RepostFragment on Repost {\n  target {\n    ...RepostTargetFragment\n    __typename\n  }\n  targetType\n  __typename\n}\n\nfragment RepostTargetFragment on RepostTarget {\n  ... on OriginalPost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    topic {\n      id\n      content\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Answer {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on OfficialMessage {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    __typename\n  }\n  ... on DeletedRepostTarget {\n    status\n    __typename\n  }\n  __typename\n}\n"

# 将查询和变量打包到一个 JSON 对象中
query_data = {
    "operationName": operationName,
    "query": query,
    "variables": variables,
}

def update_status():
    global total_post_count,has_next,cur_page_count,cookies,pic_list,total_image_count
    total_post_count = 0
    has_next = True
    cur_page_count = 1
    pic_list = []
    total_image_count = 0
    update_cookies()

def update_cookies():
    global cookies
    cookies = jike_utils.get_cookies_by_domain("okjike.com")

def get_page_node_imgs(json_obj):
    import threading
    global total_image_count
    name = jike_utils.get_display_name(json_obj)
    post_nodes = jike_utils.get_nodes_node(json_obj)
    threads = []
    # download images
    if len(post_nodes) > 0:
        for post_node in post_nodes:
            out_dir = f"out/{name}/pics/"
            img_name = f"{str(post_node['createdAt']).replace('.','_').replace(':','_').replace('-','_')}"
            import os
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            pic_node = post_node["pictures"]
            thread = threading.Thread(target=jike_utils.save_images_async, args=(pic_node, out_dir, img_name))
            thread.start()
            threads.append(thread)
            post_img_count = len(jike_utils.get_images_url_list(pic_node))
            total_image_count += post_img_count

    # 等待所有线程完成
    for thread in threads:
        thread.join()
origin_json_path = ""
content_file_path = ""
def write_json_to_file(json_obj,sql_response_json_content,is_first_page):
    write_mode = "w" if is_first_page == True else "a"
    name = jike_utils.get_display_name(json_obj)
    jike_utils.save_data_to_file(sql_response_json_content,output_dir=f"out/{name}",file_name="origin_json.txt",mode=write_mode)

# 重复拉取下一页，保存post 和 json数据，并拉取图片
def loop_thing(sql_response_json_content,json_obj,is_first_page=False):
    global total_post_count,has_next,cur_page_count,cookies,total_image_count
    print(f"start new page cur_page_count = {cur_page_count}")
    
    update_cookies()
    
    # write origin json to json file
    write_json_to_file(json_obj,sql_response_json_content,is_first_page)

    # write post to post file
    total_post_count = jike_utils.write_page_data_to_file(json_obj,total_post_count,is_first_page)
    
    # download imgs
    get_page_node_imgs(json_obj)
    
    has_next = jike_utils.has_next_page(json_obj)
    if has_next == True:
        next_page_param_key = jike_utils.get_next_page_key(json_obj)
        variables["loadMoreKey"] = {"lastId":next_page_param_key}
        query_data["variables"] = variables
    print(f"now total_post_count = {total_post_count} total_image_count = {total_image_count}\nhas_next={str(has_next)}")
    cur_page_count += 1


def get_first_page():
    response = jike_utils.get_page_data(sql_path,cookies,headers,query_data)
    sql_response_json_content = response.text
    json_obj = json.loads(sql_response_json_content)
    post_nodes = jike_utils.get_nodes_node(json_obj)
    print(f"len = {len(post_nodes)}")
    if len(post_nodes) > 0:
        all_post_text = ""
        all_post_text += "screenName: "+str(post_nodes[0]["user"]["screenName"])+"\n"
        all_post_text += "username: "+str(post_nodes[0]["user"]["username"])+"\n"
        all_post_text += "briefIntro: "+str(post_nodes[0]["user"]["briefIntro"])+"\n"
        all_post_text += "avatarImage: "+str(post_nodes[0]["user"]["avatarImage"])+"\n" 
        all_post_text += "~~~~~~~post below:\n\n"   
        loop_thing(sql_response_json_content,json_obj,is_first_page = True)
        time.sleep(1)

def start_loop():
    global has_next,loop_count
    while has_next and loop_count != 0 :
        response = jike_utils.get_page_data(sql_path,cookies,headers,query_data)
        sql_response_json_content = response.text
        json_obj = json.loads(sql_response_json_content)
        loop_thing(sql_response_json_content,json_obj)
        loop_count -= 1
        time.sleep(1)

def get_config():
    global variables,loop_count,config_data

    with open("config.json", "r") as read_file:
        config_data = json.load(read_file)
    print(config_data)
    variables["username"] = config_data["user_name"]
    # loop_count = int(input("input loop count( -1 define get all page):"))
    loop_count = config_data["loop_count"]

def run():
    get_config()
    update_status()
    get_first_page()
    start_loop()

if __name__ == '__main__':
    run()
   