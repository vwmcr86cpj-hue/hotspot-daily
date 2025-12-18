"""
热点日报主收集器 - 使用B站和GitHub
"""
import json
import time
from datetime import datetime
import os
import sys

# 导入自定义爬虫
sys.path.append('.')
try:
    from crawlers.bilibili import BilibiliCrawler
    from crawlers.github_trending import GitHubTrendingCrawler
    print("✅ 爬虫模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class HotspotCollector:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化可用的爬虫
        self.bilibili_crawler = BilibiliCrawler()
        self.github_crawler = GitHubTrendingCrawler()
        print("📦 爬虫初始化完成")
    
    def collect_all(self):
        """收集所有可用平台数据"""
        print("=" * 60)
        print("🔥 热点日报数据收集器 v1.0")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        all_data = {
            "timestamp": datetime.now().isoformat(),
            "platforms": {},
            "data": {}
        }
        
        # 1. 收集B站数据
        print("\n[1/2] 收集B站数据...")
        bilibili_results = self._collect_bilibili()
        if bilibili_results:
            all_data["platforms"]["bilibili"] = {
                "name": "Bilibili",
                "status": "success"
            }
            all_data["data"]["bilibili"] = bilibili_results
        time.sleep(2)
        
        # 2. 收集GitHub数据
        print("\n[2/2] 收集GitHub数据...")
        github_results = self._collect_github()
        if github_results:
            all_data["platforms"]["github"] = {
                "name": "GitHub Trending", 
                "status": "success"
            }
            all_data["data"]["github"] = github_results
        
        # 统计和保存
        return self._finish_collection(all_data)
    
    def _collect_bilibili(self):
        """收集B站数据"""
        try:
            print("  📺 获取热门视频...")
            videos = self.bilibili_crawler.get_ranking(rid=0, page_size=10)
            time.sleep(1)
            
            print("  �� 获取热搜词...")
            hot_search = self.bilibili_crawler.get_hot_search()
            
            if videos or hot_search:
                return {
                    "videos": videos[:5] if videos else [],  # 只取前5
                    "hot_search": hot_search[:5] if hot_search else []
                }
        except Exception as e:
            print(f"  ❌ B站收集失败: {e}")
        return None
    
    def _collect_github(self):
        """收集GitHub数据"""
        try:
            print("  💻 获取GitHub热门仓库...")
            repos = self.github_crawler.get_trending(since="daily")
            
            if repos:
                return {
                    "repos": repos[:5]  # 只取前5
                }
        except Exception as e:
            print(f"  ❌ GitHub收集失败: {e}")
        return None
    
    def _finish_collection(self, all_data):
        """完成收集流程"""
        print("\n" + "=" * 60)
        print("📊 数据收集统计")
        print("=" * 60)
        
        # 计算统计数据
        total_items = 0
        platform_count = 0
        
        for platform_id, platform_info in all_data["platforms"].items():
            if platform_info["status"] == "success":
                platform_count += 1
                data = all_data["data"].get(platform_id, {})
                
                if platform_id == "bilibili":
                    video_count = len(data.get("videos", []))
                    hot_count = len(data.get("hot_search", []))
                    total_items += video_count + hot_count
                    print(f"  📺 Bilibili: {video_count}视频 + {hot_count}热搜")
                
                elif platform_id == "github":
                    repo_count = len(data.get("repos", []))
                    total_items += repo_count
                    print(f"  💻 GitHub: {repo_count}个仓库")
        
        all_data["summary"] = {
            "total_items": total_items,
            "platform_count": platform_count,
            "collection_time": datetime.now().isoformat()
        }
        
        # 保存数据
        if total_items > 0:
            filename = self._save_data(all_data)
            
            print(f"\n💾 数据已保存: {filename}")
            print(f"🎯 成功收集 {platform_count} 个平台，共 {total_items} 条数据")
            print("=" * 60)
            
            return filename
        else:
            print("\n❌ 没有收集到任何数据")
            return None
    
    def _save_data(self, data):
        """保存数据到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.data_dir}/hotspot_daily_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename

if __name__ == "__main__":
    collector = HotspotCollector()
    data_file = collector.collect_all()
    
    if data_file:
        print("🎉 数据收集完成！下一步：")
        print("1. 查看数据: cat data/hotspot_daily_*.json | head -100")
        print("2. 生成日报: python generate_report.py")
    else:
        print("❌ 数据收集失败，请检查爬虫")
