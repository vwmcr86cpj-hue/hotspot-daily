"""
热点日报生成器
从JSON数据生成Markdown格式的日报
"""
import json
import os
from datetime import datetime
import re

class ReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def find_latest_data(self, data_dir="data"):
        """查找最新的数据文件"""
        data_files = []
        for f in os.listdir(data_dir):
            if f.startswith("hotspot_daily_") and f.endswith(".json"):
                data_files.append(os.path.join(data_dir, f))
        
        if not data_files:
            print("❌ 没有找到数据文件")
            return None
        
        # 按修改时间排序
        data_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return data_files[0]
    
    def load_data(self, data_file):
        """加载数据文件"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return None
    
    def generate_markdown(self, data, filename_prefix="hotspot_report"):
        """生成Markdown日报"""
        if not data:
            return None
        
        timestamp = datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
        
        # 构建Markdown内容
        md_content = f"""# 📰 热点日报 {timestamp.strftime('%Y年%m月%d日')}

> 每日热点速览 | 自动生成 | 数据更新时间: {timestamp.strftime('%H:%M')}

## 📊 数据概览

"""
        
        # 汇总信息
        summary = data.get("summary", {})
        md_content += f"- **收集时间**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        md_content += f"- **覆盖平台**: {summary.get('platform_count', 0)} 个\n"
        md_content += f"- **热点总数**: {summary.get('total_items', 0)} 条\n\n"
        
        # 各平台数据
        platforms_data = data.get("data", {})
        
        # 1. B站数据
        if "bilibili" in platforms_data:
            bilibili_data = platforms_data["bilibili"]
            md_content += self._generate_bilibili_section(bilibili_data)
        
        # 2. GitHub数据
        if "github" in platforms_data:
            github_data = platforms_data["github"]
            md_content += self._generate_github_section(github_data)
        
        # 页脚
        md_content += f"\n---\n"
        md_content += f"*报告自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        md_content += f"*数据来源: Bilibili, GitHub Trending*\n"
        
        return md_content
    
    def _generate_bilibili_section(self, data):
        """生成B站数据部分"""
        section = "\n## 📺 B站热点\n\n"
        
        # 热门视频
        videos = data.get("videos", [])
        if videos:
            section += "### 🎥 热门视频\n\n"
            for video in videos[:5]:  # 最多5个
                view_str = self._format_number(video.get("view", 0))
                like_str = self._format_number(video.get("like", 0))
                duration = video.get("duration", 0)
                
                section += f"{video.get('rank', 0)}. **{video.get('title', '')}**\n"
                section += f"   - UP主: {video.get('up', '')}\n"
                section += f"   - 播放: {view_str} | 点赞: {like_str}\n"
                if duration > 0:
                    minutes = duration // 60
                    seconds = duration % 60
                    section += f"   - 时长: {minutes}:{seconds:02d}\n"
                section += f"   - [观看链接]({video.get('url', '')})\n\n"
        
        # 热搜词
        hot_search = data.get("hot_search", [])
        if hot_search:
            section += "### 🔥 热搜话题\n\n"
            for item in hot_search[:5]:  # 最多5个
                section += f"{item.get('rank', 0)}. **{item.get('keyword', '')}**\n"
                if item.get('heat'):
                    section += f"   热度: {item.get('heat')}\n"
                section += f"   搜索: {item.get('url', '')}\n\n"
        
        return section
    
    def _generate_github_section(self, data):
        """生成GitHub数据部分"""
        section = "\n## 💻 GitHub 趋势\n\n"
        
        repos = data.get("repos", [])
        if repos:
            section += "### 🏆 热门仓库\n\n"
            for repo in repos[:5]:  # 最多5个
                stars = repo.get("stars", 0)
                stars_today = repo.get("stars_today", "0")
                language = repo.get("language", "Unknown")
                
                section += f"{repo.get('title', '')}\n"
                section += f"   - 描述: {repo.get('description', '无描述')[:80]}\n"
                section += f"   - 语言: {language}\n"
                section += f"   - 星标: {self._format_number(stars)} (今日: +{stars_today})\n"
                section += f"   - 仓库: {repo.get('url', '')}\n\n"
        
        return section
    
    def _format_number(self, num):
        """格式化数字显示"""
        if num >= 100000000:
            return f"{num/100000000:.1f}亿"
        elif num >= 10000:
            return f"{num/10000:.1f}万"
        else:
            return f"{num:,}"
    
    def save_report(self, markdown_content, filename_prefix="hotspot_report"):
        """保存日报到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.reports_dir}/{filename_prefix}_{timestamp}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"📄 日报已生成: {filename}")
        return filename
    
    def generate_and_save(self, data_file=None):
        """生成并保存日报"""
        if not data_file:
            data_file = self.find_latest_data()
            if not data_file:
                return None
        
        print(f"📁 使用数据文件: {data_file}")
        
        data = self.load_data(data_file)
        if not data:
            return None
        
        print("📝 生成日报内容...")
        markdown_content = self.generate_markdown(data)
        
        if markdown_content:
            report_file = self.save_report(markdown_content)
            
            # 显示报告摘要
            print("\n" + "=" * 60)
            print("🎉 热点日报生成完成！")
            print("=" * 60)
            print(f"📄 报告文件: {report_file}")
            print(f"📊 报告大小: {len(markdown_content)} 字符")
            
            # 显示前几行预览
            print("\n📋 报告预览:")
            print("-" * 40)
            for line in markdown_content.split('\n')[:15]:
                print(line)
            print("-" * 40)
            
            return report_file
        else:
            print("❌ 日报生成失败")
            return None

if __name__ == "__main__":
    generator = ReportGenerator()
    report_file = generator.generate_and_save()
    
    if report_file:
        print(f"\n🚀 日报生成成功！")
        print(f"💡 查看完整报告: cat {report_file}")
    else:
        print("❌ 日报生成失败")
