import requests
import re
import json
from datetime import datetime
import time

def get_zhihu_billboard():
    """
    知乎热榜网页版爬虫
    访问 https://www.zhihu.com/billboard 提取数据
    """
    url = "https://www.zhihu.com/billboard"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始抓取知乎热榜网页...")
    
    try:
        # 添加延时，避免请求太快
        time.sleep(2)
        
        response = requests.get(url, headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        print(f"页面大小: {len(response.text)/1024:.1f}KB")
        
        if response.status_code == 200:
            html = response.text
            
            # 方法1：正则匹配JSON数据
            # 知乎热榜数据在 <script id="js-initialData"> 标签中
            pattern = r'<script id="js-initialData" type="text/json">(.*?)</script>'
            matches = re.findall(pattern, html, re.DOTALL)
            
            if matches:
                print("✅ 找到热榜数据")
                json_str = matches[0]
                
                try:
                    data = json.loads(json_str)
                    
                    # 知乎热榜的嵌套路径
                    hot_list = data.get('initialState', {}).get('topstory', {}).get('hotList', [])
                    
                    if not hot_list:
                        # 尝试其他可能的路径
                        hot_list = data.get('initialState', {}).get('billboard', {}).get('hotList', [])
                    
                    if not hot_list:
                        # 尝试搜索整个数据结构
                        def find_hotlist(obj, depth=0):
                            if depth > 3:  # 防止递归太深
                                return None
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    if 'hot' in key.lower() and isinstance(value, list):
                                        return value
                                    result = find_hotlist(value, depth+1)
                                    if result:
                                        return result
                            elif isinstance(obj, list):
                                for item in obj[:5]:  # 只检查前几项
                                    result = find_hotlist(item, depth+1)
                                    if result:
                                        return result
                            return None
                        
                        hot_list = find_hotlist(data)
                    
                    if hot_list and isinstance(hot_list, list):
                        print(f"🎉 成功解析到 {len(hot_list)} 条热榜数据")
                        
                        # 输出前10条
                        for i, item in enumerate(hot_list[:10], 1):
                            if isinstance(item, dict):
                                # 提取标题
                                target = item.get('target', {})
                                title = target.get('title', item.get('title', '无标题'))
                                
                                # 提取热度
                                hot = item.get('detailText', item.get('detail_text', ''))
                                if not hot:
                                    hot = item.get('metrics', {}).get('area', {}).get('text', '')
                                
                                # 提取链接
                                link = f"https://www.zhihu.com/question/{target.get('id', '')}" if target.get('id') else ''
                                
                                print(f"{i:2d}. {title[:30]:30}... 热度: {hot}")
                        
                        return hot_list
                    else:
                        print("⚠️ 未找到热榜列表结构")
                        
                        # 保存HTML用于调试
                        with open('zhihu_debug.html', 'w', encoding='utf-8') as f:
                            f.write(html[:5000])
                        print("📁 已保存HTML片段到 zhihu_debug.html")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析错误: {e}")
                    print(f"JSON片段: {json_str[:200]}")
            else:
                print("❌ 未找到热榜数据标签")
                
                # 尝试搜索热榜关键词
                if '热榜' in html or 'HotList' in html:
                    print("💡 页面包含热榜关键词，但未找到结构化数据")
                    
                # 保存HTML用于分析
                with open('zhihu_full.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print("📁 已保存完整HTML到 zhihu_full.html")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 抓取失败: {type(e).__name__}: {e}")
    
    return []

if __name__ == "__main__":
    print("=" * 60)
    print("知乎热榜网页版爬虫 v1.0")
    print("=" * 60)
    
    results = get_zhihu_billboard()
    
    if results:
        print(f"\n✅ 总共获取到 {len(results)} 条热榜数据")
        print("🎯 知乎热榜爬取成功！")
    else:
        print("\n❌ 知乎热榜爬取失败")
        print("💡 建议：")
        print("1. 检查网络是否可以正常访问 https://www.zhihu.com/billboard")
        print("2. 尝试更换User-Agent")
        print("3. 添加必要的Cookie（如果需要）")
        print("4. 先试试其他平台（微博/B站）")
