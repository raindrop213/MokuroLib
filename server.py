from flask import Flask, jsonify, send_file
import os
import re
from natsort import natsorted  # 用于排序
import json

app = Flask(__name__)

def load_cached_manga_list():
    cache_file = 'manga_cache.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_manga_list_to_cache(manga_list):
    cache_file = 'manga_cache.json'
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(manga_list, f, ensure_ascii=False, indent=4)

def parse_manga_name(manga_name):
    # 假设格式为 "[作者] 作品名"
    match = re.match(r'\[(.*?)\]\s*(.*)', manga_name)
    if match:
        author, title = match.groups()
        return author, title
    return None, manga_name

def get_manga_list():
    # 尝试从缓存加载
    cached_list = load_cached_manga_list()
    if cached_list:
        return cached_list

    manga_dir = "manga"
    manga_list = []
    
    # 遍历manga目录
    for manga_name in os.listdir(manga_dir):
        manga_path = os.path.join(manga_dir, manga_name)
        if os.path.isdir(manga_path):
            author, title = parse_manga_name(manga_name)
            volumes = []
            cover_image = None
            # 查找该漫画下的所有html文件
            for file in os.listdir(manga_path):
                if file.endswith('.html'):
                    volume_path = os.path.join(manga_path, file[:-5])
                    volume_cover = None
                    if os.path.isdir(volume_path):
                        images = [img for img in os.listdir(volume_path) if img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
                        if images:
                            volume_cover = f'{manga_dir}/{manga_name}/{file[:-5]}/{images[0]}'
                    
                    volumes.append({
                        'title': file[:-5],  # 移除.html后缀
                        'path': f'{manga_dir}/{manga_name}/{file}',
                        'cover': volume_cover
                    })
                # 查找漫画封面图片
                if not cover_image and os.path.isdir(os.path.join(manga_path, file)):
                    image_dir = os.path.join(manga_path, file)
                    images = [img for img in os.listdir(image_dir) if img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
                    if images:
                        cover_image = f'{manga_dir}/{manga_name}/{file}/{images[0]}'
            
            if volumes:  # 只添加有卷的漫画
                manga_list.append({
                    'author': author,
                    'title': title,
                    'volumes': natsorted(volumes, key=lambda x: x['title']),
                    'cover': cover_image
                })
    
    # 保存到缓存
    save_manga_list_to_cache(manga_list)
    return natsorted(manga_list, key=lambda x: x['title'])

@app.route('/list-manga')
def list_manga():
    return jsonify(get_manga_list())

@app.route('/')
def root():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8091) 