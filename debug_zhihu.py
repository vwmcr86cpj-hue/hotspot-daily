import requests
import json

url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
params = {"limit": 5}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {response.headers.get('content-type')}")
    
    # 尝试解析JSON
    data = response.json()
    
    print("\n=== 完整的API返回数据（前500字符）===")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
    
    print("\n=== 数据结构分析 ===")
    print(f"返回数据的键: {list(data.keys())}")
    
    # 检查不同可能的字段
    if "data" in data:
        print("✅ 找到 'data' 字段")
    elif "hotList" in data:
        print("✅ 找到 'hotList' 字段")
    elif "list" in data:
        print("✅ 找到 'list' 字段")
    else:
        print("�� 检查第一层数据结构:")
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                print(f"  {key}: 类型={type(value)}, 长度={len(value) if hasattr(value, '__len__') else 'N/A'}")
    
except Exception as e:
    print(f"错误: {e}")
    print(f"原始响应文本（前200字符）: {response.text[:200]}")
