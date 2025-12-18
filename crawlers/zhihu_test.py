import requests
import json
from datetime import datetime

def test_zhihu():
    """测试知乎热榜API"""
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    params = {"limit": 5}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始测试知乎热榜...")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "data" in data:
            hot_items = data["data"]
            print(f"✅ 成功获取 {len(hot_items)} 条热榜数据")
            
            for i, item in enumerate(hot_items[:3], 1):
                title = item.get("target", {}).get("title", "无标题")
                hot = item.get("detail_text", "未知热度")
                print(f"{i}. {title[:20]}... ({hot})")
            return True
        else:
            print("❌ 未找到有效数据")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

if __name__ == "__main__":
    success = test_zhihu()
    if success:
        print("\n🎯 测试通过！可以开始正式开发了。")
    else:
        print("\n⚠️ 测试失败，请检查网络或API变更。")
