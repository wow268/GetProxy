import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
import json
import concurrent.futures
from datetime import datetime

class ProxyCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.results = []

    # 修改为实例方法，并修正代理格式处理
    def check_proxy(self, proxy_str):
        ip, port = proxy_str.split(':')
        proxy_dict = {
            'ip': ip,
            'port': port,
            'proxy_str': proxy_str
        }
        
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }
    
        try:
            # 测试访问百度（超时设置为5秒）
            response = requests.get(
                'http://www.baidu.com', 
                proxies=proxies, 
                timeout=5
            )
            if response.status_code == 200:
                proxy_dict['status'] = 'OK'
            else:
                proxy_dict['status'] = 'NG'
        except:
            proxy_dict['status'] = 'NG'
    
        return proxy_dict

    def get_agent(self):
        return self.ua.random

    def request_get_url(self, url, tag, retry=3):
        delay = random.uniform(1, 5)
        headers = {'User-Agent': self.get_agent()}
        
        try:
            response = requests.get(f"{url}{tag}", headers=headers, timeout=10)
            response.raise_for_status()
            self.parse_doc(response.text)
            return True
            
        except Exception as e:
            if retry > 0:
                time.sleep(delay)
                return self.request_get_url(url, tag, retry-1)
            print(f"请求失败: {e}")
            return False

    def parse_doc(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if 'fpsList' in script.text:    
                start = script.text.find('fpsList = [') + len('fpsList = ')
                end = script.text.find('];', start) + 1
                json_data = script.text[start:end]
                proxy_list = json.loads(json_data)
                for proxy in proxy_list:
                    ip = proxy['ip']
                    port = proxy['port']
                    if ip and port:
                        self.results.append(f"{ip}:{port}")

    def save_results(self, proxies, filename):
        # 筛选出可用的代理（status == 'OK'）
        working_proxies = [proxy for proxy in proxies if proxy['status'] == 'OK']

        with open(filename, 'w') as f:
            # 写入头部信息
            f.write(f"代理验证结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n")
            
            for proxy in working_proxies:
                f.write(f"{proxy['proxy_str']} - {proxy['status']}\n")

            # 统计信息
            ok_count = sum(1 for p in proxies if p['status'] == 'OK')
            f.write("\n" + "="*50 + "\n")
            f.write(f"Total: {len(proxies)} proxies\n")
            f.write(f"AVL: {ok_count} \n")
            f.write(f"N/A: {len(proxies)-ok_count} \n")
            f.write(f"Rate: {ok_count/len(proxies)*100:.1f}%\n")

    def crawl(self):
        base_url = "https://www.kuaidaili.com/free/inha/"
        # 页号 1-11
        for page in range(1, 11):
            success = self.request_get_url(base_url, str(page))
            if not success:
                break
            time.sleep(random.uniform(1, 3))
        
        # 保存原始结果
        with open('proxy_results.txt', 'w') as f:
            f.write('\n'.join(self.results))

        print(f"成功抓取 {len(self.results)} 个代理IP，正在验证连通性。。。")

        # 使用线程池并发验证（最多10个线程）
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 使用lambda将实例方法绑定到当前对象
            checked_proxies = list(executor.map(lambda p: self.check_proxy(p), self.results))
    
        # 打印结果
        for proxy in checked_proxies:
            print(f"IP: {proxy['proxy_str']} - {proxy['status']}")
    
        # 保存结果到文件
        self.save_results(checked_proxies, 'proxy_results_test.txt')
        print("\n测试结果已保存到 proxy_results_test.txt")
    
        # 统计可用代理数量
        ok_count = sum(1 for p in checked_proxies if p['status'] == 'OK')
        print(f"\n可用代理: {ok_count}/{len(checked_proxies)}，输入回车确认")

if __name__ == "__main__":
    print(f"获取中，请等待。。。")
    crawler = ProxyCrawler()
    crawler.crawl()
    input()