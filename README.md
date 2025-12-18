# 热点日报生成器

一个自动收集多平台热点内容并生成日报的工具。

## 🎯 项目目标
- 自动收集GitHub、B站、今日头条等平台的热点内容
- 生成结构化的热点日报
- 为内容创作者提供选题灵感

# 热点日报生成器

一个自动收集多平台热点内容并生成日报的工具。

## 🎯 项目目标
- 自动收集GitHub、B站、今日头条等平台的热点内容
- 生成结构化的热点日报
- 为内容创作者提供选题灵感

## �� 项目结构
hotspot-daily/
├── crawlers/ # 各平台爬虫
├── processors/ # 数据处理
├── utils/ # 工具函数
├── data/ # 数据存储（.gitignore）
├── reports/ # 生成的报告
├── requirements.txt # 依赖包
└── README.md

## 🚀 快速开始
1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 运行：`python crawlers/zhihu_test.py`

## 📅 今日进展
- 2024-12-17: 项目初始化，环境搭建完成
- 发现知乎API需要认证，计划从其他平台开始

## 🔧 技术栈
- Python 3.12
- Requests (网络请求)
- BeautifulSoup4 (HTML解析)
- Streamlit (计划中的Web界面)

## 📋 TODO
- [ ] 完善B站爬虫
- [ ] 实现GitHub Trending爬虫
- [ ] 添加今日头条爬虫
- [ ] 创建数据聚合器
- [ ] 生成Markdown日报
