#!/bin/bash
# 热点日报项目 - 每日自动提交脚本

echo "🚀 开始每日自动提交流程"
echo "========================"
echo "时间: $(date)"

# 1. 收集数据
echo "📊 收集热点数据..."
python hotspot_collector.py

# 2. 生成报告
echo "📝 生成日报..."
python generate_report.py

# 3. 添加到Git
echo "💾 提交到GitHub..."
git add .

# 4. 提交
COMMIT_MSG="每日更新: $(date '+%Y-%m-%d %H:%M')

✅ 自动收集B站+GitHub热点数据
📄 生成最新热点日报
📊 数据已保存到data/目录
📁 报告已生成到reports/目录"

git commit -m "$COMMIT_MSG"

# 5. 推送
git push origin main

echo "✅ 自动提交完成！"
echo "🔗 GitHub仓库: https://github.com/$(git remote get-url origin | cut -d':' -f2 | sed 's/\.git$//')"
