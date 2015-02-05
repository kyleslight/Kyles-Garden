# import MySQLdb

# class DatabaseHandler():
# 	def __init__(self, db):
# 		self.db = MySQLdb.connect(
# 				host = "localhost",
# 				port = 3306,
# 				user = "lk",
# 				passwd = "lk",
# 				db = db
# 			)

# 	def execute_ins(self, ins, para):
# 		cur = self.db.cursor()
# 		cur.execute(ins, para)
# 		cur.close()
# 		self.db.commit()

# 	def get_fetch(self, ins):
# 		cur = self.db.cursor()
# 		cur.execute(ins)
# 		result = cur.fetchall()
# 		cur.close()
# 		return result

import MySQLdb
import MySQLdb.cursors

class DatabaseHandler():
	def __init__(self, db):
		self.db = MySQLdb.connect(
				host = "localhost",
				port = 3306,
				user = "lk",
				passwd = "lk",
				db = db,
				cursorclass=MySQLdb.cursors.DictCursor,
				use_unicode=True,
                charset="utf8",
			)

	def insert(self, table, para, value):
		cur = self.db.cursor()
		ins = "insert into %s %s values %s" %(table, para, value)

		try:
			cur.execute(ins)
			self.db.commit()
		except:
			self.db.rollback()

		cur.close()

	def exe_ins(self, ins, para):
		cur = self.db.cursor()
		cur.execute('SET NAMES utf8;')
		cur.execute('SET CHARACTER SET utf8;')
		cur.execute('SET character_set_connection=utf8;')
		cur.execute("ALTER DATABASE test CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'")
		cur.execute(ins, para)
		self.db.commit()
		cur.close()

	def fetch_one(self, ins):
		cur = self.db.cursor()
		cur.execute(ins)
		data = cur.fetchone()
		cur.close()
		return data

	def fetch_all(self, ins):
		cur = self.db.cursor()
		cur.execute(ins)
		data = cur.fetchall()
		cur.close()
		return data

	def change_name(self, table, uid, name):
		cur = self.db.cursor()
		ins = "update %s set name = '%s' where uid = %d" %(table, name, uid)
		print ins
		try:
			cur.execute(ins)
			self.db.commit()
		except:
			self.db.rollback()

		cur.close()

# my_test_database = Database("test")
# para = "insert into book(title, order_id)"
# data = my_test_database.fetch_all(para)
# print data
# para = "(name, uid)"
# value = "('miao', 1000)"
# my_test_database.insert("first_test", para, value)
# my_test_database.change_name("first_test", 13, "bai")
