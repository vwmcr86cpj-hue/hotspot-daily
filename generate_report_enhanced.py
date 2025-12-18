"""
增强版日报生成器 - 优化格式和可读性
"""
import json
import os
from datetime import datetime
import re

class EnhancedReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def generate_enhanced_report(self, data_file):
        """生成增强版日报"""
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        timestamp = datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
        
        # 生成更漂亮的Markdown
        md = f"""# 🌟 每日热点简报 {timestamp.strftime('%m/%d')}

> ⏰ 更新时间: {timestamp.strftime('%H:%M')} | 📊 数据来源: B站 + GitHub

---

## 📈 今日数据概览

| 指标 | 详情 |
|------|------|
| 收集时间 | {timestamp.strftime('%Y-%m-%d %H:%M:%S')} |
| 覆盖平台 | {data.get('summary', {}).get('platform_count', 0)} 个 |
| 热点数量 | {data.get('summary', {}).get('total_items', 0)} 条 |
| 生成状态 | ✅ 自动生成 |

---

## 🎬 B站今日热门

### 🎥 热门视频 TOP5
"""
        
        # B站视频部分
        bilibili_data = data.get("data", {}).get("bilibili", {})
        videos = bilibili_data.get("videos", [])
        
        for video in videos[:5]:
            view_str = f"{video.get('view', 0)/10000:.1f}万" if video.get('view', 0) >= 10000 else f"{video.get('view', 0)}"
            like_str = f"{video.get('like', 0)/10000:.1f}万" if video.get('like', 0) >= 10000 else f"{video.get('like', 0)}"
            
            md += f"""
**{video.get('rank', 0)}. {video.get('title', '')}**
- 👤 UP主: `{video.get('up', '')}`
- 📊 数据: ▶️{view_str} | 👍{like_str} | 💬{video.get('reply', 0)}
- 🔗 [观看链接]({video.get('url', '')})
"""
        
        # B站热搜
        hot_search = bilibili_data.get("hot_search", [])
        if hot_search:
            md += f"""
### 🔥 热搜话题
"""
            for item in hot_search[:5]:
                md += f"- **{item.get('keyword', '')}** `热搜第{item.get('rank', 0)}`\n"
        
        md += f"""
---

## 💻 GitHub 趋势

### 🏆 热门仓库
"""
        
        # GitHub部分
        github_data = data.get("data", {}).get("github", {})
        repos = github_data.get("repos", [])
        
        for repo in repos[:5]:
            stars = repo.get("stars", 0)
            stars_str = f"{stars/1000:.1f}k" if stars >= 1000 else str(stars)
            
            md += f"""
**{repo.get('title', '')}**
- 📝 {repo.get('description', '无描述')[:60]}...
- 🏷️ 语言: `{repo.get('language', 'Unknown')}`
- ⭐ 星标: **{stars_str}** (今日: +{repo.get('stars_today', 0)})
- 🔗 [查看仓库]({repo.get('url', '')})
"""
        
        # 页脚
        md += f"""
---

## 📊 生成信息
- 报告生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据文件: {os.path.basename(data_file)}
- 下次更新: 建议每日上午9点自动运行

> ✨ 本报告由热点日报系统自动生成，数据仅供参考
"""
        
        # 保存文件
        filename = f"{self.reports_dir}/enhanced_report_{timestamp.strftime('%Y%m%d_%H%M')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"📄 增强版日报已生成: {filename}")
        return filename

if __name__ == "__main__":
    # 找到最新数据文件
    data_files = [f for f in os.listdir('data') if f.startswith('hotspot_daily_')]
    if data_files:
        data_files.sort(reverse=True)
        latest_file = os.path.join('data', data_files[0])
        
        generator = EnhancedReportGenerator()
        report_file = generator.generate_enhanced_report(latest_file)
        
        if report_file:
            # 显示预览
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n" + "="*60)
                print("📋 增强版日报预览 (前20行):")
                print("="*60)
                for line in content.split('\n')[:20]:
                    print(line)
    else:
        print("❌ 没有找到数据文件")
