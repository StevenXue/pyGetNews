#! /usr/bin/python
# -*- coding:utf-8 -*-
import sqlite3 # 导入 sqlite3 模块
# 连接数据库 company.db袁如果该数据库不存在，则创建一个
# 数据库
conn = sqlite3.connect('company.db')
cur=conn.cursor()
# 创建一个表 EMPLOYEE
cur.execute('''CREATE TABLE EMPLOYEE
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT NOT NULL ,
AGE INT NOT NULL ,
SEX CHAR(1) NOT NULL,
ADDRESS CHAR(50));''')
# 插入数据
cur.execute ("INSERT INTO EMPLOYEE (NAME,AGE,SEX,ADDRESS) VALUES (' 王丽 ',25,'女',' 北京 ')")
# 执行多个 sql 数据，sql 语句用分号(;)隔开
cur.executescript("""
INSERT INTO EMPLOYEE (NAME,AGE,SEX,ADDRESS)
VALUES (' 张三 ',28,'男',' 浙江杭州 ');
INSERT INTO EMPLOYEE (NAME,AGE,SEX,ADDRESS)
VALUES (' 丽丽 ',22,'女',' 江苏南京 ');
INSERT INTO EMPLOYEE (NAME,AGE,SEX,ADDRESS)
VALUES ('Tom',40,'男','USA');
""")
# 提交当前事务
conn.commit()
# 查询数据
cur.execute("SELECT * FROM EMPLOYEE")
# 打印出结果集中的所有行
for row in cur:
	print "ID=>", row[0]
	print "NAME=>", row[1]
	print "AGE=>",row[2]
	print "SEX=>",row[3]
	print "ADDRESS=>", row[4]
# 更新数据
cur.execute ("UPDATE EMPLOYEE set ADDRESS = ' 上海 'where ID=1")
conn.commit
# 删除数据
cur.execute("DELETE FROM EMPLOYEE WHERE ID = 4")
conn.commit()
# 关闭数据库连接
conn.close()