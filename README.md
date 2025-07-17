# GetProxy
自动爬免费代理IP（国内IP），并自动验证连通性

获取结果会保存在"proxy_results_test.txt"

需要修改获取数量：在117行调整页码
为避免反爬机制，从网站获取IP时未设多线程

-
免费代理IP是第三方代理服务器，收集自互联网，并非作者所有，作者不对免费代理IP的有效性负责。
-
请合法使用开放代理IP，由用户使用开放代理IP带来的法律责任与作者无关。
-
若开放代理IP侵犯了您的权益，请及时告知作者（Issue），作者将在第一时间删除。

重点来了！！！！！！！！！
4.2.3 开源 ip代理池—ProxyPool（吐血推荐）
类比线程池，进程池，懂了吧？
这是俺发现的一个不错的开源 ip 代理池ProxyPool，可以用windows系统的，至少Python3.5以上环境哟，还需要将Redis服务开启。

现成的代理池，还不用起来？

ProxyPool下载地址：

https://github.com/Python3WebSpider/ProxyPool.git

（可以手动下载也可以使用git下来。）

1.ProxyPool的使用：
<img width="1489" height="887" alt="image" src="https://github.com/user-attachments/assets/84e67754-942e-48e2-8ed4-da810afa92ba" />


首先使用 git clone 将源代码拉到你本地，
在这里插入图片描述
3.进入proxypool目录，修改settings.py文件，PASSWORD为Redis密码，如果为空，则设置为None。（新装的redis一般没有密码。）

(如果你没 redis 的话，可以先去下载了安装了再来看吧。)

（假设你的redis已经安装完成。）

4.接着在你 clone 下来的文件目录中（就是这个ProxyPool存的电脑路径 ）

5.安装相关所需的 依赖包：
（pip或pip3）

pip install -r requirements.txt
 
AI写代码
python
运行
（如果你把ProxyPool导入在pycharm里面，那就一切都在pycharm里面搞就可以了。
<img width="323" height="264" alt="image" src="https://github.com/user-attachments/assets/1f4b51d9-cc69-4c65-b179-3dea1742eb1e" />

在这里插入图片描述
6.接下来开启你的 redis服务，
<img width="1213" height="704" alt="image" src="https://github.com/user-attachments/assets/f473ff40-9b6d-42bc-b224-d9a53c745e4e" />

直接cmd 打开dos窗口，运行：redis-server.exe
即可开启redis服务器。redis 的默认端口就是 6379
在这里插入图片描述
7.接着就可以运行 run.py 了。

可以在cmd里面命令方式运行，也可以导入pycharm里面运行。

图示：
<img width="1073" height="717" alt="image" src="https://github.com/user-attachments/assets/d43da986-fde5-45d5-9458-3246a16d4a7f" />

在这里插入图片描述
8.运行 run.py 以后，你可以打开你的redis管理工具，或者进入redis里面查看，这时候在你的 redis 中就会存入很多已经爬取到的代理 ip 了：
<img width="1271" height="658" alt="image" src="https://github.com/user-attachments/assets/d8a3ee5a-af1e-4841-b8f1-2243a7e88e80" />

在这里插入图片描述
9.项目跑起来之后，【不要停止】，此时redis里面存了ip，就可以访问这个代理池了。

在上面的图中，可以看到有这么一句话

Running on http://0.0.0.0:5555/ (Press CTRL+C to quit)
这就是告诉我们随机访问地址URL是多少。
10.在浏览器中随机获取一个代理 ip 地址：

你就浏览器输入：

http://0.0.0.0:5555/random

<img width="949" height="231" alt="image" src="https://github.com/user-attachments/assets/d03ba8b0-6de7-4457-959b-2522539932e1" />

在这里插入图片描述
11.在代码中随机获取一个ip代理

就这样：
import requests
# 随机ip代理获取
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response 
