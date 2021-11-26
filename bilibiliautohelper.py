import base64
import linecache
import requests
from PIL import Image
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random


def getElement(way, element):
    time.sleep(1)
    if way == 'CSS_SELECTOR':
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
    elif way == 'ID':
        return wait.until(EC.presence_of_element_located((By.ID, element)))
    elif way == 'XPATH':
        return wait.until(EC.presence_of_element_located((By.XPATH, element)))

# 登陆完整操作
# 初始化
def init():
    global browser, wait
    options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=http://222.95.240.86:3000')
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # 实例化chrome浏览器
    browser = webdriver.Chrome(
        r"D:\chromedriver_win32\chromedriver.exe", options=options)
    # browser.get("http://ip138.com/")
    browser.maximize_window()
    time.sleep(2)
    # 设置等待超时
    wait = WebDriverWait(browser, 20)

# 登录
def login(name1, pw1, type, url):
    if type == "1":
        # 打开登录页面
        browser.get(url)
        time.sleep(6)
        quick_login = getElement('CSS_SELECTOR', 'a.bilibili-player-quick-login')
        quick_login.click()
        time.sleep(2)
    elif type == "2":
        # 打开直播页面
        browser.get(url)
        time.sleep(13)
        js = "window.scrollTo(0,0);"
        browser.execute_script(js)
        quick_login = getElement('CSS_SELECTOR', 'a.top-nav-btn.dp-i-block.v-top.pointer.border-box')
        quick_login.click()
        time.sleep(2)
    # 转到iframe
    iframe = getElement('XPATH', '/html/body/div[5]/div')
    browser.switch_to.frame(iframe)
    # 获取用户名输入框
    user = getElement('XPATH', '/html/body/div[5]/div/div[3]/div/div[2]/div[1]/div/input')
    # 获取密码输入框
    passwd = getElement('XPATH', '/html/body/div[5]/div/div[3]/div/div[2]/div[2]/div/input')
    # 输入用户名
    user.send_keys(name1)
    # 输入密码
    passwd.send_keys(pw1)
    # 获取登录按钮
    login_btn = getElement('ID', 'login-submit')
    # 随机延时点击
    login_btn.click()
    time.sleep(1.5)

# 下载
def downfile():
    # js代码根据canvas文档说明
    js = 'return document.getElementsByClassName("' \
         'geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png")'
    js1 = 'return document.getElementsByClassName("' \
          'geetest_canvas_fullbg geetest_fade geetest_absolute")[0].toDataURL("image/png")'
    # 执行 JS 代码并拿到图片 base64 数据
    im_info = browser.execute_script(js)  # 执行js文件得到带图片信息的图片数据
    im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    im_info1 = browser.execute_script(js1)
    im_base641 = im_info1.split(',')[1]
    im_bytes1 = base64.b64decode(im_base641)
    with open(r'C:\Users\jiang\Desktop\autologin\bg1.png', 'wb') as f:  # 保存图片到本地
        f.write(im_bytes)
    with open(r'C:\Users\jiang\Desktop\autologin\bg.png', 'wb') as f:
        f.write(im_bytes1)

# 获取 缺口图片位置坐标
def get_geetest_position(image1, image2):
    left = 0
    for i in range(left, image1.size[0]):
        for j in range(image1.size[1]):
            if not is_pixel_equal(image1, image2, i, j):
                left = i
                return left
    return left

