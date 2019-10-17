"""
    编写 unittest 相关实现:
        请求业务封装进 api 包
"""
# 导包
import unittest
import requests

import app
from api.UserAPI import UserLogin
import json

# 参数化步骤1:导包
from parameterized import parameterized
# 设置文件解析函数
def read_json():
    # 怎么读取 JSON 文件
    # 1.设置一个接收数据的列表
    data = []
    # 2.开启文件流，读数据并将数据导入列表
    with open(app.PRO_PATH + "/data/login_data.json","r",encoding="utf-8") as f:
        """
            json 解析
        """
        #all = json.load(f)
        # vs = json.load(f).values()
        # #print("整个文件流:",all)
        # print("大值:",vs)
        for value in json.load(f).values():
            #print("value=",value)
            #获取 value 中每一个小值
            username = value.get("username")
            password = value.get("password")
            verify_code = value.get("verify_code")
            status = value.get("status")
            msg = value.get("msg")
            # 将所有字段组织成元组，再将元组追加进列表
            ele = (username,password,verify_code,status,msg)
            data.append(ele)
            # data.append((username,password,verify_code,status,msg))
    # 3.返回列表
    return data
    #return [("13012345678","123456","8888",1,"登陆成功"),("13012345679","123456","8888",-1,"账号有误"),("13012345678","123457","8888",-2,"密码错误")]

# 创建测试类
class TestUser(unittest.TestCase):

    #初始化函数
    def setUp(self):
        #初始化 session
        self.session = requests.Session()
        # 创建 UserLogin 对象
        self.user_obj = UserLogin()

    #资源销毁函数
    def tearDown(self):
        #销毁 session
        self.session.close()


    #测试函数1: 获取验证码
    def test_get_verify_code(self):
        # 1.请求业务
        # 调用 get_verify_code 函数
        response = self.user_obj.get_verify_code(self.session)
        # 2.断言业务
        self.assertEqual(200,response.status_code)
        self.assertIn("image",response.headers.get("Content-Type"))

    #测试函数2: 登录
    def test_login_success(self):
        # 1.请求业务
        # 调用 get_verify_code 函数
        response1 = self.user_obj.get_verify_code(self.session)
        # 调用 login 函数
        response2 = self.user_obj.login(self.session,
                                        "13012345678","123456","8888")
        # 2.断言业务
        print(response2.json())

    #测试函数3: 以参数化的方式读取测试数据然后执行登录
    """
        参数化:动态(程序驱动代替人工驱动)的生成或导入数据
        流程:
            1.导包
            from parameterized import parameterized
            2.定义一个获取数据的函数
            def read_json():
                # .....
                return [("13012345678","123456","8888",1,"登陆成功"),("13012345679","123456","8888",-1,"账号有误"),("13012345678","123457","8888",-2,"密码错误")]
            3.测试函数声明 @parameterized.expand(函数) 将数据导入测试函数
    """
    @parameterized.expand(read_json())
    def test_login(self,username,password,verify_code,status,msg):
        print("-"*100)
        print(username,password,verify_code,status,msg)
        # 1.请求业务
        # 调用 api 包下对象的相关函数
        # 1.1 现获取验证码
        response1 = self.user_obj.get_verify_code(self.session)
        # 1.2 再执行登录
        response2 = self.user_obj.login(self.session,username,password,verify_code)
        # 2.断言业务
        print(response2.json())
        self.assertEqual(status,response2.json().get("status"))
        self.assertIn(msg,response2.json().get("msg"))

