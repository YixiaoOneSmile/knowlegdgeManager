import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ChromeOptions
import time
import json
import pandas as pd
import requests

papers_info_list = []
one_paper = {}

keyword = "你的query"  # 搜索关键词

# 设置options参数，以开发者模式运行
option = ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])

# 解决报错，设置无界面运行
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# option.add_argument("--headless")
option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
option.add_argument(f'user-agent={user_agent}')

url = "https://kns.cnki.net/kns8s/defaultresult/index?crossids=YSTT4HG0%2CLSTPFY1C%2CJUP3MUPD%2CMPMFIG1A%2CWQ0UVIAA%2CBLZOG7CK%2CEMRPGLPA%2CPWFIRAGL%2CNLBO1Z6R%2CNN3FJMUV&korder=SU&kw=" + str(
    keyword)
driver = webdriver.Edge(option)
driver.get(url)

while (True):
    # 等待新界面加载完毕
    time.sleep(3)
    papers = driver.find_elements(By.XPATH, '//div[@id="gridTable"]//table[@class="result-table-list"]/tbody/tr')
    basestr = '//div[@id="gridTable"]//table[@class="result-table-list"]/tbody/tr'

    for i, li in enumerate(papers):
        # pass
        name = li.find_element(By.CSS_SELECTOR, value='td.name a').text
        name_link = li.find_element(By.CSS_SELECTOR, value='td.name a').get_attribute("href")
        author = li.find_element(By.CSS_SELECTOR, value='td.author').text
        source = li.find_element(By.CSS_SELECTOR, value='td.source a').text
        source_link = li.find_element(By.CSS_SELECTOR, value='td.source a').get_attribute("href")
        print(source_link)
        date = li.find_element(By.CSS_SELECTOR, value='td.date').text  # 发表日期
        data = li.find_element(By.CSS_SELECTOR, value='td.data').text  # 数据库来源
        try:
            quote = li.find_element(By.CSS_SELECTOR, value='td.quote').text
        except:
            quote = None
        try:
            downloadCount = li.find_element(By.CSS_SELECTOR, value='td.download').text
        except:
            downloadCount = None
        try:
            operat = li.find_element(By.CSS_SELECTOR, value='td.operat a.downloadlink.icon-download')
            href = operat.get_attribute("href")  # caj下载链接
        except:
            href = None

        print("\n\n\n")
        print("文章名称：", name)  # 文章名字
        print("作者：", author)  # 作者名字
        print("文章来源：", source)  # 文章来源
        # print(source_link) # 期刊链接
        print("发表日期：", date)  # 发表日期
        print("数据库：", data)  # 数据库
        if quote: print("被引次数: ", quote)  # 引用次数
        if downloadCount: print("下载次数: ", downloadCount)  # 下载次数


        # 查看文章详细信息
        new_driver = webdriver.Chrome(option)
        new_driver.get(name_link)
        try:
            institute = new_driver.find_element(By.CSS_SELECTOR, value='div.brief h3:nth-last-child(1)').text  # 机构信息
        except:
            institute = "无机构信息"
        print("机构: ", institute)
        try:
            infos = new_driver.find_elements(By.CSS_SELECTOR, value='div.doc-top div.row')
        except:
            infos = []
        for info in infos:
            print(info.text.strip())  # 摘要、关键词等信息

        try:
            pdf_link = new_driver.find_element(By.CSS_SELECTOR, value='#pdfDown').get_attribute("href")
        except:
            pdf_link = ""
        print("pdf下载地址: ", pdf_link) # pdf下载地址，该pdf地址似乎直接复制到浏览器会报错说应用来源错误...，所以下面直接点击按钮实现自动下载pdf
        text = requests.get(pdf_link)
        with open('./pdf/' + name + '.pdf', 'wb') as f:
            f.write(text.content)
        f.close()

        time.sleep(3)  # 等待页面加载完毕
        new_driver.find_element(By.CSS_SELECTOR, value='#pdfDown').click()
        time.sleep(3)  # 等待pdf下载完毕

        # 查看期刊详细信息
        new_driver2 = webdriver.Chrome(option)
        new_driver2.get(source_link)
        # infobox = new_driver.find_element(By.XPATH, '//*[@id="qk"]//dd[@class="infobox"]')
        try:
            new_driver2.find_element(By.XPATH, '//a[@id="J_sumBtn-stretch"]').click()  # 展开详细信息
        except:
            pass  # 无需展开
        try:
            listbox = new_driver2.find_element(By.XPATH, '//dd[@class="infobox"]/div[@class="listbox clearfix"]')
            text = listbox.text
        except:
            text = "本期刊缺乏信息"
        print("--------本期刊详细信息---------")
        print("期刊名：", source)
        print(text)  # 期刊详细信息
        new_driver2.quit()
        new_driver.quit()

    # 模拟点击下一页
    try:
        driver.find_element(By.XPATH, '//*[@id="PageNext"]').click()
    except:
        break

driver.quit()

