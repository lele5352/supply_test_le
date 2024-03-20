# -*- coding: utf8 -*-
import datetime
import time
import random
import requests
from bs4 import BeautifulSoup


class RobotMsg(object):

    def get_headers(self):
        ua_lsit = [
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
        ]
        ua = random.choice(ua_lsit)
        headers = {
            'user-agent': ua
        }

        return headers

    def greetings(self):
        """ 打招呼信息"""
        hour = int(time.strftime('%H', time.localtime(time.time())))
        if 5 <= hour <= 10:
            return "各位同学早上好！\n"
        elif hour == 12 or hour == 11:
            return "各位同学中午好！\n"
        elif 13 <= hour <= 18:
            return "各位同学下午好！\n"
        elif 19 <= hour <= 24:
            return "各位同学晚上好！\n"
        else:
            return "夜深了，早点睡觉咯~"

    def get_week_day(self, date):
        """日期信息"""
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        day = date.weekday()
        res = "今天日期为：" + str(datetime.date.today()) + ' ' + week_day_dict[day]
        return res

    def get_weather(self):
        """获取天气"""
        url = "http://www.nmc.cn/rest/weather?stationid=59287&_=1638428068253"
        r_url = requests.get(url, headers=self.get_headers())
        data = r_url.json()['data']
        air = data['air']
        real = data['real']
        station = data['predict']['station']
        city = station['city']
        aqi = air['aqi']
        humidity = str(data['real']['weather']['humidity'])
        wind_direct = real['wind']['direct']
        wind_power = real['wind']['power']
        temp = real['weather']['temperature']
        weather = real['weather']['info']
        airQuality = air['text']
        comfort_dict = {9999: ' ', 4: '很热，极不适应', 3: '热，很不舒适', 2: '暖，不舒适', 1: '温暖，较舒适', 0: '舒适，最可接受', -1: '凉爽，较舒适', \
                        -2: '凉，不舒适', -3: '冷，很不舒适', -4: '很冷，极不适应'}
        icomfort_no = real['weather']['icomfort']
        icomfort = comfort_dict[icomfort_no]

        return city + " " + '今日天气：' + weather + ' 当前温度：' + str(
            temp) + ' ℃ ' + '舒适度：' + icomfort + ' ' + wind_direct + ' ' + wind_power + \
               ' 当前相对湿度：' + humidity + "%" + ' 空气质量：' + str(aqi) + "（" + airQuality + "）"

    def get_top_list(self, use_flag=0):
        """
        百度前十热点
        use_flag:0-企业微信机器人、1-飞书机器人
        """

        requests_page = requests.get('http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b42_c513')
        soup = BeautifulSoup(requests_page.text, "html.parser")
        soup_text = soup.find_all(class_='content_1YWBm')
        i = 0
        top_list = []
        if use_flag:
            for text in soup_text:
                tag_a = {
                    "tag": "a",
                    "text": text.div.string + "\n",
                    "href": text.a["href"]
                }
                top_list.append(tag_a)
                i += 1
                if i == 10:
                    break
        else:
            for text in soup_text:
                i += 1
                top_list.append("[" + text.div.string + "](" + text.a['href'] + ")")
                if i == 10:
                    break
        return top_list

    def get_daily_sentence(self):
        """每日经典语录"""
        url = "http://open.iciba.com/dsapi/"
        r = requests.get(url, headers=self.get_headers())
        content = r.json()["content"]
        note = r.json()["note"]
        daily_sentence = "> " + content + "\n" + "> " + note
        return daily_sentence

    def get_random_sentence(self):
        """随机语录"""
        url = "https://api.xygeng.cn/one"
        r = requests.get(url, headers=self.get_headers())
        data = r.json().get("data")
        get_random_sentence = "> " + data.get("content") + "\n" + "> " + data.get("origin") + "\n" + "> " + data.get(
            "tag")
        return get_random_sentence


class QwRobot(RobotMsg):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def get_sendContent(self):
        qw_count = "# " + self.greetings() + "\n" + \
                   '<font color=\"warning\">' + self.get_week_day(datetime.date.today()) + '</font>' + "\n\n" + \
                   self.get_weather() + "\n\n" + \
                   str(self.get_top_list()).replace("', '", '\n').replace("['", "").replace("']", "") + "\n\n" + \
                   self.get_daily_sentence() + "\n\n"
        qw_count = {
            "msgtype": "markdown",
            "markdown": {
                "content": qw_count,
            }
        }
        return qw_count

    def send(self, webhook_url, content):
        headers = {"Content-Type": "text/plain"}
        requests_url = requests.post(webhook_url, headers=headers, json=content)
        if requests_url.text == '{"errcode":0,"errmsg":"ok"}':
            print("发送成功" + requests_url.text)
        else:
            print("发送失败" + requests_url.json())


class FsRobot(RobotMsg):

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def get_sendContent(self):
        title = self.greetings()
        tag_text = []
        get_week_day = self.get_week_day(datetime.date.today())
        tag_text.append(get_week_day)

        get_weather = self.get_weather()
        tag_text.append(get_weather)

        get_daily_sentence = self.get_daily_sentence()
        tag_text.append(get_daily_sentence)

        new_tag_test = [{"tag": "text", "text": x + "\n\n"} for x in tag_text]
        tag_a = self.get_top_list(1)

        fs_count = {
            "zh_cn": {
                "title": title,
                "content": [
                    new_tag_test, tag_a
                ]
            }
        }
        fs_count = {
            "msg_type": "post",
            "content": {
                "post": fs_count
            }
        }
        return fs_count

    def send(self, webhook_url, content):
        res = requests.post(webhook_url, headers=self.get_headers(), json=content)
        print(res.json())
        if res.json().get("msg") == "success":
            print("发送成功")
        else:
            print("发送失败" + res.text)

    # get_random_sentence()


if __name__ == '__main__':
    url_qw = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2c0ee031-c1a7-4217-a532-99ec013e436c"
    robot_qw = QwRobot(url_qw)
    count = robot_qw.get_sendContent()
    robot_qw.send(robot_qw.webhook_url, count)

    # url_fs = "https://open.feishu.cn/open-apis/bot/v2/hook/7d17ff4b-7ced-4f5e-a770-d2b410a66363"  # 填写你自己的机器人配置链接
    # robot_fs = FsRobot(url_fs)
    # count = robot_fs.get_sendContent()
    # robot_fs.send(url_fs, count)
