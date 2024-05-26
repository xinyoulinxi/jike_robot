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
    with open(file_name, "r") as f:
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
            
def save_images_async(pic_node,dic,file_name):
    global pic_process_count
    # print("save_image_saync pic_node",pic_node)
    import os,time
    if not os.path.exists(dic):
        os.makedirs(dic)
    import threading
    save_path = os.path.join(dic,file_name)
    url_list = get_images_url_list(pic_node)
    image_count = len(url_list)
    index = 0
    for url in url_list:
        pic_process_count+=1
        print(f"start new image download count = {pic_process_count}")
        download_image(url, f"{save_path}_{index}.jpg")
        index+=1
    return image_count

def write_page_data_to_file(response_json,total_post_count,is_first_page=False):
    post_nodes = response_json["data"]["userProfile"]["feeds"]["nodes"]
    print(f"len = {len(post_nodes)}")
    if len(post_nodes) > 0:
        all_post_text = ""
        for post_node in post_nodes:
            pic_node = post_node["pictures"]
            all_post_text += f"index: {total_post_count}\n"
            all_post_text += "content: "+str(post_node["content"])+"\n"
            all_post_text += "createdAt: "+str(post_node["createdAt"])+"\n"
            all_post_text += "shareCount: "+str(post_node["shareCount"])+"\n"
            all_post_text += "repostCount: "+str(post_node["repostCount"])+"\n"
            all_post_text += "commentCount: "+str(post_node["commentCount"])+"\n"
            all_post_text += "likeCount: "+str(post_node["likeCount"])+"\n"
            all_post_text += "pictures: "+str(get_images_url_list(pic_node))+"\n"
            all_post_text += "urlsInText: "+str(post_node["urlsInText"])+"\n"
            all_post_text += "type: "+str(post_node["type"])+"\n"
            if "topic" in post_node:
                all_post_text += "topic: "+str(post_node["topic"])+"\n"
            all_post_text+="\n"
            total_post_count+=1
            
        name = get_display_name(response_json)
        write_mode = "w" if is_first_page == True else "a"
        save_data_to_file(all_post_text,output_dir=f"out/{name}",file_name="all_post.txt",mode = write_mode)
    print("write to file successful~")
    return total_post_count
        # print(all_post_text)

def save_image_info_to_file(url, url_path,out_path):
    with open(out_path, 'a') as file:
        file.write(f"{url},{url_path}")

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
        
def get_page_data(path,cookies,headers,data):
    import requests
    import json
    response = requests.post(path, cookies=cookies, headers=headers, data=json.dumps(data))
    # 检查请求是否成功
    if response.status_code == 200:
        print("request success!")
    else:
        print(f"request error, code: {response.status_code}")