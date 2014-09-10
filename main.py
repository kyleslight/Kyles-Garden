# coding=utf-8

import os.path

from tornado import httpserver
from tornado import ioloop
from tornado.web import RequestHandler, Application, UIModule
from tornado.options import define, options, parse_command_line
from urllib2 import Request, urlopen, URLError, HTTPError

from tornado.escape import json_encode, json_decode
from pyquery import PyQuery as py

import pymongo

define("port", default = 8000, help = "run on given port", type = int)
define("debug", default = True, type = bool)
define("host", default = "localhost", type = str)

# class ApplicationHandler(Application):
# 	def __init__(self):
		
# 		conn = pymongo.Connection("127.0.0.1", 27017)
# 		self.db = content['test_1']
# 		Application.__init__(self, handlers, debug = True)

class IndexHandler(RequestHandler):
	def get(self):
		self.render('index.html')

# 	def write_error(self, status_code, **kwargs):
# 		self.write("Gosh!, you have occured a %d error. What a pity" %status_code)

# class PoemMakeHandler(RequestHandler):
# 	def post(self):
# 		words = {}
# 		words['noum1'] = self.get_argument('noum1')
# 		words['noum2'] = self.get_argument('noum2')
# 		words['verb'] = self.get_argument('verb')
# 		words['noum3'] = self.get_argument('noum3')
# 		self.render('poem.html', words = words)

# class BookHandler(RequestHandler):
# 	def get(self):
# 		self.render('book.html')

# class SuggestionHandler(RequestHandler):
# 	def get(self, suggestiontext):
# 		suggestiontext = suggestiontext.encode('utf-8')
# 		suggest_url = r'http://www.sogou.com/web?query='+suggestiontext+r'&interation=196647&chuidq=39&sourceid=inttab_zhishi'
# 		req = Request(suggest_url)
# 		res = urlopen(req).read()
# 		p = py(res)
# 		result = p(".rb")

# 		blog_list = []
# 		for i in xrange(0, len(result) - 1):
# 			result_temp = result.eq(i)
# 			blog = {}
# 			blog['title'] = result_temp.find(".pt a").text()
# 			blog['content'] = result_temp.find(".ft").text()
# 			blog['link'] = result_temp.find(".pt a").attr("href")
# 			blog_list.append(blog)

# 		self.write(json_encode(blog_list))

# class DictHandler(RequestHandler):
# 	def get(self, word):
# 		self.write("you wnat you search : %s" %word)

# class BookModule(UIModule):
# 	def render(self):
# 		return "<h1>This is a book</h1>"

# 	def embedded_javascript(self): 
# 		return "document.write(\"hi!\")"


if __name__ == "__main__":
	parse_command_line()
	app = Application(
		handlers = [
			(r"/", IndexHandler),],
			# (r'/poem', PoemMakeHandler),
			# (r'/book', BookHandler),
			# (r'/suggestion/(\w+)', SuggestionHandler),
			# (r'/dict/(\w+)', DictHandler)],
		debug = True,
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		)
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port)
	ioloop.IOLoop.instance().start()
