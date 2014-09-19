import MySQLdb

class DatabaseHandler():
	def __init__(self, db):
		self.db = MySQLdb.connect(
				host = "localhost",
				port = 3306,
				user = "lk",
				passwd = "lk",
				db = db
			)

	def execute_ins(self, ins, para):
		cur = self.db.cursor()
		cur.execute(ins, para)
		cur.close()
		self.db.commit()

	def get_fetch(self, ins):
		cur = self.db.cursor()
		cur.execute(ins)
		result = cur.fetchall()
		cur.close()
		return result