# coding=utf-8

import os.path

from tornado import httpserver
from tornado import ioloop
from tornado.web import RequestHandler, Application, UIModule
from tornado.options import define, options, parse_command_line
import MySQLdb

from datetime import date
import datetime

import data

from tornado.escape import json_encode, json_decode

define("port", default = 8000, help = "run on given port", type = int)
define("debug", default = True, type = bool)
define("host", default = "localhost", type = str)

class BrowseHandler(RequestHandler):
	def get(self):
		test_database = data.DatabaseHandler("test")
		para = "select id, title, description, collect_id, order_id, insert_time from article_6 order by id desc limit 20"
		articles = test_database.fetch_all(para)

		if articles:
			for article in articles:
				collection_id = article['collect_id']
				ins = "select title from collect where id = %s" %collection_id

				article['collection_title'] = test_database.fetch_one(ins)['title']

				ins_2 = "select id from article_6 where collect_id = %s" %collection_id
				article['collection_first_article'] = test_database.fetch_one(ins_2)['id']

		para_2 = "select * from book"
		books = test_database.fetch_all(para_2)

		if books:
			for book in books:
				book_id = book['id']
				ins = "select * from collect where book_id = %s" %book_id
				bookcollections = test_database.fetch_all(ins)
				book['bookcollections'] = bookcollections

				for bookcollection in book['bookcollections']:
					collection_id = bookcollection['id']
					ins_2 = "select * from article_6 where collect_id = %s" %collection_id
					article = test_database.fetch_one(ins_2)
					if article:
						bookcollection['articleid'] = article['id']
						bookcollection['is_empty'] = False
					else:
						bookcollection['is_empty'] = True

		self.render('browse.html', articles = articles, books = books)

class ArticleHandler(RequestHandler):
	def get(self, aid):

		test_database = data.DatabaseHandler("test")
		ins = "select content from article_6 where(id = %s)" %aid
		maintext = test_database.fetch_one(ins)['content']

		ins_2 = "select collect_id, insert_time from article_6 where id = %s" %aid
		collection_id = test_database.fetch_one(ins_2)['collect_id']
		article_date = test_database.fetch_one(ins_2)['insert_time']

		ins_3 = "select * from collect where id = %s" %collection_id
		collection = test_database.fetch_one(ins_3)

		ins_4 = "select title, id from article_6 where collect_id = %s" %collection_id
		collection_articles = test_database.fetch_all(ins_4)

		self.render('article.html', maintext = maintext, article_date = article_date, collection = collection, collection_articles = collection_articles, aid = aid)



class CollectionHandler(RequestHandler):
	def get(self, cid):
		self.render('collection.html')


class EditHandler(RequestHandler):
	def get(self, cid):
		self.render('edit.html', cid = cid)

class ArticleCreateHandler(RequestHandler):
	def post(self):
		self.create()

		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from article_6"
		article_id = test_database.fetch_one(ins)['count(*)']
		url = "/article/%s" %article_id
		self.redirect(url)

	def create(self):
		title = self.get_argument('arttitle')
		maintext = self.get_argument('maintext')
		description = self.get_argument('artdes')
		collection_id = self.get_argument('cid')
		insert_time = date.today()

		# get the oredr number of article in this collection
		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from article_6 where collect_id = %s" %collection_id
		order = test_database.fetch_one(ins)['count(*)'] + 1

		test_database = data.DatabaseHandler("test")
		ins = "insert into article_6(title, description, content, collect_id, order_id, insert_time) value(%s, %s, %s, %s, %s, %s)"
		para = (title, description, maintext, collection_id, order, insert_time)
		print para
		result = test_database.exe_ins(ins, para)
		# print result

class BookCreateHandler(RequestHandler):
	def get(self):
		self.create()

	def create(self):
		title = self.get_argument('title')
		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from book"
		order = test_database.fetch_one(ins)['count(*)'] + 1
		print order
		ins_2 = "insert into book(title, order_id) value(%s, %s)"
		para = (title, order)
		result = test_database.exe_ins(ins_2, para)

		ins_3 = "select count(*) from book"
		book_id = test_database.fetch_one(ins_3)['count(*)']

		book_info = {'id' : book_id, 'title' : title}
		self.write(json_encode(book_info))

class CollectionCreateHandler(RequestHandler):
	def get(self):
		self.create()

	def create(self):
		title = self.get_argument('title')
		book_id = self.get_argument('book_id')
		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from collect where book_id = %s" %book_id
		order = test_database.fetch_one(ins)['count(*)'] + 1
		ins_2 = "insert into collect(title, book_id, order_id) value(%s, %s, %s);"
		para = (title, book_id, order)
		result = test_database.exe_ins(ins_2, para)

		ins_3 = "select count(*) from collect"
		collection_id = test_database.fetch_one(ins_3)['count(*)']

		collection_info = {'id' : collection_id, 'title' : title, 'book_id' : book_id}
 		self.write(json_encode(collection_info))

	


if __name__ == "__main__":
	parse_command_line()
	app = Application(
		handlers = [
			(r'/article/create', ArticleCreateHandler),
			(r'/', BrowseHandler),
			(r'/article/(\w+)', ArticleHandler),
			(r"/edit/collection/(\w+)", EditHandler),
			(r'/book/add', BookCreateHandler),
			(r'/collection/add', CollectionCreateHandler),],
		debug = True,
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		)
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port)
	ioloop.IOLoop.instance().start()
