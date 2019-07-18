import os
import time
# from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from lxml import etree


# date = datetime.now().strftime('%Y%m%d')
# aws_price_url = 'https://www.amazonaws.cn/en/ec2/pricing/'


class GetEC2Price(object):
    def __init__(self):
        self.aws_ec2_price_url = 'https://www.amazonaws.cn/en/ec2/pricing/'

    @staticmethod
    def soup(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def soup_request(url, headers=None, cookies=None):
        soup = ''
        cookies_dict = dict()
        if cookies is not None:
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
        while True:
            try:
                response = requests.get(url, headers=headers, cookies=cookies_dict)
                soup = BeautifulSoup(response.text, 'html.parser')
                break
            except Exception as e:
                print(e.__str__())
                time.sleep(2)
                continue
        return soup

    def lxml_html(self, html):
        html = etree.HTML(str(html))
        result = etree.tostring(html)
        soup = self.soup(result)
        return soup

    def get_price_urls(self, url):
        price_urls = []
        html = self.soup_request(url)
        html = html.find('div', class_='lb-rtxt')
        html = self.lxml_html(html)
        html_hrefs = html.find_all('a')
        for html_href in html_hrefs:
            postfix_url = (html_href['href'])
            price_urls.append(urljoin(url, postfix_url))
        return price_urls

    @staticmethod
    def combine_data(od_list, ri_list):
        ri_instance_types = []
        for ri_type in ri_list:
            ri_instance_types.append(ri_type[0])
        od_count = len(od_list)
        lines = []
        for i in range(od_count):
            od_instance_type = od_list[i][0]
            cpu = od_list[i][1]
            memory = od_list[i][3]
            storage = od_list[i][4]
            price = od_list[i][-1].replace('/', '')
            if price != 'NA':
                month_price = float(price) * 24 * 30
                month_price = str(month_price)
            else:
                month_price = 'N/A'
            while True:
                if od_instance_type not in ri_instance_types:
                    line = '"%s","N/A","N/A","N/A","N/A","N/A","N/A","N/A","%s","%s","%s","%s","%s"' % (od_instance_type, price, month_price, cpu, memory, storage)
                    lines.append(line)
                    break
                else:
                    ri_data = ri_list[0]
                    ri_instance_type = ri_data[0]
                    line = ''
                    if od_instance_type == ri_instance_type:
                        ri_data.append(month_price)
                        ri_data.append(cpu)
                        ri_data.append(memory)
                        ri_data.append(storage)
                        length = len(ri_data)
                        for j in range(length):
                            if j == length - 1:
                                line = line + '"' + ri_data[j] + '"'
                            else:
                                line = line + '"' + ri_data[j] + '"' + ','
                        lines.append(line)
                        ri_list.remove(ri_data)
                        if len(ri_list) == 0:
                            break
                    else:
                        next_ri_instance_type = ri_list[1][0]
                        next_od_instance_type = od_list[i + 1][0]
                        if next_od_instance_type == next_ri_instance_type:
                            break
                        else:
                            if next_od_instance_type not in ri_instance_types:
                                break
                            else:
                                length = len(ri_data)
                                if ri_instance_type == next_ri_instance_type:
                                    for j in range(length):
                                        if j == length - 1:
                                            line = line + '"' + ri_data[j] + '"'
                                        else:
                                            line = line + '"' + ri_data[j] + '"' + ','
                                    lines.append(line)
                                    ri_list.remove(ri_data)
                                else:
                                    if next_od_instance_type != next_ri_instance_type:
                                        for j in range(length):
                                            if j == length - 1:
                                                line = line + '"' + ri_data[j] + '"'
                                            else:
                                                line = line + '"' + ri_data[j] + '"' + ','
                                        lines.append(line)
                                        ri_list.remove(ri_data)
                                    else:
                                        break
        return lines

    def get_price_type_info(self, html):
        new_html_lis = []
        html = self.lxml_html(html)
        html_lis = html.find_all('li', 'lb-accordion-group')
        new_html_lis.append(html_lis[0])
        new_html_lis.append(html_lis[2])
        od_list = []
        ri_list = []
        for html_li in new_html_lis:
            instance_type = html_li.a.div.string
            instance_type = str(instance_type).strip()
            html_instance_type = self.lxml_html(html_li)
            trs = html_instance_type.find_all('tr')
            for tr in trs:
                html_tr = self.lxml_html(tr)
                tds = html_tr.find_all('td')
                line = []
                if str(tds[0].string).strip() != '':
                    for i in range(len(tds)):
                        td_string = str(tds[i].string).strip()
                        if i == len(tds) - 1:
                            line.append(td_string)
                        else:
                            line.append(td_string)
                    if '' not in line:
                        if 'Instance Type' not in line:
                            if instance_type == 'On-Demand Instances':
                                od_list.append(line)
                            else:
                                ri_list.append(line)
        lines = self.combine_data(od_list, ri_list)
        return lines

    def store_price_info(self, url):
        html = self.soup_request(url)
        title = html.find('h1').string
        regions = html.find_all('h3')
        regions_uls = html.find_all('ul', 'lb-accordion lb-accordion-sketch')
        for i in range(len(regions)):
            region = regions[i].string
            # file = '%s_%s_%s.csv' % (title, region, date)
            file = '%s_%s.csv' % (title, region)
            if os.path.exists(file):
                os.remove(file)
            f = open(file, 'a+', encoding='utf8')
            f.write(region + ',' + '\n')
            region_uls = regions_uls[i]
            lines = self.get_price_type_info(region_uls)
            f.write(
                'Instance Type,Term,Offering Type,Upfront Price,Usage Price,Monthly Cost,Effective RI Rate,Savings Compared to OD,OD Price,OD Monthly Cost,CPU,Memory,Storage' + '\n')
            for line in lines:
                f.write(line + '\n')
            f.close()

    def main(self):
        for price_url in self.get_price_urls(self.aws_ec2_price_url):
            self.store_price_info(price_url)


if __name__ == '__main__':
    app = GetEC2Price()
    app.main()
