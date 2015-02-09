# coding=utf-8

import os.path

from tornado import httpserver
from tornado import ioloop
from tornado.web import RequestHandler, Application, UIModule
from tornado.options import define, options, parse_command_line
import MySQLdb
import tornado.web

from datetime import date
import datetime

import data
import base64, uuid

from tornado.escape import json_encode, json_decode

define("port", default = 8000, help = "run on given port", type = int)
define("debug", default = True, type = bool)
define("host", default = "localhost", type = str)

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("SU")

class BrowseHandler(BaseHandler):
	def get(self):
		SU = self.get_secure_cookie("SU")

		test_database = data.DatabaseHandler("test")
		para = "select id, title, description, collect_id, order_id, insert_time from article_6 order by id desc limit 20"
		articles = test_database.fetch_all(para)

		if articles:
			for article in articles:
				collection_id = article['collect_id']
				ins = "select title from collect where id = %s" %collection_id

				article_collection = test_database.fetch_one(ins)
				if article_collection:
					article['collection_title'] = test_database.fetch_one(ins)['title']
				else:
					article['collection_title'] = ''

				ins_2 = "select id from article_6 where collect_id = %s" %collection_id
				article['collection_first_article'] = test_database.fetch_one(ins_2)['id']

				ins_3 = "select book_id from collect where id = %s" %collection_id
				bid = test_database.fetch_one(ins_3)['book_id']

				ins_4 = "select title from book where id = %s" %bid
				article['book_title'] = test_database.fetch_one(ins_4)['title']

		para_2 = "select * from book order by id desc"
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

		if SU:
			self.login_render(articles, books, SU)
		else:
			self.guest_render(articles, books, SU)

	@tornado.web.authenticated
	def login_render(self, articles, books, SU):
		self.render('browse.html', articles = articles, books = books, SU = SU)

	def guest_render(self, articles, books, SU):
		self.render('browse.html', articles = articles, books = books, SU = SU)


	def post(self):
		print self.get_argument('password')
		if self.get_argument("name") == 'kyleslight' and self.get_argument('password') == '3a62d09710ff56a3e4cbd31b43323b41':
		    self.set_secure_cookie("SU", self.get_argument("name"))
		    self.write(json_encode({'message' : 'login success'}))
		else:
			self.write(json_encode({'message' : 'bad login'}))
	

class ArticleHandler(BaseHandler):
	def get(self, aid):
		SU = self.get_secure_cookie("SU")

		test_database = data.DatabaseHandler("test")
		ins = "select content from article_6 where id = %s" %aid
		maintext = test_database.fetch_one(ins)['content']

		ins_2 = "select collect_id, insert_time from article_6 where id = %s" %aid
		collection_id = test_database.fetch_one(ins_2)['collect_id']
		article_date = test_database.fetch_one(ins_2)['insert_time']

		ins_3 = "select * from collect where id = %s" %collection_id
		collection = test_database.fetch_one(ins_3)

		ins_4 = "select title, id from article_6 where collect_id = %s" %collection_id
		collection_articles = test_database.fetch_all(ins_4)

		self.render('article.html', maintext = maintext, article_date = article_date, collection = collection, collection_articles = collection_articles, aid = aid, SU = SU)


class BookCreateHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.create()

	def create(self):
		test_database = data.DatabaseHandler("test")
		title = self.get_argument('title').encode('utf-8')
		ins = "select count(*) from book"
		order = test_database.fetch_one(ins)['count(*)'] + 1
		print order
		ins_2 = "insert into book(title, order_id) value(%s, %s)"
		para = (title, order)
		result = test_database.exe_ins(ins_2, para)

		ins_3 = "select id from book order by id desc"
		book_id = test_database.fetch_one(ins_3)['id']

		book_info = {'id' : book_id, 'title' : title}
		self.write(json_encode(book_info))


class BookModifyHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.modify()

	def modify(self):
		test_database = data.DatabaseHandler('test')
		title = self.get_argument('title').encode('utf-8')
		bid = self.get_argument('id')

		ins = "update book set title = %s where id = %s"
		para = (title, bid)
		result = test_database.exe_ins(ins, para)

		ins_2 = "select title from book where id = %s" %bid
		updated_title = test_database.fetch_one(ins_2)['title']

		book_info = {'id' : bid, 'title' : updated_title}
		self.write(json_encode(book_info))

class BookDeleteHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, bid):
		
		test_database = data.DatabaseHandler("test")
		ins = "select id from collect where book_id = %s" %bid
		collection_ids = test_database.fetch_all(ins)

		for collection_id in collection_ids:
			cid = collection_id['id']
			ins_2 = "delete from article_6 where collect_id = %s" %cid
			para_2 = ()
			result_1 = test_database.exe_ins(ins_2, para_2)

			ins_3 = "delete from collect where id = %s" %cid
			para_3 = ()
			result_2 = test_database.exe_ins(ins_3, para_3)

		ins_4 = "delete from book where id = %s" %bid
		para_4 = ()
		result = test_database.exe_ins(ins_4, para_4)

		self.redirect('/')


class CollectionCreateHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.create()

	def create(self):
		title = self.get_argument('title').encode('utf-8')
		book_id = self.get_argument('book_id')
		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from collect where book_id = %s" %book_id
		order = test_database.fetch_one(ins)['count(*)'] + 1
		ins_2 = "insert into collect(title, book_id, order_id) value(%s, %s, %s);"
		para = (title, book_id, order)
		result = test_database.exe_ins(ins_2, para)

		ins_3 = "select id from collect order by id desc"
		collection_id = test_database.fetch_one(ins_3)['id']

		collection_info = {'id' : collection_id, 'title' : title, 'book_id' : book_id}
 		self.write(json_encode(collection_info))

class CollectionModifyHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.modify()

	def modify(self):
		test_database = data.DatabaseHandler('test')
		title = self.get_argument('title').encode('utf-8')
		cid = self.get_argument('id')

		ins = "update collect set title = %s where id = %s"
		para = (title, cid)
		result = test_database.exe_ins(ins, para)

		ins_2 = "select title from collect where id = %s" %cid
		updated_title = test_database.fetch_one(ins_2)['title']

		collection_info = {'id' : cid, 'title' : updated_title}
		self.write(json_encode(collection_info))

class CollectionDeleteHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, cid):
		
		test_database = data.DatabaseHandler("test")
		ins = "delete from article_6 where collect_id = %s" %cid
		para = ()
		result = test_database.exe_ins(ins, para)

		ins_2 = "delete from collect where id = %s" %cid
		para_2 = ()
		result_2 = test_database.exe_ins(ins_2, para_2)

		self.redirect('/')

class EditHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, cid):
		SU = self.get_secure_cookie("SU")
		self.render('edit.html', cid = cid, SU = SU)	

class ArticleCreateHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.create()

		test_database = data.DatabaseHandler("test")
		ins = "select id from article_6 order by id desc"
		article_id = test_database.fetch_one(ins)['id']
		url = "/article/%s" %article_id
		self.redirect(url)

	def create(self):
		title = self.get_argument('arttitle').encode('utf-8')
		maintext = self.get_argument('maintext').encode('utf-8')
		description = self.get_argument('artdes').encode('utf-8')
		ori_text = self.get_argument('ori_text').encode('utf-8')
		collection_id = self.get_argument('cid')
		insert_time = date.today()

		# get the order number of article in this collection
		test_database = data.DatabaseHandler("test")
		ins = "select count(*) from article_6 where collect_id = %s" %collection_id
		order = test_database.fetch_one(ins)['count(*)'] + 1

		test_database = data.DatabaseHandler("test")
		ins = "insert into article_6(title, description, content, ori_text, collect_id, order_id, insert_time) value(%s, %s, %s, %s, %s, %s, %s)"
		para = (title, description, maintext, ori_text, collection_id, order, insert_time)
		result = test_database.exe_ins(ins, para)
		

class ArticleTobeModifyHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, aid):
		SU = self.get_secure_cookie("SU")

		test_database = data.DatabaseHandler("test")
		ins = "select ori_text, collect_id from article_6 where(id = %s)" %aid
		article_tobe_modify = test_database.fetch_one(ins)
		self.render('modify.html', aid = aid, article_tobe_modify = article_tobe_modify, SU = SU)

class ArticleModifyHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self, aid):
		self.modify(aid)

		test_database = data.DatabaseHandler("test")
		url = "/article/%s" %aid
		self.redirect(url)

	def modify(self, aid):
		title = self.get_argument('arttitle').encode('utf-8')
		maintext = self.get_argument('maintext').encode('utf-8')
		description = self.get_argument('artdes').encode('utf-8')
		ori_text = self.get_argument('ori_text').encode('utf-8')
		collection_id = self.get_argument('cid')

		test_database = data.DatabaseHandler("test")
		ins = "update article_6 set title = %s, description = %s, content = %s, ori_text = %s where id = %s"
		para = (title, description, maintext, ori_text, aid)
		result = test_database.exe_ins(ins, para)


class ArticleDeleteHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, aid):
		
		test_database = data.DatabaseHandler('test')
		ins = "delete from article_6 where id = %s" %aid
		para = ()

		result = test_database.exe_ins(ins, para)

		self.redirect('/')


# class LoginHandler(BaseHandler):
#     def get(self):
#         self.write('<html><body><form action="/login" method="post">'
#                    'Name: <input type="text" name="name">'
#                    '<input type="submit" value="Sign in">'
#                    '</form></body></html>')

#     def post(self):

# 	    self.set_secure_cookie("user", self.get_argument("name"))
# 	    self.redirect("/")

# class MainHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         name = tornado.escape.xhtml_escape(self.current_user)
#         self.write("Hello, " + name)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('SU')
        self.redirect('/')

settings = dict(
    		cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    		xsrf_cookies = True,
    		login_url = "/login", # 默认的登陆页面，必须有
    		debug = True,
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			)


if __name__ == "__main__":
	parse_command_line()
	app = Application(
		handlers = [
			(r'/article/create', ArticleCreateHandler),
			(r'/', BrowseHandler),
			(r'/login', BrowseHandler),
			(r'/logout', LogoutHandler),
			(r'/article/(\w+)', ArticleHandler),
			(r'/edit/article/(\w+)', ArticleTobeModifyHandler),
			(r'/modify/article/(\w+)', ArticleModifyHandler),
			(r'/modify/book/', BookModifyHandler),
			(r'/modify/collection/', CollectionModifyHandler),
			(r"/edit/collection/(\w+)", EditHandler),
			(r'/delete/book/(\w+)', BookDeleteHandler),
			(r'/delete/collection/(\w+)', CollectionDeleteHandler),
			(r'/delete/article/(\w+)', ArticleDeleteHandler),
			(r'/book/add', BookCreateHandler),
			(r'/collection/add', CollectionCreateHandler),], **settings
		
		)
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port)
	ioloop.IOLoop.instance().start()
