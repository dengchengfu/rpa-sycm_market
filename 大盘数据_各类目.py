import pyautogui
import random
import time
import webbrowser
import os
import pyperclip
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import datetime
import time
import calendar
pyautogui.FAILSAFE = True

def getDayList():
    #Set time
    today = datetime.date.today()
    print("今天是：" + str(today))
    need_day= int(input("是否下载昨天（是输入1, 否输入0）："))

    if need_day == 0:
        start_d = input("开始日期（输入格式 YYYY-MM-DD）：")
        end_d = input("结束日期（输入格式 YYYY-MM-DD）：")
        date_list = []
        #将日期字符串转成datetime日期格式
        datestart=datetime.datetime.strptime(start_d,'%Y-%m-%d')
        dateend=datetime.datetime.strptime(end_d,'%Y-%m-%d')
        #将datetime日期格式转成字符串
        date_list.append(datestart.strftime('%Y-%m-%d'))
        while datestart < dateend:
            # 日期叠加一天
            datestart += datetime.timedelta(days=+1)
            # 日期转字符串存入列表
            date_list.append(datestart.strftime('%Y-%m-%d'))
    else:
        today = datetime.date.today()
        date_list = []
        date_list.append(str(today + datetime.timedelta(days=-1)))

    return date_list


def getMonthList():
    need_month = int(input("是否下载多月数据?（是输入1, 否输入0）："))

    if need_month == 1:
        year_month = []
        start_m = input("开始年月（输入格式 YYYY-MM）：") + '-01'
        end_m = input("结束年月（输入格式 YYYY-MM）：") + '-01'

        monthstart=datetime.datetime.strptime(start_m,'%Y-%m-%d')
        monthend=datetime.datetime.strptime(end_m,'%Y-%m-%d')
        #初始值录入
        month = monthstart.month
        year = monthstart.year
        year_month.append((year,month))

        #剩余全部数值陆续填充
        compare_year = 1 if monthstart.year < monthend.year else 0
        diff_year = monthend.year - monthstart.year
        month_max = 12*diff_year if compare_year == 1 else monthend.month

        while month < month_max:
            month += 1
            if month%12 == 0:
                year = monthstart.year
                year_month.append((year,12))
                continue
            year = monthstart.year + month//12
            year_month.append((year,month%12))

        if compare_year:
            month = 1
            year_month.append((monthend.year,month))
            while month < monthend.month:
                month += 1
                year_month.append((monthend.year,month))
    else:
        year_month = []
        start_m = input("输入年月（输入格式 YYYY-MM）：") + '-01'
        monthstart = datetime.datetime.strptime(start_m,'%Y-%m-%d')
        year = monthstart.year
        month = monthstart.month
        year_month.append((year,month))

    return year_month


def MonthDay(year,month):
    month_start = datetime.datetime(year, month, 1)
    start_day = month_start.strftime("%Y-%m-%d")
    
    month_end = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    start_end = month_end.strftime("%Y-%m-%d")
    return (start_day,start_end)

def get_url_daily():
    urls = []
    datelist = getDayList()
    for date in datelist:
        for cat in catId.keys():
            query_dict ={
             'activeKey': 'shop',
             'cateFlag': '2',
             'cateId': cat,
             'dateRange': date +"|"+ date,
             'dateType': 'day',
             'sellerType': '1'}
            new_query = urlencode(query_dict, doseq=True)
            url = base_url + new_query
            urls.append(url)
    return urls

def get_url_monthly():
    urls = []
    year_month = getMonthList()
    for i in year_month:
        for cat in catId.keys():
            query_dict ={
             'activeKey': 'shop',
             'cateFlag': '2',
             'cateId': cat,
             'dateRange': str(MonthDay(i[0],i[1])[0])+"|"+ str(MonthDay(i[0],i[1])[1]),
             'dateType': 'month',
             'sellerType': '1'}
            new_query = urlencode(query_dict, doseq=True)
            url = base_url + new_query
            urls.append(url)
    return urls


