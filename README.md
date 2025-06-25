# Web_TextMiner

一个基于 Web 的中文文本信息提取与分析系统，支持命名实体识别、词性标注、情感分析、依存句法分析等功能，适用于法律、教育、新闻等行业的文档处理需求。

ATTENTION: 由于模型过大，未将模型放在仓库里，需要安装zh_core_web_lg-3.0.0模型并放在文件夹中才能运行
这是下载地址：https://github.com/explosion/spacy-models/releases/download/zh_core_web_lg-3.0.0/zh_core_web_lg-3.0.0.tar.gz
你也可以使用 spaCy 命令安装：python -m spacy download zh_core_web_lg

## 🔍 项目特点

- 支持上传 `.txt` 文本文件或直接输入文本进行分析
- 提供命名实体识别（NER）、词性标注、情感分析、句法分析等功能
- 分析结果以可视化图表与结构化信息形式展示
- 实现用户注册、登录、头像上传功能
- 用户可提交反馈，管理员可查看与回复
- 历史分析记录可追溯、可还原
- 支持管理员端操作与多角色权限控制

## 🧠 使用技术栈

| 分类 | 技术 |
|------|------|
| 前端 | HTML、CSS、JavaScript、Chart.js |
| 后端 | Python、Flask、spaCy、TextBlob |
| 数据 | JSON 本地文件存储（可拓展为数据库） |
| 其他 | Git、GitHub、Git LFS（可选用于大文件） |

## 🚀 功能演示

### 📄 文本分析
- 输入或上传文本，勾选功能项，点击“开始提取”
- 支持以下 NLP 模块：
  - 命名实体识别
  - 词性标注
  - 句法分析
  - 情感分析（使用 TextBlob）

### 👤 用户系统
- 注册时支持头像上传
- 登录后可查看历史分析记录与反馈回复

### 🛠 管理员系统
- 查看所有用户反馈
- 提供反馈回复功能并自动发送至用户端

## 📂 项目结构
├── static/ # 前端样式与脚本
├── templates/ # HTML 页面（如使用 Flask 模板）
├── uploads/ # 用户上传文件
├── users.json # 用户信息存储（邮箱、密码、头像）
├── feedback.json # 用户反馈信息
├── index.html # 项目主页面
├── web.py # Flask 后端主程序
├── README.md # 项目说明文件

启动服务

python web.py
访问：http://localhost:5000
