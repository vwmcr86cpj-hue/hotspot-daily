import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_weibo_hot():
    """微博热搜测试（相对简单）"""
    url = "https://s.weibo.com/top/summary"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": "",  # 可以留空试试
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    }
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 测试微博热搜...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 微博热搜通常在<td>标签中
            hot_items = []
            
            # 方法1：查找热搜列表
            for td in soup.find_all('td', class_='td-02'):
                link = td.find('a')
                if link and link.text.strip():
                    title = link.text.strip()
                    href = link.get('href', '')
                    
                    # 提取热度
                    span = td.find('span')
                    hot = span.text if span else ''
                    
                    hot_items.append({
                        'title': title,
                        'url': f"https://s.weibo.com{href}" if href.startswith('/') else href,
                        'hot': hot
                    })
            
            if hot_items:
                print(f"✅ 成功获取 {len(hot_items)} 条微博热搜")
                for i, item in enumerate(hot_items[:10], 1):
                    print(f"{i}. {item['title'][:20]}... {item['hot']}")
                return True
            else:
                # 方法2：尝试其他选择器
                print("⚠️ 方法1失败，尝试其他选择器...")
                
                # 微博可能用其他结构
                for a in soup.find_all('a'):
                    href = a.get('href', '')
                    if '/weibo?q=' in href and a.text.strip():
                        print(f"  备选: {a.text[:20]}...")
                
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 微博热搜获取失败: {e}")
        return False

if __name__ == "__main__":
    success = get_weibo_hot()
    if success:
        print("\n🎯 微博热搜测试成功！")
    else:
        print("\n🔧 建议：")
        print("1. 检查网络是否可以访问微博")
        print("2. 可能需要更新选择器")
