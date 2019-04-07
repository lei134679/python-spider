from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, random, pymysql


class Tmall():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        # self.options.set_headless()  # 把 chrome 设置成无头模式，不论 windows 还是 linux 都可以，自动适配对 应参数
        self.options.add_experimental_option('excludeSwitches',
                                             ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        # mysql对象
        self.con = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="sql-file")
        self.cur = self.con.cursor()
        # 待爬取数据dict
        self.no_spider = []

    def cookie(self):
        """
        获取登陆后的cookie，模拟登陆
        :return:
        """
        self.driver.get('https://www.tmall.com/')
        cookies = [
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "_l_g_",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "Ug%3D%3D",
                "id": 1
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1555205818.129384,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_m_h5_tk",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "a95b4b1eceb0613ab0111a6972404a4b_1554610381596",
                "id": 2
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1555205818.129509,
                "hostOnly": False,
                "httpOnly": False,
                "name": "_m_h5_tk_enc",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "0c14aa982e31cdf832849f2d4da744cf",
                "id": 3
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "_nk_",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "l15038604055",
                "id": 4
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "_tb_token_",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "757e1b5b77397",
                "id": 5
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "ck1",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "\"\"",
                "id": 6
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 2185110629,
                "hostOnly": False,
                "httpOnly": False,
                "name": "cna",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "wi8nFV+O238CAT2jiWbIATre",
                "id": 7
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": True,
                "name": "cookie1",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "B0b%2FGMLxPOMYvBGIWiUhxFEOQjY9G5nkxS2wttANTVw%3D",
                "id": 8
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": True,
                "name": "cookie17",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "UU6oK4uF6LhStQ%3D%3D",
                "id": 9
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": True,
                "name": "cookie2",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "11d17c3330cc8bd5f8b527217ca197c9",
                "id": 10
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "csg",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "c216495f",
                "id": 11
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1869750828.264008,
                "hostOnly": False,
                "httpOnly": True,
                "name": "enc",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "R3hGuxKTeLsvOiHnkR9%2FLmvJsUgJg%2FOa3Q%2B6OvBmp1YyWKYYszE1nUIIoyU7havvVOBIRLGc6gBAbO65qkNTkg%3D%3D",
                "id": 12
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1557199193.778426,
                "hostOnly": False,
                "httpOnly": False,
                "name": "hng",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "\"\"",
                "id": 13
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1570159195,
                "hostOnly": False,
                "httpOnly": False,
                "name": "isg",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "BPT0KJKUFI5mhIDNICOhuwyvxbKmZTPjAIE2Ro5Vw38C-ZRDttklR7y7eXGEAVAP",
                "id": 14
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1570159195,
                "hostOnly": False,
                "httpOnly": False,
                "name": "l",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "bB_bD4Nuv66mE2JoBOCwquIRXnbO-IRAguPRwkTei_5Zy_T6yhWOlGOWXE96Vj5R_gLB402lRpy9-etki",
                "id": 15
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "lgc",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "l15038604055",
                "id": 16
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1586137024.221412,
                "hostOnly": False,
                "httpOnly": False,
                "name": "lid",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "l15038604055",
                "id": 17
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "login",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "true",
                "id": 18
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1586141401,
                "hostOnly": False,
                "httpOnly": False,
                "name": "otherx",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0",
                "id": 19
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "skt",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "61710a80e4a7d11c",
                "id": 20
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "t",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "986a19d3a3733d685c299e38bde662cb",
                "id": 21
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "tk_trace",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "1",
                "id": 22
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "tracknick",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "l15038604055",
                "id": 23
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "uc1",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTZ4Mn7etUs6g%3D%3D&tag=8&lng=zh_CN",
                "id": 24
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": True,
                "name": "uc3",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "vt3=F8dByEiR0g8MTZXN7mc%3D&id2=UU6oK4uF6LhStQ%3D%3D&nk2=D5LcBxsybxnUdzpx&lg2=Vq8l%2BKCLz3%2F65A%3D%3D",
                "id": 25
            },
            {
                "domain": ".tmall.com",
                "hostOnly": False,
                "httpOnly": False,
                "name": "unb",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "2692604818",
                "id": 26
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1557199193.779407,
                "hostOnly": False,
                "httpOnly": False,
                "name": "uss",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "\"\"",
                "id": 27
            },
            {
                "domain": ".tmall.com",
                "expirationDate": 1585926886,
                "hostOnly": False,
                "httpOnly": False,
                "name": "x",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "__ll%3D-1%26_ato%3D0",
                "id": 28
            },
            {
                "domain": "www.tmall.com",
                "expirationDate": 1586143196,
                "hostOnly": True,
                "httpOnly": False,
                "name": "cq",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "ccp%3D0",
                "id": 29
            }
        ]
        print('删除所有cookie')
        self.driver.delete_all_cookies()
        print('添加cookie')
        for item in cookies:
            self.driver.add_cookie(item)
        print('cookie添加完成')
        self.driver.get('https://www.tmall.com/')

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 0.7
        # 计算间隔
        t = 0.05
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 18
            else:
                # 加速度为负3
                a = -6
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
            # print('forword', current, distance)

        v = 0

        move = current - distance
        # 加入轨迹
        track.append(round(move))

        return track

    def yzm(self):
        """
        滑动验证码
        :return:
        """
        element = self.wait.until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))
        # action.click_and_hold(element)
        span = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nc_1__scale_text > span')))
        x1 = span.size
        x2 = element.size
        ActionChains(self.driver).click_and_hold(element).perform()
        track = self.get_track(x1['width'] - x2['width']+10)
        while track:
            x = random.choice(track)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            track.remove(x)
            time.sleep(0.01)
        ActionChains(self.driver).release(element).perform()
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nc-lang-cnt')))
            print('验证码未通过，继续滑动')
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, '刷新'))).click()
            self.yzm()
        except:
            print('验证码通过')

    def get_data(self):
        """
        从数据库中获取数据
        :return: 返回关键字，品牌名
        """
        self.cur.execute("select title from fcms_product")
        result = self.cur.fetchall()
        for item in result[:1000]:
            if item[0]:
                keyword = item[0].split('-')[1]
                brand_name = item[0].split('-')[0]
                brand_name = brand_name.split('/')[0]
                self.no_spider.append([keyword, brand_name])

    def search(self):
        """
        爬去信息
        :return:
        """
        while self.no_spider:
            item = self.no_spider[0]
            print('搜索商品：', item[0], item[1])
            self.wait.until(EC.presence_of_element_located((By.ID, 'mq'))).clear()
            self.wait.until(EC.presence_of_element_located((By.ID, 'mq'))).send_keys(item[0])
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.mallSearch-input.clearfix > button'))).click()
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, '更多'))).click()
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.j_BrandSearch.av-search.clearfix > input'))).send_keys(item[1])
            time.sleep(2)
            li = self.driver.find_elements_by_css_selector('.row-1.av-expand > li')
            if li:
                if li[0].text.find(item[1]):
                    li[0].click()
                    # 中途验证码重新请求
                    if self.driver.title == 'security-X5':
                        # 模拟滑动
                        self.yzm()

                        # 重新请求
                        # tmall.cookie()
                        # tmall.search()
                    else:
                        self.spider()
            else:
                print('此品牌不存在', item[0], item[1])
        else:
            print('null, 请添加商品，继续爬取')

    def spider(self):
        """
        爬去所需信息
        :return:
        """
        div = self.driver.find_elements_by_css_selector('div[class="product  "]')
        print(len(div))
        for d in div:
            print('=' * 100)
            id = d.get_attribute('data-id')
            print('商品id', id)
            store_name = d.find_element_by_css_selector('.product-iWrap > .productShop > a').text
            print('店铺名称', store_name)
            # 存储数据库
            sql = 'insert into tmall_spider values(%s,%s,%s)'
            self.cur.execute(sql, (0, id, store_name))
            self.con.commit()
        # 翻页处理
        try:
            next_page = self.driver.find_element_by_link_text('下一页>>').get_attribute('href')
            next_page = self.driver.current_url.split()[0] + next_page
            print('下一页', next_page)
            self.driver.get(next_page)
            self.spider()
        except:
            print('已到最后一页，请更换商品')
            self.no_spider.pop(0)

    def close(self):
        """
        关闭数据库， 关闭浏览器
        :return:
        """
        self.cur.close()
        self.con.close()
        self.driver.quit()


if __name__ == '__main__':
    tmall = Tmall()
    tmall.cookie()
    tmall.get_data()
    tmall.search()
    tmall.close()
