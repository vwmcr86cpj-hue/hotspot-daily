import requests
import time

platforms = [
    ("微博热搜", "https://weibo.com/ajax/side/hotSearch"),
    ("B站热门", "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"),
    ("今日头条", "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"),
    ("百度热搜", "https://top.baidu.com/board?tab=realtime"),
    ("豆瓣话题", "https://www.douban.com/feed/"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("测试各平台可访问性...")
print("=" * 60)

for name, url in platforms:
    try:
        start = time.time()
        response = requests.get(url, headers=headers, timeout=8)
        cost = (time.time() - start) * 1000
        
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"{status} {name:10} | 状态: {response.status_code:3} | 延迟: {cost:.0f}ms | 大小: {len(response.text)/1024:.1f}KB")
        
        if response.status_code != 200 and response.status_code != 403:
            print(f"   可能可用，需要进一步测试")
            
    except Exception as e:
        print(f"❌ {name:10} | 错误: {str(e)[:30]}")

print("=" * 60)
print("💡 建议：")
print("1. 优先测试状态码200的平台")
print("2. 403/401的平台可以暂时放弃")
print("3. 从最简单的开始，建立信心")
