import time
import smtplib
import yagmail
import requests
from bs4 import BeautifulSoup


class NetworkTool:
    # 专家id
    e_id = '1100'
    # 日期
    book_date = '2023-05-20'
    # 病人id
    patient_id = '118709'
    # 病人账号
    phoneNumber = '13419589441'
    # 病人密码
    password = 'he951110'
    # 身份证
    idCard = '420303199610192826'
    # 姓名
    patient_name = '贺子怡'

    # # 专家id
    # e_id = '1100'
    # # 病人id
    # patient_id = '119230'
    # # 病人账号
    # phoneNumber = '15858199047'
    # # 病人密码
    # password = '123456'
    # # 身份证
    # idCard = '420202199012171230'
    # # 姓名
    # patient_name = '李琴'

    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                         '*/*;q=0.8,'
                         'application/signed-exchange;v=b3;q=0.9',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'micromessenger',
               'Cache-Control': 'no-cache'}

    baseUrl = 'http://www.yztzy.com/assets/weixin'
    session = requests.session()
    # 预约事件id
    d_id = ''

    def login(self):
        url = self.baseUrl + '/getWeiXinLogin1?code=' + self.phoneNumber + '&password=' + self.password + '&start=yy'
        response = self.session.get(url, headers=self.headers)

    def get_available_ticket(self):
        url = self.baseUrl + '/getWinXinDoctorCon?e_id=' + self.e_id
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        time_labels = soup.find_all('em', {'class': 'c-f16 clearfix'})
        tags = soup.find_all('a')
        for index, tag in enumerate(tags):
            the_tag_date = time_labels[index].text
            if "预约(满)" in tag.text:
                print('预约(满)', the_tag_date)
            elif "停诊" in tag.text:
                print('停诊', the_tag_date)
            else:
                if self.book_date not in the_tag_date:
                    return False
                js_func_string = str(tag['onclick']).replace('checkidCard (', '').replace(')', '').split(',')
                print('Ticket:' + str(js_func_string))
                self.d_id = js_func_string[0]
                self.e_id = js_func_string[1]
                return True
        return False

    def book(self):
        data = {'id': self.patient_id,
                'code': self.phoneNumber,
                'password': self.password,
                'patientName': self.patient_name,
                'patientIdCard': self.idCard,
                'patientTelphone': self.phoneNumber,
                'patientCard': ''}
        book_url = self.baseUrl + '/getWeiXinPay?patient_id=' + self.patient_id + '&d_id=' + self.d_id + '&e_id=' + self.e_id + '&source=2'
        response = self.session.post(book_url, data, headers=self.headers)
        return response.status_code == 200

    def sendEmail(self):
        yagmail.register('438189130@qq.com', 'vpkldewzdajscbdh')  # 发送者邮箱和秘钥
        email = yagmail.SMTP(user='438189130@qq.com', host='smtp.qq.com')
        try:
            email.send('kobelishiyang@gmail.com', self.patient_name, self.phoneNumber + ': ' + self.password)
            print('Succeed for ', 'kobelishiyang@gmail.com')
        except Exception as emailError:
            print(emailError)


try:
    while True:
        print('Start')
        tool = NetworkTool()
        tool.login()
        hasTicket = tool.get_available_ticket()
        if hasTicket:
            print('hasTicket')
            succeed = tool.book()
            if succeed:
                print('Book succeed')
                tool.sendEmail()
                break
        else:
            print('No tickets')
        time.sleep(1.0)
except Exception as e:
    print(e)
