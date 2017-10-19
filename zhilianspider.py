# _*_ coding:utf-8 _*_ 
_author_ = 'mlj'
_date_ = '2017/10/19 16:53'

from selenium import webdriver
import json, time, xlwt


class Zhilian(object):
    def __init__(self):
        # 第一页url 智联 北京 python
        self.url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python&p=1&isadv=0'
        # 构建请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
        self.driver = webdriver.Chrome()
        # self.page = 1

    def parser_data(self):
        node_list = self.driver.find_elements_by_xpath('//*[@class="newlist"]')
        print(len(node_list))
        data_list = []
        i = 1
        for node in node_list:
            if i == 1:
                # 第一个是title 略过
                pass
            else:
                # print(node)
                temp = {}
                temp['职位名称'] = node.find_element_by_xpath('./tbody/tr/td/div/a').text
                temp['公司名称'] = node.find_element_by_xpath('./tbody/tr[1]/td[3]/a[1]').text
                temp['职位月薪'] = node.find_element_by_xpath('./tbody/tr[1]/td[4]').text
                temp['工作地点'] = node.find_element_by_xpath('./tbody/tr[1]/td[5]').text
                temp['学历'] = node.find_element_by_xpath('./tbody/tr[2]/td/div/div/ul/li[1]/span[4]').text
                temp['发布日期'] = node.find_element_by_xpath('./tbody/tr[1]/td[6]/span').text
                temp['url'] = node.find_element_by_xpath('./tbody/tr[1]/td[1]/div/a').get_attribute('href')
                data_list.append(temp)
            i = i + 1
            print(i)
        # print(data_list)
        return data_list

    def save_data_json(self, data_list):
        with open('智联mlj.json', 'ab+')as f:
            for data in data_list:
                str_data = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(str_data.encode())

    def __del__(self):
        self.driver.close()

    def run(self):
        # 第一页
        self.driver.get(self.url)

        while True:
            # 打开网页发送请求　　　
            print('当前要请求的网页：', self.driver.current_url)
            # 解析数据
            data_list = self.parser_data()
            # 保存数据
            self.save_data_json(data_list)

            # 翻页
            try:
                el_next = self.driver.find_element_by_xpath('//ul/li/a[@class="next-page"]')
                el_next.click()
                self.driver.implicitly_wait(2)
                # time.sleep(2)
                next_url = self.driver.current_url
                self.driver.get(next_url)

            except Exception as e:
                print(e)
                break


if __name__ == '__main__':
    zhilian = Zhilian()
    zhilian.run()
