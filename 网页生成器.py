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
# 子网页文件夹路径，相对于项目根目录
subpage_folder = "子网页"
# 商品链接文件夹路径，相对于项目根目录
link_folder = "商品链接"
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

# 获取所有图片文件名（支持更多格式）
image_files = sorted(
    [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpeg', '.jpg', '.png', '.gif'))]
)
print(f"获取到的图片文件数量: {len(image_files)}")

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

# 读取商品链接文件
link_file_path = os.path.join(link_folder, "链接.txt")
if os.path.exists(link_file_path):
    with open(link_file_path, 'r', encoding='utf-8') as file:
        links = file.read().splitlines()
    # 提取链接并存储为字典，格式为 {编号: 链接}
    link_dict = {}
    for link in links:
        match = re.match(r'(\d+)\.\s*.*商品链接：(.+)', link)
        if match:
            link_dict[match.group(1)] = match.group(2)
else:
    link_dict = {}

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
            <link rel="icon" href="../网页素材/图标-10种尺寸.ico" type="image/x-icon">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-image: url('../网页素材/背景.jpg');
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
               .content {{
                    margin: 20px;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: rgba(255, 255, 255, 0.8); /* 为内容区域添加半透明背景 */
                }}
               .content h1 {{
                    color: black; /* 设置标题颜色 */
                }}
               .content p {{
                    color: red; /* 设置提示文本颜色 */
                }}
               .content pre {{
                    color: blue; /* 设置详细内容文本颜色 */
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <h1>{subpage_title}</h1>
                <p>有时目录更新可能不及时,<br>具体已实际资源为准!</p>
                <pre>{detail_content}</pre>
            </div>
        </body>
        </html>
        """)

# 每页显示的图片数量
items_per_page = 24
# 计算总页数
total_pages = len(image_files) // items_per_page
if len(image_files) % items_per_page != 0:
    total_pages += 1

# 生成主页面HTML代码
html_code_pages = []
all_image_items = []
for page in range(total_pages):
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    page_image_files = image_files[start_index:end_index]
    page_names = names[start_index:end_index]
    page_html_code = ""
    for index, (image_file, name) in enumerate(zip(page_image_files, page_names), start=start_index + 1):
        # 格式化编号为三位数（例如：001, 002,..., 450）
        formatted_index = f"{index:03d}"
        # 在编号前添加 NO:
        numbered_caption = f"NO:{formatted_index}"
        # 获取对应的子页面链接
        subpage_link = f"{subpage_folder}/{subpage_titles[index - 1]}.html" if index - 1 < len(subpage_titles) else "#"
        # 获取对应的商品链接
        buy_link = link_dict.get(formatted_index, "#")
        # 创建图片和按钮的HTML代码
        item_html = f"""
        <div class="image-item" id="image-{index}">
            <img src="{image_folder}/{image_file}" alt="{name}">
            <div class="caption-number">{numbered_caption}</div>
            <div class="caption-name">{name}</div>
            <div class="buttons">
                <a href="{subpage_link}" target="_blank" class="detail-button">详细目录</a>
                <a href="#" onclick="return confirmPurchase('{buy_link}')" class="buy-button">立即购买</a>
            </div>
        </div>
        """
        page_html_code += item_html
        all_image_items.append(item_html)
        # 每4张图片换一行
        if index % 4 == 0:
            page_html_code += "<div class='row-break'></div>"

    # 添加分页导航（优化为只显示5个页码）
    pagination = "<div class='pagination'>"
    if page > 0:
        pagination += f"<a href='javascript:void(0);' data-page='{page - 1}'>上一页</a>"

    # 计算页码范围
    start_page = max(0, page - 2)
    end_page = min(total_pages, start_page + 5)
    if end_page - start_page < 5:
        start_page = max(0, end_page - 5)

    for i in range(start_page, end_page):
        if i == page:
            pagination += f"<span class='current-page'>{i + 1}</span>"
        else:
            pagination += f"<a href='javascript:void(0);' data-page='{i}'>{i + 1}</a>"

    if page < total_pages - 1:
        pagination += f"<a href='javascript:void(0);' data-page='{page + 1}'>下一页</a>"
    pagination += "</div>"

    # 单独添加显示总页数的代码
    total_pages_display = f"<div class='total-pages-display'>共 {total_pages} 页</div>"

    page_html_code += pagination + total_pages_display
    html_code_pages.append(page_html_code)

# 生成主页面的 HTML 模板
main_template = f"""
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
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            position: relative;
        }}

       .gallery {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            box-sizing: border-box;
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
            vertical-align: top; /* 保证图片项顶部对齐 */
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
            bottom: 85px;
            left: 50%;
            transform: translateX(-50%);
            color: #FF0000;
            font-weight: bold;
            font-family: 'KaiTi', serif;
            background-color: rgba(0, 0, 0, 0.0);
            padding: 5px;
            border-radius: 5px;
            /* 使用 text-shadow 模拟更细的描边 */
            text-shadow: 
                -0.5px -0.5px 0 #FFFFFF,  
                 0.5px -0.5px 0 #FFFFFF,
                -0.5px  0.5px 0 #FFFFFF,
                 0.5px  0.5px 0 #FFFFFF;
            white-space: nowrap;
            letter-spacing: 0px;
        }}

       .caption-name {{
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            color: black;
            font-weight: bold;
            font-family: 'KaiTi', serif;
            background-color: rgba(200, 200, 200, 0.88);
            padding: 3px;
            border-radius: 5px;
            white-space: nowrap;
        }}

       .buttons {{
            position: relative; /* 修改为相对定位 */
            bottom: auto;
            left: auto;
            transform: none;
            display: block; /* 修改为块级元素 */
            margin-top: 10px; /* 添加顶部间距 */
        }}

       .buttons a {{
            display: inline-block; /* 修改为内联块元素 */
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 14px;
            margin: 5px; /* 添加按钮间距 */
        }}

       .buttons a.buy-button {{
            background-color: #f44336;
        }}

       .row-break {{
            clear: both;
        }}

       .search-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
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

       .pagination {{
            text-align: center;
            margin-top: 20px;
        }}

       .pagination a,
       .pagination span {{
            display: inline-block;
            padding: 5px 10px;
            margin: 0 5px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            text-decoration: none;
            color: #333;
        }}

       .pagination .current-page {{
            background-color: #333;
            color: white;
        }}

       .total-pages-display {{
            text-align: center;
            margin-top: 10px;
        }}

        /* 媒体查询：手机端 */
        @media (max-width: 768px) {{
           .caption-number {{
                font-size: 12px;
            }}

           .caption-name {{
                font-size: 6px;
            }}

           .buttons a {{
                font-size: 10px;
                padding: 3px 6px;
            }}
        }}

        /* 媒体查询：平板端 */
        @media (min-width: 769px) and (max-width: 1024px) {{
           .caption-number {{
                font-size: 22px;
            }}

           .caption-name {{
                font-size: 16px;
            }}

           .buttons a {{
                font-size: 12px;
                padding: 4px 8px;
            }}
        }}

        /* 媒体查询：电脑端 */
        @media (min-width: 1025px) {{
           .caption-number {{
                font-size: 26px;
            }}

           .caption-name {{
                font-size: 18px;
            }}

           .buttons a {{
                font-size: 14px;
                padding: 5px 10px;
            }}
        }}

        /* 自定义模态框样式 */
       .modal {{
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.4);
        }}

       .modal-content {{
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 400px;
            text-align: center;
            border-radius: 15px; /* 添加弹窗圆角 */
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }}

       .close {{
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            position: absolute;
            top: 10px;
            right: 10px;
        }}

       .close:hover,
       .close:focus {{
            color: black;
            text-decoration: none;
            cursor: pointer;
        }}

       .modal-content p.title {{
            color: #0000FF; /* 标题颜色 */
            font-weight: bold;
            margin-bottom: 20px; /* 增加底部间距 */
        }}

       .modal-content p.content {{
            color: #008000; /* 内容颜色 */
            margin: 10px 0; /* 调整上下间距 */
        }}

       .modal-content p.tip {{
            color: #FF0000; /* 提示颜色 */
            margin: 10px 0; /* 调整上下间距 */
        }}

       .modal-content p.ti {{
            color: #000000; /* 提示颜色 */
            margin-top: 20px; /* 增加顶部间距 */
        }}
    </style>