def download_gmv(url):
    # 打开网页
    webbrowser.open(url)
    pyautogui.sleep(10)

    # 一键转化的位置
    pyautogui.moveTo(717, 317, duration=0.25)
    pyautogui.click()
    pyautogui.sleep(2.5)

    # 阿明工具导出文件的位置
    pyautogui.moveTo(1098, 490, duration=0.25)
    pyautogui.click()
    pyautogui.sleep(1)

    # 关闭网页
    pyautogui.hotkey('command', 'w')

    pyautogui.sleep(0.5)

#-----------------------爬取入口---------------------
if __name__ == '__main__':
    catId = {
        "1801": "美容护肤/美体/精油",
        "50010788": "彩妆/香水/美妆工具",
        "50010794": "睫毛膏/睫毛增长液" ,
        "50010798": "眉笔/眉粉/眉膏",
        "50010797": "眼线",
        "50010796": "眼影",
        "201161605": "彩妆套装",
        "50010808": "唇膏/口红",
        "50010807": "唇彩/唇蜜/唇釉",
        "50010803": "遮瑕",
        "50010805": "腮红/胭脂" ,
        "50010792": "蜜粉/散粉",
        "50010790": "粉饼",
        "50010789": "粉底液/膏",
        "50013794": "BB霜",
        "121382014": "高光",
        "121426007": "隔离/妆前",
        "201310801": "定妆喷雾",
        "201173303": "防晒（新）",
        "50011990": "卸妆"
    }

    #设置参数
    base_url = "https://sycm.taobao.com/mc/mq/market_rank?"
    download_path = "/Users/dengchengfu/Downloads/"

    missing_page = []
    urls = []
    count = 0
    dateInput = input("输入时间维度（day or month）: ")
    if dateInput == 'day':
        urls = get_url_daily()
       
    if dateInput == 'month':
        urls = get_url_monthly()

    total = len(urls)
    print("-"*50)
    print("一共需要下载{}页".format(str(total)))
    print("-"*50)

    start = time.time()
    for url in urls:
        parser = urlparse(url)
        query = parser.query
        query_dict = parse_qs(query)

        url_info = "类目:" + catId[query_dict['cateId'][0]] + ", " + "时间:" + query_dict['dateRange'][0]
        count += 1
        print("{}/{}".format(count,total), "开始下载: ", url_info)

        #记录当前文件数
        file_origin_counts = len(os.listdir(download_path))
        download_gmv(url)
        #记录文件下载后的文件数
        file_now_counts = len(os.listdir(download_path))

        #判断文件是否下载成功
        if (file_now_counts - file_origin_counts) == 1:
            print("下载成功: {}".format(url_info))
            print("-"*50)
        else:
            missing_page.append((url_info, url))
            print("下载失败,需要重新下载:")
            print(url_info)
            print(url)
            print("-"*50)

    sucess_urls = total - len(missing_page)
    print("成功下载链接{}个,".format(str(sucess_urls)), "失败下载链接{}个".format(str(len(missing_page))))
    print("下载失败链接如下:")
    for i in range(len(missing_page)):
        print(i+1,missing_page[i][0])
        print(missing_page[i][1])
    print("-"*50)

    #开始重新下载失败链接
    retry_count = 0
    retry_num = 1
    missing_total = len(missing_page)

    while len(missing_page) != 0:
        retry_count += 1
        if retry_num > 1:
            print("{}/{}".format(retry_count,missing_total), "开始重下失败链接,", "第{}次尝试".format(str(retry_num)))
        else:
            print("{}/{}".format(retry_count,missing_total), "开始重下失败链接:")

        #记录当前文件数
        file_origin_counts = len(os.listdir(download_path))
        download_gmv(missing_page[-1][1])
        #记录文件下载后的文件数
        file_now_counts = len(os.listdir(download_path))

        #判断文件是否下载成功
        if (file_now_counts - file_origin_counts) == 1:
            print("成功!!")
            print(missing_page[-1][0])
            print("*"*50)
            missing_page.pop()
            retry_num = 1
        else:
            print("重新下载失败, 需要再次下载.")
            print(missing_page[-1][0])
            print("*"*50)
            retry_count -= 1
            retry_num += 1

    end = time.time()
    duration_s = round(end-start,1)
    duration_min = round(duration_s/60,2)
    print("行业大盘数据全部爬取完成, 共{}页".format(str(total)))
    print("总耗时: {}s,".format(duration_s), "{}min".format(duration_min))
    
