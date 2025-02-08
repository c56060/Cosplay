import os
import re

# 假设项目根目录为当前工作目录，后续路径基于此相对路径设置
# 图片文件夹路径，相对于项目根目录
image_folder = "预览图"
# 名称文本文件路径，相对于项目根目录
name_file = "名称文件/名称.txt"
# 输出网页文件存放路径，相对于项目根目录，修改为当前目录
output_folder = "."
# 详细目录文件夹路径，相对于项目根目录
detail_folder = "详细目录"
# 子网页文件夹路径，相对于项目根目录，修改为当前目录
subpage_folder = "."
# 背景图片路径，相对于项目根目录
background_image_path = "网页素材/背景.jpg"
# 图标文件路径，相对于项目根目录
favicon_path = "网页素材/图标-10种尺寸.ico"

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# 如果子网页文件夹不存在，则创建
if not os.path.exists(subpage_folder):
    os.makedirs(subpage_folder)

# 获取所有图片文件名
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpeg')])

# 读取名称文件
with open(name_file, 'r', encoding='utf-8') as file:
    names = file.read().splitlines()

# 确保图片文件数量和名称数量一致
if len(image_files) != len(names):
    raise ValueError("图片文件数量和名称数量不一致，请检查！")

# 获取详细目录中的TXT文件列表，并按文件名中的数字排序
detail_files = sorted(
    [f for f in os.listdir(detail_folder) if f.endswith('.txt')],
    key=lambda x: int(re.match(r'(\d+)', x).group(1))
)

