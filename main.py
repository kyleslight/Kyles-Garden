# coding=utf-8

import os.path

from tornado import httpserver
from tornado import ioloop
from tornado.web import RequestHandler, Application, UIModule
from tornado.options import define, options, parse_command_line
import MySQLdb

import data

from tornado.escape import json_encode, json_decode

define("port", default = 8000, help = "run on given port", type = int)
define("debug", default = True, type = bool)
define("host", default = "localhost", type = str)

class BrowseHandler(RequestHandler):
	def get(self):
		self.render('browse.html')

class ArticleHandler(RequestHandler):
	def get(self, aid):
		test_database = data.DatabaseHandler("kylesgarden_test")
		ins = "select maintext from article where(aid = %s)" %aid
		maintext = test_database.get_fetch(ins)
		maintext = str(maintext[0][0])
		self.render('article.html', maintext = maintext)

class EditHandler(RequestHandler):
	def get(self):
		self.render('edit.html')

class ArticleCreateHandler(RequestHandler):
	def post(self):
		self.create()
		self.write("congratulations!")

	def create(self):
		uid = 1
		title = "haha"
		collid = 12
		maintext = self.get_argument('maintext')
		print maintext
		descrbtion = "dsjfhkjsdfhks"

		test_database = data.DatabaseHandler("kylesgarden_test")
		ins = "insert into article(uid, title, collid, maintext, descrbtion) value(%s, %s, %s, %s, %s)"
		para = (uid, title, collid, maintext, descrbtion)
		test_database.execute_ins(ins, para)




if __name__ == "__main__":
	parse_command_line()
	app = Application(
		handlers = [
			(r'/article/create', ArticleCreateHandler),
			(r'/browse', BrowseHandler),
			(r'/article/(\w+)', ArticleHandler),
			(r"/edit", EditHandler),],
		debug = True,
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		)
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port)
	ioloop.IOLoop.instance().start()
