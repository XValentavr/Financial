import os

os.environ["SECRET_KEY"] = "7b0342f12ee64296aaaa9738c72ca2c4"
os.environ[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost:3306/financialapp"