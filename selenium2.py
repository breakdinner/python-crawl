# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from prettyprinter import pprint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException as ne
import time
import platform

# 浏览器初始化准备
def _init(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    if platform.system() == 'Linux':
        chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    return driver


# 获取赛事
def _get_games():
    return [
        '英超', '西甲', '德甲', '法甲', '意甲', '苏超', '中超', '瑞典超', '瑞典甲',
        '瑞士超', '挪超', '挪甲', '丹麦超', '葡超', '荷甲', '比超', '希腊超',
        '俄超', '奥甲', '罗甲', '乌克超', '捷甲', '斯伐超', '土超', '以超',
        '克亚甲', '保超', '巴甲', '阿甲', '乌拉甲', '委内超', '玻利甲', '厄瓜甲',
        '美职业', '波兰超', '塞浦甲', '爱超', '爱甲'
    ]


def _filter_game(driver):
    # 等待页面加载完成, 以找到id为odds的元素为准
    element = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.ID, "odds"))
    )
    # 设置简体
    language0 = driver.find_element_by_css_selector('#Language0 > span')
    ActionChains(driver).click(language0)
    # 显示初盘
    firstodds = driver.find_element_by_id('firstodds')
    ActionChains(driver).click(firstodds)
    # time.sleep(5)
    # 赛事选择-开启界面
    league_div = driver.find_element_by_xpath("//a[contains(@onclick, 'LeagueDiv')]")
    ActionChains(driver).click(league_div)
    # 赛事选择-未开始
    select_league_2 = driver.find_element_by_id('selectLeague2')
    ActionChains(driver).click(select_league_2)
    # TODO 这里根据game来点击需要的赛事, 减少后面的查找
    # 赛事选择-一级
    yiji = driver.find_element_by_id('yiji')

    ActionChains(driver).click(yiji)
    # 赛事选择-ok
    select_ok = driver.find_element_by_xpath("//input[starts-with(@onclick, 'SelectOK')]")
    ActionChains(driver).click(select_ok)

    return element


# 根据赛事获取
def get_by_game():
    data = []
    games = _get_games()
    driver = _init('http://score.nowscore.com/odds/')
    try:
        element = _filter_game(driver)
        # 查找所有的赛事table
        elements = element.find_elements_by_class_name('b_tab')
        # exit(0)
        for i in elements:
            # 对一级进行赛事过滤
            try:
                i_a = i.find_element_by_xpath(
                    ".//a[starts-with(@href, 'http://info.nowscore.com/cn')]"
                )
            except ne:
                continue
            if i_a.text not in games:
                continue
            # pprint(i)
            # continue
            i_names = i.find_elements_by_tag_name('b')
            # 注意最前面有个. , 如果不带.的话是全元素匹配, 带上.是基于当前元素下匹配
            i_bankers = i.find_elements_by_xpath(".//tr[starts-with(@id, 'odds_')]")

            single_first_odds = {}
            single_win = {}
            single_tie = {}
            single_fail = {}
            for banker in i_bankers:
                name = banker.find_element_by_xpath(".//td[@height='20']")
                try:
                    all_contents = banker.find_elements_by_tag_name('td')
                    if len(all_contents) < 1:
                        continue
                except IndexError:
                    pprint(IndexError)
                    continue
                single_first_odds[name.text] = all_contents[2].text
                single_win[name.text] = all_contents[4].text
                single_tie[name.text] = all_contents[5].text
                single_fail[name.text] = all_contents[6].text
            data.append({
                'host': i_names[0].text,
                'guest': i_names[1].text,
                'first_odds': single_first_odds,
                'win': single_win,
                'tie': single_tie,
                'fail': single_fail,
                'game': i_a.text
            })
    except ec as e:
        pprint(e)
    finally:
        driver.quit()

    return data


# 获取指定赛事指定队伍的近期状况
def get_by_game_of_team():
    driver = _init('http://score.nowscore.com/odds/')
    element = _filter_game(driver)
    games = _get_games()
    # 查找所有的赛事table
    elements = element.find_elements_by_class_name('b_tab')
    # url
    url: str = 'http://score.nowscore.com/panlu/{0}.html'
    # 详细信息
    all = []
    for e in elements:
        # i_a = e.find_element_by_xpath(
        #     ".//a[starts-with(@href, 'http://info.nowscore.com/cn')]"
        # )
        # 获取主客队名称
        host_name = e.find_element_by_xpath(".//div[starts-with(@id, 'home_')]")
        guest_name = e.find_element_by_xpath(".//div[starts-with(@id, 'guest_')]")
        pprint(host_name.text)
        pprint(guest_name.text)
        continue
        try:
            i_a = e.find_element_by_xpath(
                ".//a[starts-with(@href, 'http://info.nowscore.com/cn')]"
            )
        except ne:
            continue
        if i_a.text not in games:
            id: str = e.get_attribute('id')
            special: int = id.split('_').pop()
            url = url.format(special)

            # req = request.Request(url)
            # rlb = request.urlopen(req, timeout=3).read()
            # bs = BeautifulSoup(rlb, 'lxml')
            # print(bs.prettify())
            # exit(0)

            driver_child = _init(url)
            # 近15场 todo 延时加载的问题
            # last15 = driver_child.find_element_by_id('td15')
            # ActionChains(driver_child).move_to_element(last15).click()

            # 等待页面加载完成, 以找到id为odds的元素为准
            element_child = WebDriverWait(driver_child, 5).until(
                ec.presence_of_element_located((By.XPATH, "//tr[@align='center']"))
            )
            result = element_child.find_elements_by_xpath("//tr[@align='center']")
            for r in result:
                if r.get_attribute('bgcolor') == '#4F608C':
                    continue
                td = r.find_elements_by_tag_name('td')
                single = {
                    'name': td[0].text,
                    'time': td[1].text,
                    'host': td[2].text.split(' ').pop(),
                    'guest': td[4].text.split(' ').pop(),
                    'score': td[3].text,
                    'half-score': td[5].text,
                    'result': td[6].text,
                    'pan': td[7].text,
                }
                all.append(single)

            pprint(all)
            exit(0)
            # req = request.Request(url.format(special))
            # rlb = request.urlopen(req, timeout=3).read()
            # bs = BeautifulSoup(rlb, 'lxml')
            # print(bs.prettify())


get_by_game_of_team()


# sleep(3)
# res = driver.find_element_by_xpath('//*[@id="bottom"]')
# actions = ActionChains(driver).move_to_element(res)
#

