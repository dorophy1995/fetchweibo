# coding:UTF-8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 键盘
from selenium.common.exceptions import *


# come to the bottom of ther page
def to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# find the next page button or return None
def find_next_page_or_none(driver):
    try:
        next_page = driver.find_element_by_link_text('下一页')
        return next_page
    except:
        return None


# login with your own account
def login(driver, account, password):
    try:
        label = driver.find_element_by_link_text('登录')
        label.click()
    except:
        pass
    try:
        label = driver.find_element_by_link_text('帐号登录')
        label.click()
    except:
        try:
            label = driver.find_element_by_link_text('账号登录')
            label.click()
        except:
            return
    try:
        login_name = driver.find_element_by_id('loginname')
        login_name.send_keys(account)
    except:
        pass
    try:
        login_pw = driver.find_element_by_name('password')
        login_pw.send_keys(password)
        login_pw.send_keys(Keys.RETURN)
    except NoSuchElementException:
        print 'NoSuchElementException'
    try:
        login_name = driver.find_element_by_id('loginname')
        login_name.send_keys(account)
    except:
        pass


def main(account, password, topic, pages=10, one_page_try=6):
    """
    :param account: your account name
    :param password:  your password
    :param topic: the topic you want to fetch
    :return: a txt file named weibo+datetime storing all weibo content in specified topic
    """
    driver = webdriver.Chrome()
    driver.get('http://weibo.com')
    # login
    time.sleep(3)
    login(driver, account, password)
    # 到话题页
    driver.get('http://huati.weibo.com/k/{}'.format(topic))

    output = open('weibo-%s.txt' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), 'w')

    for i in range(pages):
        for j in range(one_page_try):
            if find_next_page_or_none(driver) is None:
                # 拽到页面最下方
                time.sleep(1)
                to_bottom(driver)
            else:
                break
        # 抓到所有微博
        e = driver.find_elements_by_xpath('//div[@class="WB_text W_f14"]')
        for x in e:
            try:
                output.write(x.text.encode('utf8'))
            except:
                print x.text
            output.write('\n')
        output.flush()
        # 翻页
        try:
            find_next_page_or_none(driver).click()
            login(driver, account, password)
            # 重新login
        except:
            break

    output.close()
    driver.close()

