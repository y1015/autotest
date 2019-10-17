"""
    组织测试套件生成测试报告
    流程:
        1.导包
        2.创建套件对象
        3.创建文件流，并且使用工具执行套件，将执行结果写入文件流
"""
# 导包
import unittest

import time

from case.TestTPShopUser import TestUser
from tools.HTMLTestRunner import HTMLTestRunner

# 创建测试套件对象
suite = unittest.TestSuite()
# 添加测试类或测试函数
# suite.addTest(TestUser("test_login_success"))
suite.addTest(unittest.makeSuite(TestUser))

#先创建文件
file_to = "./report/report.html"
# file_to = "./report/report" + time.strftime("%Y%m%d%H%M%S") + ".html"#为文件名称添加时间戳，以避免文件覆盖
# 打开文件流，工具执行套件，并将结果写出
with open(file_to,"wb") as f:
    runner = HTMLTestRunner(f, title="我的测试报告", description="V1.0")
    runner.run(suite)
print("************")
