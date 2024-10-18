from pymysql import Connection
# 构建到MySQL数据库的链接
conn = Connection(
    host='localhost',   # 主机名（IP）
    port=3306,          # 端口
    user='',        # 自己数据库账户
    password='',  # 自己数据库密码
    autocommit=True     # 自动提交（确认）
)
