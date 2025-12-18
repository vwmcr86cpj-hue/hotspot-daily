"""
今日头条热点数据收集
"""
import requests
import json
from datetime import datetime
import time

class ToutiaoCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.toutiao.com",
            "Origin": "https://www.toutiao.com"
        }
    
    def get_hot_board(self, limit=20):
        """获取头条热榜"""
        url = "https://www.toutiao.com/hot-event/hot-board/"
        params = {
            "origin": "toutiao_pc"
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 获取今日头条热榜...")
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("message") == "success":
                    hot_news = data.get("data", [])
                    
                    result = []
                    for i, news in enumerate(hot_news[:limit], 1):
                        news_info = {
                            "rank": i,
                            "id": news.get("ClusterId", ""),
                            "title": news.get("Title", ""),
                            "url": news.get("Url", ""),
                            "hot_value": news.get("HotValue", 0),
                            "label": news.get("Label", ""),
                            "label_style": news.get("LabelStyle", ""),
                            "query_word": news.get("QueryWord", ""),
                            "heat": self._format_heat(news.get("HotValue", 0)),
                            "platform": "Toutiao"
                        }
                        result.append(news_info)
                    
                    print(f"✅ 获取到 {len(result)} 条热榜新闻")
                    return result
                else:
                    print(f"⚠️ API返回错误: {data.get('message', '未知错误')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 获取失败: {e}")
        
        return []
    
    def _format_heat(self, hot_value):
        """格式化热度值"""
        if hot_value >= 100000000:
            return f"{hot_value/100000000:.1f}亿"
        elif hot_value >= 10000:
            return f"{hot_value/10000:.1f}万"
        else:
            return str(hot_value)
    
    def get_hot_video(self):
        """获取头条热门视频（备用）"""
        url = "https://www.toutiao.com/api/pc/list/feed"
        params = {
            "category": "pc_profile_hot",
            "max_behot_time": int(time.time()),
            "aid": 24
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 获取头条热门视频...")
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get("data", [])
                
                result = []
                for video in videos[:10]:
                    if video.get("article_type") == 1:  # 视频类型
                        video_info = {
                            "title": video.get("title", ""),
                            "url": f"https://www.toutiao.com/video/{video.get('item_id', '')}",
                            "play_count": video.get("video_detail_info", {}).get("video_watch_count", 0),
                            "digg_count": video.get("digg_count", 0),
                            "comment_count": video.get("comment_count", 0)
                        }
                        result.append(video_info)
                
                if result:
                    print(f"✅ 获取到 {len(result)} 个热门视频")
                return result
            else:
                print(f"❌ 视频请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 视频获取失败: {e}")
        
        return []
    
    def save_to_file(self, data, filename_prefix="toutiao"):
        """保存数据到JSON文件"""
        if not data:
            print("⚠️ 没有数据可保存")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/{filename_prefix}_{timestamp}.json"
        
        os.makedirs("data", exist_ok=True)
        
        save_data = {
            "platform": "toutiao",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存到: {filename}")
        return filename

def test_toutiao():
    """测试今日头条爬虫"""
    print("=" * 60)
    print("今日头条爬虫测试")
    print("=" * 60)
    
    crawler = ToutiaoCrawler()
    
    # 1. 测试热榜
    print("\n1. 测试热榜:")
    hot_news = crawler.get_hot_board(limit=15)
    
    if hot_news:
        print(f"\n🔥 今日头条热榜TOP5:")
        for news in hot_news[:5]:
            heat = f"{news['hot_value']:,}" if news['hot_value'] < 10000 else f"{news['hot_value']/10000:.1f}万"
            label = f"[{news['label']}]" if news['label'] else ""
            print(f"{news['rank']:2d}. {label}{news['title'][:30]:30}... 🔥{heat}")
    
    time.sleep(2)
    
    # 2. 测试热门视频（可选）
    print("\n2. 测试热门视频:")
    hot_videos = crawler.get_hot_video()
    
    if hot_videos:
        print(f"\n🎥 热门视频TOP3:")
        for i, video in enumerate(hot_videos[:3], 1):
            print(f"{i:2d}. {video['title'][:30]}...")
    
    # 3. 保存数据
    if hot_news:
        crawler.save_to_file(hot_news, "toutiao_hot")
        
        print("\n" + "=" * 60)
        print("🎯 今日头条爬虫测试完成！")
        print(f"   热榜新闻: {len(hot_news)} 条")
        if hot_videos:
            print(f"   热门视频: {len(hot_videos)} 个")
    else:
        print("\n❌ 今日头条爬虫测试失败")
    
    return hot_news

if __name__ == "__main__":
    import os
    test_toutiao()
