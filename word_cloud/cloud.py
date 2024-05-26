import re

def extract_text(data):
    # pattern = r'content: (.*?)\s+createdAt:'
    content_pattern = re.compile(r'content: (.*?)(?=createdAt:)', re.S)
    createdAt_pattern = re.compile(r'createdAt: (.*?)(?=\n\w+:)', re.S)
    content = re.findall(content_pattern, data)
    createdAt = re.findall(createdAt_pattern, data)   
    # 将 content 和 createdAt 放在同一个对象数组中
    result = [{"content": c.strip(), "createdAt": t.strip()} for c, t in zip(content, createdAt)]
    return result


def create_mask_from_image(image_path, background_color=(255, 255, 255)):
    from PIL import Image
    import numpy as np
    # 打开图片并转换为 RGBA 模式
    image = Image.open(image_path).convert("RGBA")

    # 将图片的背景颜色设置为透明
    data = np.array(image)
    red, green, blue, alpha = data.T
    white_areas = (red == background_color[0]) & (blue == background_color[1]) & (green == background_color[2])
    data[..., :-1][white_areas.T] = (0, 0, 0)
    data[..., -1][white_areas.T] = 0

    # 创建一个新的透明背景图像并将处理过的数据粘贴到其中
    new_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
    new_image.paste(Image.fromarray(data), mask=Image.fromarray(data[..., -1]))

    # 将 RGBA 图像转换为灰度图像并返回其数据作为掩码
    mask = new_image.convert("L")
    return np.array(mask)

def resize_mask_to_4k(mask):
    from PIL import Image
    import numpy as np
    # 将 NumPy 数组转换为 PIL 图像
    image = Image.fromarray(mask)

    # 将图片大小调整为 4K 分辨率（3840x2160）
    resized_image = image.resize((3840, 2160), Image.LANCZOS)

    # 返回调整大小后的掩码（NumPy 数组）
    return np.array(resized_image)

def generate_clund_image_real(content,out_dir):
    
    from os import path
    from PIL import Image
    import numpy as np
    from wordcloud import WordCloud
    # Read the whole text.
    # with open(output_file_path, 'r', encoding='utf-8') as file:
    #     file_content = file.read()
    # Generate a word cloud image
    mask = create_mask_from_image("images/bigj.png")
    big_mask = resize_mask_to_4k(mask)
    wordcloud = WordCloud(max_words=2000,background_color="#e4ca43",
                          mask=big_mask,
                        #   width=1200,height=1200,
            font_path="hei_CN_Medium.otf")
    wordcloud.generate(content)
    out_path = path.join(out_dir,"cloud.png")
    wordcloud.to_file(out_path)
    # Display the generated image:
    # the matplotlib way:
    # import matplotlib.pyplot as plt
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
    print(f"图片生成完毕,path = {out_path}")
def filter_by_year(data, year):
    # 根据输入年份筛选出为同一年的元素
    return [item for item in data if item["createdAt"].startswith(year)]

def generate_clund_image(out_dir,file_name):
    import os
    file_path = os.path.join(out_dir,file_name)
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # 调用函数并输出结果
    result_list = extract_text(file_content)
    filter_list = filter_by_year(result_list,"2023")
    # print(result_list[0:3])
    # 输出到文件
    output_file_path = os.path.join(out_dir,'output.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        index = 1
        for item in filter_list:
            output_file.write(f"{index}\n{item}" + '\n\n')
            index+=1

    print(f"content have output to {output_file_path}.")
    
    content_list = [item["content"] for item in filter_list]
    # print(content_list)
    all_content_str = ""
    for content in content_list:
        all_content_str += content + '\n'
    generate_clund_image_real(all_content_str,out_dir)

# lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(file_content)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# import re

# class PostData:
#     def __init__(self, content, other_data):
#         self.content = content
#         self.other_data = other_data

# def extract_data(data):
#     pattern = r'content: (.*?)(createdAt: (.*?))\s+'
#     matches = re.findall(pattern, data, re.DOTALL)
#     result = []

#     for match in matches:
#         content = match[0].strip()
#         other_data = match[2].strip()
#         post_object = PostData(content, other_data)
#         result.append(post_object)

#     return result

# # 读取文件
# file_path = 'Nepentheee_posts.txt'
# with open(file_path, 'r', encoding='utf-8') as file:
#     file_content = file.read()

# # 调用函数并输出结果
# result_objects = extract_data(file_content)

# # 输出到文件
# output_file_path = 'output_objects.txt'
# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     for obj in result_objects:
#         output_file.write(f"Content: {obj.content}\n date: {obj.other_data}\n\n")

# print(f"提取的对象已经写入到 {output_file_path} 中。")
