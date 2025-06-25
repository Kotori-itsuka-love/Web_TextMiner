from flask import Flask, request, jsonify, Response
import spacy
from spacy.matcher import Matcher
from textblob import TextBlob
import os
from flask_cors import CORS
from flask import send_from_directory
import json
from datetime import datetime

FEEDBACK_FILE = 'feedback.json'


USER_FILE = 'users.json'
# 初始化 Flask 应用
app = Flask(__name__)

# 允许跨域请求
CORS(app)

# 加载 zh_core_web_lg 模型
nlp = spacy.load('D:/For_pytorch/pythonProject/zh_core_web_lg-3.0.0/zh_core_web_lg/zh_core_web_lg-3.0.0')

# 文件上传路径
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_user(data):
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = []

    users.append(data)

    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_feedbacks():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_feedbacks(feedbacks):
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# 1. 命名实体识别（NER）
def get_entities(text):
    doc = nlp(text)
    return [{"entity": ent.text, "type": ent.label_, "start": ent.start_char, "end": ent.end_char} for ent in doc.ents]

# 2. 词性标注（POS Tagging）
def get_pos_tags(text):
    doc = nlp(text)
    return [{"word": token.text, "pos": token.pos_, "start": token.idx, "end": token.idx + len(token.text)} for token in doc]

# 3. 依存句法分析（Dependency Parsing）
def get_dependency_parse(text):
    doc = nlp(text)
    return [{"word": token.text, "dep": token.dep_, "head": token.head.text, "start": token.idx, "end": token.idx + len(token.text)} for token in doc]

# 4. 句法分析（Sentence Segmentation）
def get_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

# 5. 情感分析（Sentiment Analysis）
def get_sentiment(text):
    blob = TextBlob(text)
    return {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}

# 根路由，返回首页
@app.route('/')
def home():
    with open('index.html', encoding='utf-8') as f:
        content = f.read()
    return Response(content, content_type='text/html; charset=utf-8')

# 文件上传路由
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # 读取文件内容

    return jsonify({"message": "File uploaded successfully", "file_path": f"uploads/{file.filename}"})

# 处理请求路由，根据用户选择返回不同的结果
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text', '')
    file_path = data.get('file_path', '')
    options = data.get('options', [])  # 允许选择多个功能

    if text:  # 如果用户输入了文本
        result = {}
        if 'entities' in options:
            result['entities'] = get_entities(text)
        if 'pos_tags' in options:
            result['pos_tags'] = get_pos_tags(text)
        if 'dep_parse' in options:
            result['dep_parse'] = get_dependency_parse(text)
        if 'sentences' in options:
            result['sentences'] = get_sentences(text)
        if 'sentiment' in options:
            result['sentiment'] = get_sentiment(text)

        if not result:
            return jsonify({"error": "没有选择有效的选项"}), 400

        return jsonify(result)

    elif file_path:  # 如果是上传文件
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        result = {}
        if 'entities' in options:
            result['entities'] = get_entities(text)
        if 'pos_tags' in options:
            result['pos_tags'] = get_pos_tags(text)
        if 'dep_parse' in options:
            result['dep_parse'] = get_dependency_parse(text)
        if 'sentences' in options:
            result['sentences'] = get_sentences(text)
        if 'sentiment' in options:
            result['sentiment'] = get_sentiment(text)

        if not result:
            return jsonify({"error": "没有选择有效的选项"}), 400

        return jsonify(result)

    else:
        return jsonify({"error": "没有提供文本或文件"}), 400

@app.route('/register', methods=['POST'])

def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    avatar = request.files.get('avatar')

    if avatar:
        avatar_filename = f"{email}_avatar.png"
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
        avatar.save(avatar_path)
    else:
        avatar_filename = None

    # 保存用户信息到数据库（略，此处可改为打印或存入文件）
    print(f"注册用户: {name}, 邮箱: {email}, 头像路径: {avatar_filename}")
    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "avatar": f"/uploads/{avatar_filename}" if avatar_filename else ""
    }

    save_user(user_data)
    return jsonify({"success": True, "avatar_url": user_data["avatar"]})

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not os.path.exists(USER_FILE):
        return jsonify({"success": False, "error": "用户不存在"})

    with open(USER_FILE, 'r', encoding='utf-8') as f:
        users = json.load(f)

    for user in users:
        if user["email"] == email:
            if user["password"] == password:
                return jsonify({
                    "success": True,
                    "name": user["name"],
                    "avatar": user["avatar"]
                })
            else:
                return jsonify({"success": False, "error": "密码错误"})

    return jsonify({"success": False, "error": "用户不存在"})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    email = request.form.get('email')
    feedback_type = request.form.get('type')
    content = request.form.get('content')

    if not email or not content:
        return jsonify({"success": False, "error": "邮箱和内容不能为空"})

    feedbacks = load_feedbacks()
    feedbacks.append({
        "email": email,
        "type": feedback_type,
        "content": content,
        "reply": "",
        "time": datetime.now().isoformat()
    })
    save_feedbacks(feedbacks)

    return jsonify({"success": True})

@app.route('/admin_feedbacks')
def admin_feedbacks():
    return jsonify(load_feedbacks())

@app.route('/reply_feedback', methods=['POST'])
def reply_feedback():
    index = int(request.form.get('index'))
    reply_text = request.form.get('reply')

    feedbacks = load_feedbacks()
    if 0 <= index < len(feedbacks):
        feedbacks[index]['reply'] = reply_text
        save_feedbacks(feedbacks)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "反馈不存在"})

@app.route('/user_feedbacks', methods=['GET'])
def user_feedbacks():
    email = request.args.get('email')
    if not email:
        return jsonify([])
    feedbacks = load_feedbacks()
    return jsonify([f for f in feedbacks if f['email'] == email])


# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
