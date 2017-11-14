# bttwo
![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)

使用python3爬取[bttwo](http://www.bttwo.com)全站bt文件
## Usage
使用之前请安装lxml,requests,BeautifulSoup
```
pip3 install lxml requests beautifulsoup4
```
修改bttwo.py文件里的下载路径，运行
```
python3 bttwo.py
```
## Known issue
- [ ] 使用代理并不能有效解决爬取速度过快而导致的爬取出错的问题
## TODO LIST
1. 使用数据库来解决去重问题
2. 尝试不用`sleep`函数解决爬取中断问题
3. 尝试多线程
        
