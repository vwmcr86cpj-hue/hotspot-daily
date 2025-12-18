"""
可工作的爬虫集合 - 优先做能跑通的平台
"""
import requests
import json
from datetime import datetime
import time

def get_bilibili_hot():
    """B站热门 - 通常很稳定"""
    try:
        url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all&page_size=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com"
        }
        
        print("📺 获取B站热门视频...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get("data", {}).get("list", [])
            
            if videos:
                print(f"✅ 获取到 {len(videos)} 个热门视频")
                
                hot_videos = []
                for i, video in enumerate(videos[:10], 1):
                    title = video.get("title", "")
                    play = video.get("stat", {}).get("view", 0)
                    up = video.get("owner", {}).get("name", "")
                    
                    hot_videos.append({
                        "rank": i,
                        "title": title,
                        "play": f"{play:,}",
                        "up": up,
                        "url": f"https://www.bilibili.com/video/{video.get('bvid', '')}"
                    })
                    
                    print(f"{i:2d}. {title[:30]:30}... ��{up[:10]:10} 🔥{play:,}")
                
                return hot_videos
        else:
            print(f"⚠️ B站状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ B站获取失败: {e}")
    
    return []

def get_douyin_trend():
    """抖音热榜/热点（通过API）"""
    try:
        # 抖音的热点API（可能需要特定header）
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Accept": "application/json, text/plain, */*"
        }
        
        print("🎵 尝试获取抖音热点...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hot_words = data.get("data", {}).get("word_list", [])
            
            if hot_words:
                print(f"✅ 获取到 {len(hot_words)} 个抖音热点")
                
                trends = []
                for i, word in enumerate(hot_words[:10], 1):
                    trends.append({
                        "rank": i,
                        "word": word.get("word", ""),
                        "hot": word.get("hot_value", 0)
                    })
                    print(f"{i:2d}. {word.get('word', '')[:20]:20}... 🔥{word.get('hot_value', 0):,}")
                
                return trends
        else:
            print(f"⚠️ 抖音状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 抖音获取失败: {e}")
    
    return []

def get_csdn_hot():
    """CSDN热榜 - 技术社区热点"""
    try:
        url = "https://bizapi.csdn.net/community-cloud/v1/homepage/community/hot"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print("💻 获取CSDN热榜...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("data", {}).get("article", {}).get("list", [])
            
            if articles:
                print(f"✅ 获取到 {len(articles)} 篇热门文章")
                
                hot_articles = []
                for i, article in enumerate(articles[:10], 1):
                    hot_articles.append({
                        "rank": i,
                        "title": article.get("title", ""),
                        "views": article.get("viewCount", 0)
                    })
                    print(f"{i:2d}. {article.get('title', '')[:30]:30}... 👀{article.get('viewCount', 0):,}")
                
                return hot_articles
        else:
            print(f"⚠️ CSDN状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ CSDN获取失败: {e}")
    
    return []

def get_github_trending():
    """GitHub Trending - 开发者热点"""
    try:
        url = "https://github.com/trending"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print("🐙 获取GitHub Trending...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            repos = []
            for article in soup.select('article.Box-row')[:10]:
                title_elem = article.select_one('h2 a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    repos.append({
                        "title": title,
                        "url": f"https://github.com{title_elem.get('href', '')}"
                    })
            
            if repos:
                print(f"✅ 获取到 {len(repos)} 个热门仓库")
                for i, repo in enumerate(repos, 1):
                    print(f"{i:2d}. {repo['title'][:40]:40}...")
                
                return repos
        else:
            print(f"⚠️ GitHub状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ GitHub获取失败: {e}")
    
    return []

def main():
    """运行所有可用的爬虫"""
    print("=" * 60)
    print("可用的热点数据收集")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_data = {}
    
    # 运行B站
    bilibili_data = get_bilibili_hot()
    if bilibili_data:
        all_data["bilibili"] = bilibili_data
    time.sleep(2)
    
    # 运行抖音
    douyin_data = get_douyin_trend()
    if douyin_data:
        all_data["douyin"] = douyin_data
    time.sleep(2)
    
    # 运行CSDN
    csdn_data = get_csdn_hot()
    if csdn_data:
        all_data["csdn"] = csdn_data
    time.sleep(2)
    
    # 运行GitHub
    github_data = get_github_trending()
    if github_data:
        all_data["github"] = github_data
    
    # 保存数据
    if all_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"data/working_data_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "platforms": list(all_data.keys()),
                "total_items": sum(len(v) for v in all_data.values()),
                "data": all_data
            }, f, ensure_ascii=False, indent=2)
        
        print("=" * 60)
        print(f"📊 成功获取 {len(all_data)} 个平台数据")
        print(f"💾 数据已保存到: {filename}")
        print("🎯 MVP验证成功！至少有一个平台可以工作")
    else:
        print("=" * 60)
        print("❌ 所有平台都失败了")
        print("💡 这可能意味着：")
        print("1. Codespaces IP被多数平台限制")
        print("2. 需要更换爬取策略")
        print("3. 考虑使用其他数据源")

if __name__ == "__main__":
    main()
