"""
GitHub Trending数据收集
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import re

class GitHubTrendingCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
    
    def get_trending(self, language="", since="daily"):
        """
        获取GitHub Trending
        Args:
            language: 编程语言，如"python", "javascript", "go"
            since: daily, weekly, monthly
        """
        if language:
            url = f"https://github.com/trending/{language}?since={since}"
        else:
            url = f"https://github.com/trending?since={since}"
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 获取GitHub Trending ({language or 'all'}/{since})...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                repos = []
                
                for article in soup.select('article.Box-row'):
                    repo_info = self._parse_repo_element(article)
                    if repo_info:
                        repo_info["language"] = language or "all"
                        repo_info["period"] = since
                        repos.append(repo_info)
                
                print(f"✅ 获取到 {len(repos)} 个热门仓库")
                return repos
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 获取失败: {e}")
        
        return []
    
    def _parse_repo_element(self, article):
        """解析单个仓库元素"""
        try:
            # 仓库标题和链接
            title_elem = article.select_one('h2 a')
            if not title_elem:
                return None
                
            title = title_elem.get_text(strip=True)
            repo_url = f"https://github.com{title_elem.get('href', '')}"
            
            # 提取作者和仓库名
            author, repo_name = "", ""
            if "/" in title:
                parts = title.split("/")
                if len(parts) >= 2:
                    author = parts[0].strip()
                    repo_name = parts[1].strip()
            
            # 描述
            desc_elem = article.select_one('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # 编程语言
            lang_elem = article.select_one('span[itemprop="programmingLanguage"]')
            language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
            
            # 星标数
            stars_text = "0"
            stars_elem = article.select('a[href$="/stargazers"]')
            if stars_elem:
                stars_text = stars_elem[0].get_text(strip=True)
            
            # forks数
            forks_text = "0"
            forks_elem = article.select('a[href$="/forks"]')
            if forks_elem:
                forks_text = forks_elem[0].get_text(strip=True)
            
            # 今日星标增长
            stars_today_text = ""
            stars_today_elem = article.select('span.d-inline-block.float-sm-right')
            if stars_today_elem:
                stars_today_text = stars_today_elem[0].get_text(strip=True)
                # 提取数字
                match = re.search(r'(\d+[,]?\d*)', stars_today_text)
                if match:
                    stars_today_text = match.group(1).replace(',', '')
            
            return {
                "title": title,
                "author": author,
                "repo_name": repo_name,
                "url": repo_url,
                "description": description,
                "language": language,
                "stars": self._parse_number(stars_text),
                "forks": self._parse_number(forks_text),
                "stars_today": stars_today_text,
                "platform": "GitHub"
            }
            
        except Exception as e:
            print(f"解析仓库失败: {e}")
            return None
    
    def _parse_number(self, text):
        """解析数字文本，如1.2k -> 1200"""
        if not text:
            return 0
        
        text = text.replace(',', '').strip()
        
        if 'k' in text.lower():
            try:
                return int(float(text.lower().replace('k', '')) * 1000)
            except:
                return 0
        else:
            try:
                return int(text)
            except:
                return 0
    
    def get_multiple_languages(self, languages=None, since="daily"):
        """获取多个编程语言的Trending"""
        if languages is None:
            languages = ["", "python", "javascript", "java", "go", "rust"]
        
        all_repos = []
        
        for lang in languages:
            repos = self.get_trending(language=lang, since=since)
            all_repos.extend(repos)
            if lang != languages[-1]:  # 不是最后一个
                time.sleep(2)  # 避免请求太快
        
        return all_repos
    
    def save_to_file(self, data, filename_prefix="github_trending"):
        """保存数据到JSON文件"""
        if not data:
            print("⚠️ 没有数据可保存")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/{filename_prefix}_{timestamp}.json"
        
        os.makedirs("data", exist_ok=True)
        
        save_data = {
            "platform": "github",
            "timestamp": datetime.now().isoformat(),
            "period": data[0].get("period", "daily") if data else "daily",
            "data": data
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存到: {filename}")
        return filename

def test_github_trending():
    """测试GitHub Trending爬虫"""
    print("=" * 60)
    print("GitHub Trending爬虫测试")
    print("=" * 60)
    
    crawler = GitHubTrendingCrawler()
    
    # 1. 测试全站热门
    print("\n1. 测试全站热门仓库:")
    repos = crawler.get_trending(since="daily")
    
    if repos:
        print(f"\n🏆 GitHub Trending TOP5:")
        for i, repo in enumerate(repos[:5], 1):
            print(f"{i:2d}. {repo['title'][:40]:40}")
            print(f"     {repo['description'][:50]:50}")
            print(f"     语言: {repo['language']:10} 星标: {repo['stars']:,} 今日: +{repo['stars_today']}")
    
    time.sleep(2)
    
    # 2. 测试Python语言
    print("\n2. 测试Python语言热门:")
    python_repos = crawler.get_trending(language="python", since="daily")
    
    if python_repos:
        print(f"\n🐍 Python热门TOP3:")
        for i, repo in enumerate(python_repos[:3], 1):
            print(f"{i:2d}. {repo['title'][:30]}")
    
    # 3. 保存数据
    if repos:
        crawler.save_to_file(repos, "github_trending_daily")
        
        print("\n" + "=" * 60)
        print("🎯 GitHub Trending爬虫测试完成！")
        print(f"   获取仓库: {len(repos)} 个")
        if python_repos:
            print(f"   Python仓库: {len(python_repos)} 个")
    else:
        print("\n❌ GitHub Trending爬虫测试失败")
    
    return repos

if __name__ == "__main__":
    import os
    test_github_trending()
