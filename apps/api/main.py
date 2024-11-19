import os
import re
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS  # 需要安装: pip install flask-cors

app = Flask(__name__)
CORS(app)

# Markdown 文件主目录
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'md_files')

@app.route('/api/folders', methods=['GET'])
def list_folders():
    """获取所有子文件夹名称"""
    folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
    return jsonify(folders)
    

@app.route('/api/file', methods=['GET'])
def get_markdown_file():
    """获取指定 Markdown 文件内容"""
    folder = request.args.get('folder')
    file_path = os.path.join(BASE_DIR, folder, folder+'.md')  # 假设每个文件夹都有一个 index.md

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 处理图片路径
    content = re.sub(
        r'!\[(.*?)\]\((.*?)\)', 
        lambda match: f'![{match.group(1)}](http://127.0.0.1:5000/api/image/{folder}/{match.group(2)})',
        content
    )

    return jsonify({'content': content})

@app.route('/api/image/<folder>/<filename>', methods=['GET'])
def get_image(folder, filename):
    """获取图片文件"""
    img_path = os.path.join(BASE_DIR, folder, filename)
    if os.path.exists(img_path):
        return send_file(img_path)
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
