import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.options import options, define, parse_command_line

from handlers import SampleWSServer

define('port', type=int, default=8000)


def main():
	parse_command_line()

	settings = dict(
		debug=True
	)

	app = tornado.web.Application(
		[
			(r'/sample/([^/]*)', SampleWSServer),
		],
		**settings
	)

	app.listen(options.port, address='0.0.0.0')

	tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
	main()