# 创建子网页HTML文件
subpage_titles = []
for detail_file in detail_files:
    # 获取TXT文件的名称（不包括扩展名）
    subpage_title = os.path.splitext(detail_file)[0]
    subpage_titles.append(subpage_title)
    # 读取TXT文件内容
    txt_file_path = os.path.join(detail_folder, detail_file)
    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        detail_content = txt_file.read()

    # 创建子网页HTML文件
    subpage_file_path = os.path.join(subpage_folder, f"{subpage_title}.html")
    with open(subpage_file_path, "w", encoding="utf-8") as subpage_file:
        subpage_file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>详细信息 - {subpage_title}</title>
            <link rel="icon" href="{favicon_path}" type="image/x-icon">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-image: url('{background_image_path}');
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
               .content {{
                    margin: 20px;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <h1>{subpage_title}</h1>
                <p>详细内容：</p>
                <pre>{detail_content}</pre>
            </div>
        </body>
        </html>
        """)

# 生成主页面HTML代码
html_code = ""
for index, (image_file, name) in enumerate(zip(image_files, names), start=1):
    # 格式化编号为三位数（例如：001, 002,..., 450）
    formatted_index = f"{index:03d}"
    # 在编号前添加 NO:
    numbered_caption = f"NO:{formatted_index}"
    # 创建跳转链接，确保每个图片链接到正确的子页面
    subpage_link = f"{subpage_titles[index - 1]}.html" if index - 1 < len(subpage_titles) else "#"
    html_code += f"""
    <div class="image-item" id="image-{index}">
        <a href="{subpage_link}" target="_blank">
            <img src="{image_folder}/{image_file}" alt="{name}">
        </a>
        <div class="caption-number">{numbered_caption}</div>
        <div class="caption-name">{name}</div>
    </div>
    """
    # 每4张图片换一行
    if index % 4 == 0:
        html_code += "<div class='row-break'></div>"

# 将生成的HTML代码保存到文件，修改主网页名称为 mulu.html
output_file = os.path.join(output_folder, "mulu.html")
with open(output_file, "w", encoding="utf-8") as file:
    file.write(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cosplay目录</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
        <style>
            body {{
                background-image: url('{background_image_path}');
                background-size: cover; /* 使背景图片覆盖整个页面 */
                background-repeat: no-repeat; /* 不重复显示背景图片 */
                background-attachment: fixed; /* 固定背景图片，不随页面滚动 */
                position: relative; /* 为左上角文本定位做准备 */
            }}
           .gallery {{
                max-width: 1200px; /* 设置最大宽度 */
                margin: 0 auto; /* 居中显示 */
                padding: 20px; /* 为两边添加空白区域 */
                box-sizing: border-box; /* 包含内边距和边框在宽度内 */
            }}
           .image-item {{
                display: inline-block;
                width: calc(24.5% - 2px);
                margin: 0;
                position: relative;
                text-align: center;
                overflow: hidden;
                box-sizing: border-box;
                border: 1px solid transparent;
            }}
           .image-item img {{
                width: 100%;
                height: auto;
                border-radius: 15px;
                vertical-align: bottom;
                border: 0px solid white;
                box-sizing: border-box;
            }}
           .caption-number {{
                position: absolute;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                color: #FF0000;
                font-weight: bold;
                font-size: 26px;
                font-family: 'KaiTi', serif;
                background-color: rgba(0, 0, 0, 0.0);
                padding: 5px;
                border-radius: 5px;
                text-shadow: 
                    -1px -1px 0 #FFFFFF,  
                     1px -1px 0 #FFFFFF,
                    -1px  1px 0 #FFFFFF,
                     1px  1px 0 #FFFFFF;
                white-space: nowrap;
                letter - spacing: -2px; /* 减小字符间距，可根据需要调整 */
            }}
           .caption-name {{
                position: absolute;
                bottom: 5px;
                left: 50%;
                transform: translateX(-50%);
                color: black;
                font-weight: bold;
                font-size: 18px;
                font-family: 'KaiTi', serif;
                background-color: rgba(200, 200, 200, 0.88);
                padding: 3px;
                border-radius: 5px;
                white-space: nowrap;
            }}
           .row-break {{
                clear: both;
            }}
            /* 使用 Flexbox 布局调整搜索框和按钮的位置 */
           .search-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center; /* 添加文本居中属性 */
                margin-bottom: 20px;
            }}
            #search-input {{
                width: 300px;
                height: 30px;
                margin: 10px 0;
                padding: 5px;
                font-size: 16px;
            }}
            #top-left-text {{
                margin: 0;
                padding: 0;
            }}
            #no-result-message {{
                text-align: center;
                color: red;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="search-container">
            <input type="text" id="search-input" placeholder="搜索Cosplay名称或编号">
            <div id="top-left-text">点击图片查看详细目录<br>更多资源Q群:138831650</div>
        </div>
        <div class="gallery">
            {html_code}
        </div>
        <p id="no-result-message">如未找到您喜欢的图片!<br>添加Q群:138831650 联系管理！</p>
        <script>
            document.getElementById('search-input').addEventListener('input', searchImages);

            function searchImages() {{
                var searchTerm = document.getElementById('search-input').value.toLowerCase();
                var imageItems = document.querySelectorAll('.image-item');
                var rowBreaks = document.querySelectorAll('.row-break');

                // 先隐藏所有图片项和换行元素
                imageItems.forEach(function(item) {{
                    item.style.display = 'none';
                }});
                rowBreaks.forEach(function(breakElement) {{
                    breakElement.style.display = 'none';
                }});

                var lastRowCount = 0;
                imageItems.forEach(function(item, index) {{
                    var captionName = item.querySelector('.caption-name').textContent.toLowerCase();
                    var captionNumber = item.querySelector('.caption-number').textContent.toLowerCase();
                    if (captionName.includes(searchTerm) || captionNumber.includes(searchTerm)) {{
                        item.style.display = 'inline-block';
                        lastRowCount++;
                        if (lastRowCount % 4 === 0) {{
                            // 每四张图片后显示换行元素
                            rowBreaks[Math.floor(index / 4)].style.display = 'block';
                        }}
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    """)

print(f"HTML代码已生成并保存到 {output_file} 文件中。")