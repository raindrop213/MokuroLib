from flask import Flask, jsonify, send_file
import os
import re
from natsort import natsorted
import json
import logging

class NoGetRequestsFilter(logging.Filter):
    def filter(self, record):
        # 屏蔽所有包含 'GET' 的日志消息
        return 'GET' not in record.getMessage()

# 获取 werkzeug 日志器并添加过滤器
log = logging.getLogger('werkzeug')
log.addFilter(NoGetRequestsFilter())


app = Flask(__name__)

# 全局变量
CACHE_FILE = 'manga_cache.json'
MANGA_DIR = 'manga'

def load_cached_manga_list():
    if os.path.exists(CACHE_FILE) and os.path.exists(MANGA_DIR):
        manga_dir_time = os.path.getmtime(MANGA_DIR)
        cache_time = os.path.getmtime(CACHE_FILE)
        if cache_time >= manga_dir_time:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    return None


def save_manga_list_to_cache(manga_list):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(manga_list, f, ensure_ascii=False, indent=4)


def parse_manga_name(manga_name):
    match = re.match(r'\[(.*?)\]\s*(.*)', manga_name)
    if match:
        return match.groups()
    return None, manga_name


def get_manga_list():
    cached_list = load_cached_manga_list()
    if cached_list:
        print(f"已从缓存加载 {len(cached_list)} 部漫画。")
        return cached_list

    manga_list = []
    for manga_name in os.listdir(MANGA_DIR):
        manga_path = os.path.join(MANGA_DIR, manga_name)
        if os.path.isdir(manga_path):
            author, title = parse_manga_name(manga_name)
            volumes = []
            cover_image = None
            for file in os.listdir(manga_path):
                if file.endswith('.html'):
                    volume_path = os.path.join(manga_path, file[:-5])
                    volume_cover = None
                    if os.path.isdir(volume_path):
                        images = [img for img in os.listdir(volume_path) if img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
                        if images:
                            volume_cover = f'{MANGA_DIR}/{manga_name}/{file[:-5]}/{images[0]}'
                    volumes.append({
                        'title': file[:-5],
                        'path': f'{MANGA_DIR}/{manga_name}/{file}',
                        'cover': volume_cover
                    })
                if not cover_image and os.path.isdir(os.path.join(manga_path, file)):
                    image_dir = os.path.join(manga_path, file)
                    images = [img for img in os.listdir(image_dir) if img.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
                    if images:
                        cover_image = f'{MANGA_DIR}/{manga_name}/{file}/{images[0]}'

            if volumes:
                manga_list.append({
                    'author': author,
                    'title': title,
                    'volumes': natsorted(volumes, key=lambda x: x['title']),
                    'cover': cover_image
                })

    save_manga_list_to_cache(manga_list)
    print(f"共加载 {len(manga_list)} 部漫画。")
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