def is_pixel_equal(image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    threshold = 60
    if abs(pixel1[0] - pixel2[0]) < threshold and \
            abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        print(pixel1, pixel2)
        return False

def move_to_gap(source, targetOffsetX):
    # B站根据是否有暂停时间来分辨人机。
    action_chains = webdriver.ActionChains(browser)
    # 拖拽
    action_chains.click_and_hold(source)
    action_chains.pause(0.2)
    action_chains.move_by_offset(targetOffsetX-20, 0)
    for i in range(5):
        action_chains.move_by_offset(2, 0)
    action_chains.move_by_offset(1, 0)
    action_chains.move_by_offset(-1, 0)
    action_chains.release()
    action_chains.perform()

def slide():
    image1=Image.open(r'C:\Users\jiang\Desktop\autologin\bg.png')
    image2=Image.open(r'C:\Users\jiang\Desktop\autologin\bg1.png')
    distance = get_geetest_position(image1, image2)
    print('偏移量为：%s pixel' % distance)
    slider = getElement('CSS_SELECTOR', 'div.geetest_slider_button')
    # 移动滑块
    move_to_gap(slider, distance)

def getline(file_path, linenum):
    return linecache.getline(file_path, linenum).strip()


# 各种功能
class PraiseBrush:
    def logout(self):
        hover_ele = getElement('CSS_SELECTOR', 'div.mini-avatar.van-popover__reference')
        ActionChains(browser).move_to_element(hover_ele).perform()
        quit_btn=browser.find_element_by_class_name('logout')
        quit_btn.click()
        time.sleep(2.5)

    def dzan(self):
        time.sleep(2.5)
        # 获取点赞标签以判断属性是否点过赞
        data = getElement('CSS_SELECTOR', 'span.like')
        time.sleep(0.5)
        # 获取点赞按钮
        gz_btn = getElement('CSS_SELECTOR', 'i.van-icon-videodetails_like')
        if data.get_attribute('class')!='like on':
            gz_btn.click()
            print("点赞成功")
            time.sleep(1)
            # gz_btn.click()
            # print("取消点赞成功")

        else:

            print("不操作")
        time.sleep(2.5)

    def clt(self):
        time.sleep(2.5)
        # 获取收藏标签以判断属性是否点过赞
        data = getElement('CSS_SELECTOR', 'span.collect')
        # 获取收藏按钮
        clt_btn = getElement('XPATH', '/html/body/div[3]/div/div[1]/div[3]/div[1]/span[3]/canvas')
        if data.get_attribute('class') == 'collect on':
            print("上次收藏过了")
        else:
            clt_btn.click()
            time.sleep(1)
            close = getElement('XPATH', '/html/body/div[3]/div/div[3]/div/div/div[1]/i')
            close.click()
            time.sleep(1)
            clt_btn.click()
            time.sleep(1)
            clt_btn1 = getElement('CSS_SELECTOR', 'span.fav-title')
            conf_btn = getElement('CSS_SELECTOR', 'button.btn.submit-move')
            clt_btn1.click()
            time.sleep(0.5)
            conf_btn.click()
            print("收藏成功")
        time.sleep(2.5)

    def vdodisplay(self):
        play_btn = getElement('CSS_SELECTOR', 'div.bilibili-player-video-btn')
        play_btn.click()
        time.sleep(5)
        play_btn.click()
        time.sleep(2.5)




class live_operation:
    def isElementExist(self, element):
        flag = True
        try:
            browser.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

    def rob(self):
        element = '/html/body/div[1]/main/div[1]/section[1]/div[3]/div[6]/div/div[1]/div[4]'
        i = 0
        while i < 60:
            while self.isElementExist(element):
                rob_btn = browser.find_element_by_xpath(element)
                print("存在")
                rob_btn.click()
                time.sleep(5)
            print("不存在")
            time.sleep(1)
            i = i+1
        time.sleep(2)

    def logout(self):
        time.sleep(3)


class Report:
    def repo(self, choice, reason, org):
        # 获取稿件投诉按钮
        elm1 = getElement('CSS_SELECTOR', 'div.appeal-text')
        elm1.click()
        time.sleep(1.5)
        # 转到iframe
        iframe = getElement('XPATH', '/html/body/div[3]/div/div[3]/div/div/iframe')
        browser.switch_to.frame(iframe)
        time.sleep(1)
        altern = getElement('XPATH', '/html/body/div/div[3]/div[1]/div[2]/div[' + choice + ']')
        text = getElement('XPATH', '/html/body/div/div[3]/div[1]/div[3]/div[2]/textarea')
        conf = getElement('CSS_SELECTOR', 'div.confirm')
        altern.click()
        time.sleep(0.5)
        text.send_keys(reason)
        time.sleep(0.5)
        if choice =="7":
            text1 = getElement('XPATH', '/html/body/div/div[3]/div[1]/div[4]/div/div[2]/textarea')
            text1.send_keys(org)
        elif choice == "9":
            text1 = getElement('XPATH', '/html/body/div/div[3]/div[1]/div[4]/div/input')
            text1.send_keys(org)
        conf.click()
        time.sleep(1.5)

# 97887962
# 未经作者同意擅自转载，还投了自制，侵权必究
    def logout(self):
        hover_ele = getElement('CSS_SELECTOR', 'div.mini-avatar.van-popover__reference')
        ActionChains(browser).move_to_element(hover_ele).perform()
        quit_btn = browser.find_element_by_class_name('logout')
        quit_btn.click()
        time.sleep(2.5)


# 执行操作    
def praise_collect(param, num, collect, st):
    dz = PraiseBrush()
    init()
    if num == "-1" and collect == "-1":
        for i in range(eval(st), eval(st) + 100):
            file_path = r'D:\chromedriver_win32\account.txt'
            string = getline(file_path, i)
            name = string[:8]
            pw = string[12:]
            print(name, pw)
            url = 'https://www.bilibili.com/video/' + param
            login(name, pw, "1", url)
            downfile()
            time.sleep(0.5)
            slide()
            dz.vdodisplay()
            print("播放了")
            dz.logout()
    else:
        sig = 0
        jnum = min(eval(num), eval(collect))
        diff = abs(eval(num) - eval(collect))
        if eval(num) > eval(collect):
            sig = 1
        for i in range(eval(st), eval(st)+jnum):
            file_path = r'C:\Users\jiang\Desktop\autologin\account.txt'
            string = getline(file_path, i)
            name = string[:8]
            pw = string[12:]
            print(name, pw)
            url = 'https://www.bilibili.com/video/' + param
            login(name, pw, "1", url)
            downfile()
            time.sleep(0.5)
            slide()
            dz.dzan()
            dz.vdodisplay()
            dz.clt()
            print("当前刷完的编号是" + str(i))
            time.sleep(5)
            dz.logout()
        for i in range(eval(st)+ jnum, eval(st)+ jnum+ diff):
            file_path = r'C:\Users\jiang\Desktop\autologin\account.txt'
            string = getline(file_path, i)
            name = string[:8]
            pw = string[12:]
            print(name, pw)
            url = 'https://www.bilibili.com/video/' + param
            login(name, pw, "1", url)
            downfile()
            time.sleep(0.5)
            slide()
            if sig == 1:
                dz.dzan()
            else:
                dz.clt()
            dz.vdodisplay()
            print("当前刷完的编号是" + str(i))
            time.sleep(5)
            dz.logout()
        # print("最后一个刷完的编号：" + str(eval(st) + jnum + diff - 1))
    browser.quit()


def roblt(param):
    lt = live_operation()
    init()
    url = 'https://live.bilibili.com/'+param
    name = 'pkqh8216'
    pw = '883887FsR4'
    login(name, pw, "2", url)
    downfile()
    time.sleep(0.5)
    slide()
    lt.rob()
    lt.logout()
    time.sleep(5)
    # browser.quit()

def rpt(param, num, ch, re, org, sta):
    rp = Report()
    init()
    for i in range(eval(sta), eval(sta)+eval(num)):
        file_path = r'C:\Users\jiang\Desktop\autologin\account.txt'
        string = getline(file_path, i)
        name = string[:8]
        pw = string[12:]
        print(name, pw)
        url = 'https://www.bilibili.com/video/' + param
        login(name, pw, "1", url)
        downfile()
        time.sleep(0.5)
        slide()
        rp.repo(ch, re, org)
        time.sleep(5)
        rp.logout()
    browser.quit()
    print("最后一个举报完的编号："+str(eval(sta) + eval(num) - 1))



if __name__ == '__main__':
    print("功能："
          "1.视频刷赞和收藏\n"
          "2.直播间抢辣条\n"
          "3.批量举报视频\n")
    choice = input()
    if choice == '1':
        num = input("输入刷赞次数(根据你号的个数)")
        collect = input("输入收藏次数(根据你号的个数)")
        st = input("输入从哪个号开始")
        choice1 = input("1.输入新AV号"
                        "2.选择默认AV号")
        if choice1 == "1":
            avnum = input()
            praise_collect(avnum, num, collect, st)
        else:
            avnum = 'BV1ZK411L7Wg'
            praise_collect(avnum, num, collect, st)
    elif choice == "2":
        livenum = input("直播间号")
        roblt(livenum)
    elif choice == "3":
        vdo = input("输入AV号")
        nm = input("输入举报次数")
        sta = input("输入从哪个号开始")
        report = input("选择举报原因(单选)：\n"
                        "1.违法违禁"
                        "2.色情"
                        "3.低俗\n"
                        "4.赌博诈骗"
                        "5.血腥暴力"
                        "6.人身攻击\n"
                        "7.与站内其他视频撞车"
                        "8.不良封面/标题"
                        "9.转载/自制类型错误\n"
                        "10.引战"
                        "11.不能参加充电"
                        "12.青少年不良信息\n"
                        "13.有其他问题\n")
        if report == "7":
            org = input("输入撞车av号")
        elif report == "9":
            org = input("输入原创视频出处")
        else:
            org = ''
        reason = input("输入详细理由\n")
        rpt(vdo, nm, report, reason, org, sta)





