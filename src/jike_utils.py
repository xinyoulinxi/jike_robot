
all_share_count = 0
all_repost_count = 0
all_comment_count = 0
all_like_count = 0
all_image_count = 0
def ensure_dir_exists(dir_path):
    import os
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def start_request(url, cookies,headers):
    import requests
    response = requests.post(url, cookies=cookies, headers=headers)
    html_content = ""
    
    # 检查请求是否成功
    if response.status_code == 200:
        print("request success!")
        html_content = response.text
    else:
        print(f"request error, code: {response.status_code}")
    return html_content

def get_all_item(html_content):
    import os
    import re
    import json
    def is_valid_json(json_str):
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False

    def find_nested_brackets(text):
        stack = []
        result = []
        for m in re.finditer(r'[{}]', text):
            if m.group() == '{':
                if not stack:
                    start = m.start()
                stack.append('{')
            else:
                stack.pop()
                if not stack:
                    result.append(text[start:m.end()])
        return result
    # 使用正则表达式找到所有符合要求的部分
    pattern = r'\{"id":[\s\S]*?,"__typename":[\s\S]*?\}'
    valid_json_strings = find_nested_brackets(html_content)
    # 筛选有效的 JSON 字符串
    matches = [s for s in valid_json_strings if is_valid_json(s)]
    # 确保 out 目录存在，如果不存在则创建
    output_dir = 'out'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = "out/dict.txt"
    # 对于每个匹配的部分
    out_content = ""
    for match in matches:
        out_content += match + "\n\n"
        print(f"have save into {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"size = {len(matches)}\n\n{out_content}")

def save_data_to_file(data,output_dir = "out",file_name='web_content.txt',mode="w"):
    import os
    # 确保 out 目录存在，如果不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将网页内容写入 txt 文件
    output_file = os.path.join(output_dir,file_name)
    with open(output_file, mode, encoding='utf-8') as f:
        f.write(data)

    print(f"content have output into {output_file}, mode = {mode}")

def erase_space_content(content):
    content = content.replace(" ","")
    content = content.replace("\n","")
    content = content.replace("\t","")
    content = content.replace("\r","")
    return content

def read_file_content(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def read_json_file(file_path):
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_username_by_url(url,cookie,headers):
    start_request(url,cookie,headers)

def get_cookies_by_domain(domain):
    import browser_cookie3
    r = browser_cookie3.chrome(domain_name=domain)
    return convert_cookiejar_to_requests_cookies(r)

def convert_cookiejar_to_requests_cookies(cookie_jar) -> dict:
    """
    将 CookieJar 对象转换为 requests.post 的 cookies 参数。

    Args:
        cookie_jar: CookieJar 对象。

    Returns:
        转换后的 cookies 参数。
    """
    cookies = {}
    for cookie in cookie_jar:
        cookies[cookie.name] = cookie.value
    return cookies

def get_nodes_node(response_json):
    return response_json["data"]["userProfile"]["feeds"]["nodes"]
def get_avatar_url(post_node):
    return post_node["user"]["avatarImage"]["picUrl"]

def get_display_name(response_json):
    post_nodes = response_json["data"]["userProfile"]["feeds"]["nodes"]
    return str(post_nodes[0]["user"]["screenName"])

def has_next_page(response_json):
    # print(str(response_json["data"]["userProfile"]["feeds"]["pageInfo"]["hasNextPage"]))
    return str(response_json["data"]["userProfile"]["feeds"]["pageInfo"]["hasNextPage"]) == "True"

def get_next_page_key(response_json):
    next_page_key = response_json["data"]["userProfile"]["feeds"]["pageInfo"]["loadMoreKey"]
    # print(f"next_page_id = {next_page_key}")
    return str(next_page_key["lastId"])
pic_process_count = 0
def get_images_url_list(pic_node):
    url_list = []
    if isinstance(pic_node, list):
        for url_node in pic_node:
            url = str(url_node["picUrl"])
            url_list.append(url)
    else:
        url = str(pic_node["picUrl"])
    return url_list

def get_image_path(post_node,name):
    import os
    out_dir = os.path.join("out",name,"pics")
    ensure_dir_exists(out_dir)
    img_name = f"{str(post_node['createdAt']).replace('.','_').replace(':','_').replace('-','_')}"
    return os.path.join(out_dir,img_name)

def save_images_async(pic_node,img_path):
    global pic_process_count
    # print("save_image_saync pic_node",pic_node)
    url_list = get_images_url_list(pic_node)
    image_count = len(url_list)
    index = 0
    for url in url_list:
        pic_process_count+=1
        print(f"start new image download count = {pic_process_count}")
        download_image(url, f"{img_path}_{index}.jpg")
        index+=1
    return image_count

def get_md_img_path(post_node,index):
    import os
    img_name = f"{str(post_node['createdAt']).replace('.','_').replace(':','_').replace('-','_')}"
    return f"{os.path.join('pics',img_name)}_{index}.jpg"
def get_imgs_md_content(post_node):
    pic_node = post_node["pictures"]
    image_count = len(get_images_url_list(pic_node))
    if image_count == 0:
        return ""

    if(image_count == 1):
        img_md_content = """<table width="60%">\n"""
    else:
        img_md_content = """<table width="100%">\n"""
    for i in range(image_count):
        if i % 3 == 0:  # 每行开始新的一行
            if i != 0:  # 不是第一行时关闭上一行
                img_md_content += "</tr>\n"
            img_md_content += "<tr>\n"
        # Adjust width based on number of images
        if image_count == 1:
            img_md_content += f"<td colspan='3' 'style='width: 60%; text-align: center;'><img src='{get_md_img_path(post_node, i)}'style='width: 60%; text-align: center;' alt='Image'/></td>\n"
        elif image_count == 2:
            img_md_content += f"<td style='width: 50%;'><img src='{get_md_img_path(post_node, i)}' alt='Image'/></td>\n"
        else:
            img_md_content += f"<td style='width: 33.33%;'><img src='{get_md_img_path(post_node, i)}' alt='Image'/></td>\n"
    if image_count % 3 != 0:  # 如果图片总数不是3的倍数，补齐最后一行
        img_md_content += "</tr>\n"
    img_md_content += "</table>\n"
    return img_md_content

# def get_imgs_md_content(post_node):
#     pic_node = post_node["pictures"]
#     image_count = len(get_images_url_list(pic_node))
#     if image_count == 0:
#         return ""
#     image_content = ""
#     for i in range(0, image_count):
#         image_content += f"{get_md_img_path(post_node,i)}\n"
#     return image_content

def convert_to_normal_time(time_str):
    from datetime import datetime
    datetime_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    normal_time_str = datetime_obj.strftime("%Y年%m月%d日 %H:%M:%S")
    return normal_time_str

def get_post_type(type):
    if type == "REPOST":
        return "转发"
    elif type == "ORIGINAL_POST":
        return "原创"

def write_page_data_to_file(response_json,total_post_count,is_first_page=False):
    global all_share_count,all_repost_count,all_comment_count,all_like_count,all_image_count
    # import os
    # 生成Markdown表格头部
    table_header = "| 分享数 | 转发数 | 评论数 | 点赞数 | 类型 |\n"
    table_header += "|---------|----------|-----------|--------|--------|\n"

    post_nodes = response_json["data"]["userProfile"]["feeds"]["nodes"]
    print(f"len = {len(post_nodes)}")
    # post_dir = os.path_join("out","posts")
    # ensure_dir_exists(post_dir)
    if len(post_nodes) > 0:
        all_post_text = ""
        name = get_display_name(response_json)
        for post_node in post_nodes:
            pic_node = post_node["pictures"]
            all_like_count+=int(post_node["likeCount"])
            all_image_count+= len(get_images_url_list(pic_node))
            all_comment_count+=int(post_node["commentCount"])
            all_share_count+=int(post_node["shareCount"])
            all_repost_count+=int(post_node["repostCount"])
            all_post_text += f"## {total_post_count}\n\n"
            all_post_text += "**"+convert_to_normal_time(post_node['createdAt'])+"**\n\n"
            if "topic" in post_node and post_node["topic"] != None:
                all_post_text += "**圈子: 《"+str(post_node["topic"]["content"])+"》**\n\n"
            else:
                all_post_text += "**没发表在任何圈子** \n\n"
            all_post_text += table_header
            all_post_text += f"| {post_node['shareCount']} | {post_node['repostCount']} | {post_node['commentCount']} | {post_node['likeCount']} | {get_post_type(str(post_node['type']))} | \n"
            all_post_text += "\n"+str(post_node["content"])+"\n\n"
            all_post_text += get_imgs_md_content(post_node)
            # all_post_text += "pictures: "+str(get_images_url_list(pic_node))+"\n"
            # all_post_text += "urlsInText: "+str(post_node["urlsInText"])+"\n"
            all_post_text+="\n"
            total_post_count+=1
        write_mode = "w" if is_first_page == True else "a"
        save_data_to_file(all_post_text,output_dir=f"out/{name}",file_name="all_post.md",mode = write_mode)
    print("write to file successful~")
    return total_post_count
        # print(all_post_text)

def save_image_info_to_file(url, url_path,out_path):
    with open(out_path, 'a') as file:
        file.write(f"{url},{url_path}")

def write_content_to_file(content,file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"content have output into {file_name}")
def download_image(url, save_path):
    import requests,os
    global pic_process_count
    if os.path.exists(save_path):
        print(f"download image file exist no need to download path = {save_path}")
        pic_process_count-=1
        return
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
            pic_process_count-=1
            print(f"download image from success~~ path = {save_path},remind count = {pic_process_count}")
    else:
        print(f"Failed to download image from {url}, status code: {response.status_code}")

def get_avatar_save_path(name):
    import os
    save_path = os.path.join("out",name,"pics","avatar.jpg")
    return save_path
    
def get_page_data(path,cookies,headers,data):
    import requests
    import json
    response = requests.post(path, cookies=cookies, headers=headers, data=json.dumps(data))
    # 检查请求是否成功
    if response.status_code == 200:
        print("request success!")
        return response
    else:
        print(f"request error, code: {response.status_code}")