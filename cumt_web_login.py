import requests, re

def Time():
    import time
    t = time.time()
    return int(round(t*1000))

class CUMT():

    def __init__(self, user, password, company):
        self.user = user
        self.password = password
        self.company = company

        if not self.check_status():
            self.login()

    def check_status(self):
        '''
        判断是否在线
        简单模拟http://10.2.5.251/a41.js?version=1592541085614 中的checkStatus函数
        '''
        self.check_time = Time()
        check_url = 'http://10.2.5.251/drcom/chkstatus?callback=dr{}'.format(self.check_time)
        print('检测登录状态的网址为：', check_url)
        check_html = requests.get(check_url)
        #响应包形如：
        #dr1592541086816({"result":1,"time":1,"flow":0,"fsele":1,"fee":0,"m46":0,"v46ip":"10.4.190.194","myv6ip":"","oltime":15552060,"olflow":4294967295,"lip":"","stime":"","etime":"","uid":"08183035@unicom","v6af":0,"v6df":0,"v46m":0,"v4ip":"10.4.190.194","v6ip":"::","AC":"08183035@unicom","ss5":"10.4.190.194","ss6":"10.2.5.251","vid":0,"ss1":"000d484c182f","ss4":"000000000000","cvid":0,"pvid":0,"hotel":0,"aolno":18020,"eport":0,"eclass":1,"zxopt":1,"NID":"","olmac":"480eec81bde0","ollm":10,"olm1":"00000000","olm2":"0000","olm3":0,"olmm":1,"olm5":0,"gid":2,"actM":1,"actt":85,"actdf":0,"actuf":0,"act6df":0,"act6uf":0,"allfm":1,"d1":0,"u1":0,"d2":0,"u2":0,"o1":0,"nd1":0,"nu1":0,"nd2":0,"nu2":0,"no1":0})   
        status = re.search(r'"result":(\d),', check_html.text).group(1)
        if status == '1':
            print('!!!目前已在线!!!')
            return True
        else:
            print('!!!目前未在线!!!')
            return False


    def login(self):

        # 获取登录页网址
        test_url = 'http://baidu.com'
        test_html = requests.get(test_url)
        login_page_url = re.search(r"<script>top\.self\.location\.href='(.+?)'</script>", test_html.text).group(1)
        print('登录页网址为：', login_page_url)


        # 从登录页网址中获取一些变量值
        wlan_user_ip = re.search(r'wlanuserip=(.+?)&', login_page_url).group(1)
        wlan_user_mac = re.search(r'mac=(.+?)&', login_page_url).group(1)
        wlan_ac_name = re.search(r'wlanacname=(.+?)&', login_page_url).group(1)
        login_time = Time()


        # 登录请求
        login_url = 'http://10.2.5.251:801/eportal/?c=Portal&a=login&callback=dr{}&login_method=1&user_account={}%40{}&user_password={}&wlan_user_ip={}&wlan_user_mac={}&wlan_ac_ip=&wlan_ac_name={}&jsVersion=3.0&_={}'.format(self.check_time, self.user, self.company, self.password, wlan_user_ip, wlan_user_mac, wlan_ac_name, login_time)
        print('登录请求为：', login_url)
        res = requests.get(login_url)
        # 响应包形如：
        # dr1592542850917({"result":"1","msg":"认证成功"})
        print('响应包为：', res.content.decode('utf-8'))



user = '学号'
password = '密码'
company = 'unicom'
# 中国移动cmcc  中国联通unicom  中国电信telecom

c = CUMT(user, password, company)