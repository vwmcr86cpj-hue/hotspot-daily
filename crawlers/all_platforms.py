"""
多平台热点爬虫 - 知乎失败就先做其他平台
"""
import requests
import json
from datetime import datetime
import time

class MultiPlatformCrawler:
    def __init__(self):
        self.results = {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def get_weibo_hot(self):
        """微博热搜 - 通过官方API（稳定）"""
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            response = requests.get(url, headers=self.headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                hot_searches = data.get("data", {}).get("realtime", [])
                
                items = []
                for item in hot_searches[:15]:
                    items.append({
                        "title": item.get("word", ""),
                        "hot": item.get("num", 0),
                        "rank": item.get("rank", 0)
                    })
                
                print(f"✅ 微博热搜: 获取 {len(items)} 条")
                return items
        except Exception as e:
            print(f"❌ 微博热搜失败: {e}")
        return None
    
    def get_bilibili_hot(self):
        """B站热门视频"""
        try:
            url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
            response = requests.get(url, headers=self.headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get("data", {}).get("list", [])
                
                items = []
                for video in videos[:15]:
                    items.append({
                        "title": video.get("title", ""),
                        "play": video.get("stat", {}).get("view", 0),
                        "up": video.get("owner", {}).get("name", "")
                    })
                
                print(f"✅ B站热门: 获取 {len(items)} 条")
                return items
        except Exception as e:
            print(f"❌ B站热门失败: {e}")
        return None
    
    def get_zhihu_fallback(self):
        """知乎备用方案 - 模拟简单请求"""
        try:
            # 知乎热榜的另一个可能接口
            url = "https://www.zhihu.com/api/v4/search/top_search"
            response = requests.get(url, headers=self.headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                top_search = data.get("top_search", {}).get("words", [])
                
                items = []
                for word in top_search[:10]:
                    items.append({
                        "title": word.get("query", ""),
                        "display_query": word.get("display_query", "")
                    })
                
                if items:
                    print(f"✅ 知乎热词: 获取 {len(items)} 条")
                    return items
        except Exception as e:
            print(f"❌ 知乎热词失败: {e}")
        
        # 如果上面失败，返回空列表
        print("⚠️ 知乎数据获取失败，跳过")
        return []
    
    def get_toutiao_hot(self):
        """今日头条热榜"""
        try:
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            response = requests.get(url, headers=self.headers, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                hot_news = data.get("data", [])
                
                items = []
                for news in hot_news[:15]:
                    items.append({
                        "title": news.get("Title", ""),
                        "hot": news.get("HotValue", 0)
                    })
                
                print(f"✅ 今日头条: 获取 {len(items)} 条")
                return items
        except Exception as e:
            print(f"❌ 今日头条失败: {e}")
        return None
    
    def run(self):
        """运行所有平台爬虫"""
        print("=" * 60)
        print("多平台热点数据收集")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 运行所有爬虫
        self.results["weibo"] = self.get_weibo_hot()
        time.sleep(1)  # 避免请求太快
        
        self.results["bilibili"] = self.get_bilibili_hot()
        time.sleep(1)
        
        self.results["toutiao"] = self.get_toutiao_hot()
        time.sleep(1)
        
        self.results["zhihu"] = self.get_zhihu_fallback()
        
        # 统计结果
        print("\n" + "=" * 60)
        print("📊 数据收集统计")
        print("=" * 60)
        
        total_items = 0
        for platform, data in self.results.items():
            if data:
                count = len(data)
                total_items += count
                print(f"{platform:10}: ✅ {count:3} 条数据")
            else:
                print(f"{platform:10}: ❌ 获取失败")
        
        print(f"\n🎯 总计获取: {total_items} 条热点数据")
        
        # 保存数据
        if total_items > 0:
            self.save_data()
        
        return self.results
    
    def save_data(self):
        """保存数据到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"data/hotspot_{timestamp}.json"
        
        data_to_save = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存到: {filename}")

if __name__ == "__main__":
    crawler = MultiPlatformCrawler()
    crawler.run()
