from pymysql import Connection
# 构建到MySQL数据库的链接
conn = Connection(
    host='localhost',   # 主机名（IP）
    port=3306,          # 端口
    user='root',        # 账户
    password='mysql',  # 密码
    autocommit=True     # 自动提交（确认）
)