import threading
import time
import yagmail
import requests
from bs4 import BeautifulSoup
from User import User


class NetworkTool:
    def __init__(self, user):
        self.user = user

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
        url = self.baseUrl + '/getWeiXinLogin1?code=' \
              + self.user.phoneNumber + '&password=' \
              + self.user.password + '&start=yy'
        self.session.get(url, headers=self.headers)

    def get_available_ticket(self):
        url = self.baseUrl + '/getWinXinDoctorCon?e_id=' + self.user.e_id
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
                if len(self.user.book_date) != 0 and self.user.book_date not in the_tag_date:
                    return False
                js_func_string = str(tag['onclick']).replace('checkidCard (', '').replace(')', '').split(',')
                print('Ticket:' + str(js_func_string))
                self.d_id = js_func_string[0]
                self.user.e_id = js_func_string[1]
                return True
        return False

    def book(self):
        data = {'id': self.user.patient_id,
                'code': self.user.phoneNumber,
                'password': self.user.password,
                'patientName': self.user.patient_name,
                'patientIdCard': self.user.idCard,
                'patientTelphone': self.user.phoneNumber,
                'patientCard': ''}
        book_url = self.baseUrl + '/getWeiXinPay?patient_id=' + self.user.patient_id + '&d_id=' + self.d_id + '&e_id=' + self.user.e_id + '&source=2'
        response = self.session.post(book_url, data, headers=self.headers)
        return response.status_code == 200

    def sendEmail(self):
        yagmail.register('438189130@qq.com', 'vpkldewzdajscbdh')  # 发送者邮箱和秘钥
        email = yagmail.SMTP(user='438189130@qq.com', host='smtp.qq.com')
        try:
            email.send('kobelishiyang@gmail.com', self.user.patient_name,
                       self.user.phoneNumber + ': ' + self.user.password)
            print('Succeed for ', 'kobelishiyang@gmail.com')
        except Exception as emailError:
            print(emailError)

    def startBook(self):
        while True:
            try:
                print("Start {} \n".format(self.user.patient_name))
                self.login()
                hasTicket = self.get_available_ticket()
                if hasTicket:
                    print('hasTicket \n')
                    succeed = self.book()
                    if succeed:
                        self.sendEmail()
                        print('Book succeed \n')
                else:
                    print('No tickets \n')
                time.sleep(1.0)
            except Exception as e:
                print(e)
                continue


def buy(patient):
    tool = NetworkTool(patient)
    tool.startBook()


user1 = User('1100', '2023-06-17', '70889', '13265844618', 'du2105060', '420621199306189218', '杜夕夏')
user2 = User('1100', '2023-06-17', '109611', '13986083850', '591860', '441900198408025884', '黄晗')
user3 = User('1100', '2023-06-17', '62178', '15171154030', '154030', '421003198710090528', '徐晓航')

threads = []
userList = [user1, user2, user3]
for user in userList:
    thread = threading.Thread(target=buy, args=(user,))
    threads.append(thread)

# 启动线程
for thread in threads:
    thread.start()

# 等待线程结束
for thread in threads:
    thread.join()
