"""
B站热点数据收集
包含：热门视频排行榜、热搜词
"""
import requests
import json
from datetime import datetime
import time

class BilibiliCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com"
        }
        
    def get_ranking(self, rid=0, day=3, page_size=20):
        """
        获取B站排行榜
        Args:
            rid: 分区ID (0:全站, 1:动画, 3:音乐, 4:游戏, 5:娱乐, 36:科技, 160:生活, 119:鬼畜, 129:舞蹈)
            day: 1(日榜), 3(三日榜), 7(周榜)
            page_size: 每页数量
        """
        url = "https://api.bilibili.com/x/web-interface/ranking/v2"
        params = {
            "rid": rid,
            "type": "all",
            "day": day,
            "page_size": page_size
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 获取B站排行榜 (分区: {rid})...")
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 0:
                    videos = data.get("data", {}).get("list", [])
                    
                    result = []
                    for i, video in enumerate(videos[:page_size], 1):
                        video_info = {
                            "rank": i,
                            "bvid": video.get("bvid", ""),
                            "title": video.get("title", ""),
                            "url": f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                            "up": video.get("owner", {}).get("name", ""),
                            "duration": video.get("duration", 0),  # 秒
                            "view": video.get("stat", {}).get("view", 0),
                            "danmaku": video.get("stat", {}).get("danmaku", 0),
                            "like": video.get("stat", {}).get("like", 0),
                            "coin": video.get("stat", {}).get("coin", 0),
                            "favorite": video.get("stat", {}).get("favorite", 0),
                            "share": video.get("stat", {}).get("share", 0),
                            "reply": video.get("stat", {}).get("reply", 0),
                            "category": self._get_category_name(rid)
                        }
                        result.append(video_info)
                    
                    print(f"✅ 获取到 {len(result)} 个热门视频")
                    return result
                else:
                    print(f"⚠️ API返回错误: {data.get('message', '未知错误')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 获取失败: {e}")
        
        return []
    
    def get_hot_search(self):
        """获取B站热搜榜"""
        url = "https://app.bilibili.com/x/v2/search/trending/ranking"
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 获取B站热搜...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 0:
                    hot_words = data.get("data", {}).get("list", [])
                    
                    result = []
                    for i, word in enumerate(hot_words[:20], 1):
                        word_info = {
                            "rank": i,
                            "keyword": word.get("keyword", ""),
                            "show_name": word.get("show_name", ""),
                            "url": f"https://search.bilibili.com/all?keyword={word.get('keyword', '')}",
                            "icon": word.get("icon", ""),
                            "heat": word.get("heat", 0)
                        }
                        result.append(word_info)
                    
                    print(f"✅ 获取到 {len(result)} 个热搜词")
                    return result
                else:
                    print(f"⚠️ 热搜API错误: {data.get('message', '未知错误')}")
            else:
                print(f"❌ 热搜请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 热搜获取失败: {e}")
        
        return []
    
    def _get_category_name(self, rid):
        """根据分区ID获取分区名称"""
        categories = {
            0: "全站",
            1: "动画",
            3: "音乐",
            4: "游戏",
            5: "娱乐",
            36: "科技",
            119: "鬼畜",
            129: "舞蹈",
            155: "时尚",
            160: "生活",
            168: "国创",
            188: "数码"
        }
        return categories.get(rid, f"分区{rid}")
    
    def save_to_file(self, data, filename_prefix="bilibili"):
        """保存数据到JSON文件"""
        if not data:
            print("⚠️ 没有数据可保存")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/{filename_prefix}_{timestamp}.json"
        
        os.makedirs("data", exist_ok=True)
        
        save_data = {
            "platform": "bilibili",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存到: {filename}")
        return filename

def test_bilibili():
    """测试B站爬虫"""
    print("=" * 60)
    print("B站爬虫测试")
    print("=" * 60)
    
    crawler = BilibiliCrawler()
    
    # 1. 测试全站热门
    print("\n1. 测试全站热门视频:")
    videos = crawler.get_ranking(rid=0, page_size=10)
    
    if videos:
        print("\n🏆 热门视频TOP5:")
        for video in videos[:5]:
            view_str = f"{video['view']:,}" if video['view'] < 10000 else f"{video['view']/10000:.1f}万"
            print(f"{video['rank']:2d}. {video['title'][:30]:30}...")
            print(f"     UP: {video['up'][:10]:10} 👀{view_str:>8} 👍{video['like']:,}")
    
    time.sleep(2)
    
    # 2. 测试热搜
    print("\n2. 测试热搜榜:")
    hot_search = crawler.get_hot_search()
    
    if hot_search:
        print("\n🔥 热搜TOP5:")
        for item in hot_search[:5]:
            print(f"{item['rank']:2d}. {item['keyword'][:20]}")
    
    # 3. 保存数据
    if videos or hot_search:
        all_data = {
            "ranking": videos,
            "hot_search": hot_search
        }
        crawler.save_to_file(all_data, "bilibili_full")
        
        print("\n" + "=" * 60)
        print("🎯 B站爬虫测试完成！")
        if videos:
            print(f"  热门视频: {len(videos)} 个")
        if hot_search:
            print(f"  热搜词: {len(hot_search)} 个")
    else:
        print("\n❌ B站爬虫测试失败")
    
    return videos or hot_search

if __name__ == "__main__":
    import os
    test_bilibili()
