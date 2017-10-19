# _*_ coding:utf-8 _*_ 
_author_ = 'mlj'
_date_ = '2017/10/19 21:38'

from selenium import webdriver
import json, time, xlwt


class Zhilian(object):
    def __init__(self):
        # 第一页url 智联 北京 python
        self.url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python&sm=0&sg=c0f7c83d2cc64ac280b4008b7d8e6281&p={}'

        # 构建请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36',
        }
        self.driver = webdriver.Chrome()
        self.page = 88

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
        with open('智联2.json', 'ab+')as f:
            for data in data_list:
                str_data = json.dumps(data, ensure_ascii=False) + ',\n'
                f.write(str_data.encode())

    def __del__(self):
        self.driver.close()

    def run(self):
        # 第一页
        while True:
            # 打开网页发送请求

            print('正在获取第{}页内容'.format(self.page))
            try:
                self.driver.get(self.url.format(self.page))
                # 解析数据
                data_list = self.parser_data()
                self.save_data_json(data_list)
                # 下一页
                self.page = self.page + 1
                time.sleep(2)
                # 获取下一页前面一个li内容
                pre_node = self.driver.find_element_by_xpath('//div[@class="pagesDown"]/ul/li[11]/a').text
                bl = str.isdigit(pre_node)
                print('倒数第一个页面为:%s, 是否为数字：%s, 即将爬取的页面为：%s ' % (pre_node, bl, self.page))
                # 判断是否为数字字符串
                if str.isdigit(pre_node):
                    # 判断是否小于 self.page
                    if int(pre_node) < self.page:
                        # 遍历完毕，程序结束
                        print('已经下载完成%d页，爬取结束！' % pre_node)
                        break
                pass
            except Exception as e:
                print(e)
                break


if __name__ == '__main__':
    zhilian = Zhilian()
    zhilian.run()