</head>

<body>
    <div class="search-container">
        <input type="text" id="search-input" placeholder="搜索Cosplay名称或编号">
        <div id="top-left-text">平台不做任何回复<br>更多资源Q群:138831650</div>
    </div>
    <div class="gallery" id="gallery">
        <!-- 这里将插入分页的 HTML 代码 -->
        {{ page_html_code }}
    </div>
    <p id="no-result-message">如未找到您喜欢的图片!<br>添加Q群:138831650 联系管理！</p>
    <!-- 自定义模态框 -->
    <div id="myModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="modal-notice"></div>
            <button id="confirm-button">确定</button>
        </div>
    </div>
    <script>
        const htmlCodePages = {html_code_pages};
        const allImageItems = {all_image_items};
        const gallery = document.getElementById('gallery');
        const searchInput = document.getElementById('search-input');
        let currentPage = 0;
        let targetLink = '';

        function showPage(page) {{
            currentPage = page;
            if (searchInput.value === '') {{
                gallery.innerHTML = htmlCodePages[page];
            }} else {{
                const searchResults = [];
                allImageItems.forEach(item => {{
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(item, 'text/html');
                    const captionName = doc.querySelector('.caption-name').textContent.toLowerCase();
                    const captionNumber = doc.querySelector('.caption-number').textContent.toLowerCase();
                    const searchTerm = searchInput.value.toLowerCase();
                    if (captionName.includes(searchTerm) || captionNumber.includes(searchTerm)) {{
                        searchResults.push(item);
                    }}
                }});

                const totalSearchPages = Math.ceil(searchResults.length / {items_per_page});
                const startIndex = page * {items_per_page};
                const endIndex = startIndex + {items_per_page};
                const pageResults = searchResults.slice(startIndex, endIndex);

                let pageHtml = '';
                pageResults.forEach((item, i) => {{
                    pageHtml += item;
                    if ((i + 1) % 4 === 0) {{
                        pageHtml += '<div class="row-break"></div>';
                    }}
                }});

                const pagination = createPagination(page, totalSearchPages);
                const totalPagesDisplay = `<div class='total-pages-display'>共 ${{totalSearchPages}} 页</div>`;
                pageHtml += pagination + totalPagesDisplay;
                gallery.innerHTML = pageHtml;
            }}
            const newPaginationLinks = document.querySelectorAll('.pagination a');
            newPaginationLinks.forEach(link => {{
                link.addEventListener('click', function() {{
                    const newPage = parseInt(this.dataset.page);
                    showPage(newPage);
                }});
            }});
        }}

        function createPagination(page, totalPages) {{
            let pagination = '<div class="pagination">';
            if (page > 0) {{
                pagination += `<a href='javascript:void(0);' data - page='${{page - 1}}'>上一页</a>`;
            }}
            const startPage = Math.max(0, page - 2);
            const endPage = Math.min(totalPages, startPage + 5);
            for (let i = startPage; i < endPage; i++) {{
                if (i === page) {{
                    pagination += `<span class="current - page">${{i + 1}}</span>`;
                }} else {{
                    pagination += `<a href='javascript:void(0);' data - page='${{i}}'>${{i + 1}}</a>`;
                }}
            }}
            if (page < totalPages - 1) {{
                pagination += `<a href='javascript:void(0);' data - page='${{page + 1}}'>下一页</a>`;
            }}
            pagination += "</div>";
            return pagination;
        }}

        searchInput.addEventListener('input', function() {{
            showPage(0);
        }});

        showPage(0);

        function confirmPurchase(link) {{
            targetLink = link;
            const modal = document.getElementById('myModal');
            const notice = `
                <p class="title">购买须知</p>
                <p class="content">即将跳转到对应商品链接</p>
                <p class="content">付款后自动网盘发货</p>
                <p class="tip">※为防止商品链接失效※<br>※商品以风景素材展示※</p>
                <p class="ti">有问题群内咨询<br>Q群：138831650</p>
            `;
            const modalNotice = document.getElementById('modal-notice');
            modalNotice.innerHTML = notice;
            modal.style.display = 'block';

            const closeBtn = document.querySelector('.close');
            const confirmBtn = document.getElementById('confirm-button');

            closeBtn.onclick = function() {{
                modal.style.display = 'none';
            }}

            confirmBtn.onclick = function() {{
                window.open(targetLink, '_blank');
                modal.style.display = 'none';
            }}

            window.onclick = function(event) {{
                if (event.target == modal) {{
                    modal.style.display = 'none';
                }}
            }}
        }}
    </script>
</body>

</html>
"""

# 保存默认第一页到文件
output_file = os.path.join(output_folder, "000.html")
with open(output_file, "w", encoding="utf - 8") as file:
    # 确保占位符一致，正确替换
    correct_placeholder = "{{ page_html_code }}"
    final_html = main_template.replace(correct_placeholder, html_code_pages[0])
    final_html = final_html.replace("{{html_code_pages}}", str(html_code_pages).replace("'", '"'))
    final_html = final_html.replace("{{all_image_items}}", str(all_image_items).replace("'", '"'))
    file.write(final_html)

print(f"HTML代码已生成并保存到 {output_file} 文件中。")