#!/bin/bash
echo "🚀 热点日报项目 - 明日快速启动"
echo "================================"
echo "当前目录: $(pwd)"
echo "Python版本: $(python --version)"
echo "Git状态:"
git status
echo -e "\n📁 文件结构:"
ls -la
echo -e "\n💡 明日任务建议:"
echo "1. 查看TODO.md了解计划"
echo "2. 从B站爬虫开始: python crawlers/bilibili_hot.py"
echo "3. 运行完整收集: python hotspot_collector.py"
echo "================================"
