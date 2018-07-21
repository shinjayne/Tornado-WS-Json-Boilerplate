from utils import tornado_extension


class SampleWSServer(tornado_extension.JsonWSThreadHandler):
	def __init__(self, *args, **kwargs):
		super(SampleWSServer, self).__init__(*args, **kwargs)

		self.type_key = 'head'
		self.content_key = 'body'

		self.receivers = {
			'enter_room': self.enter_room
		}

	@tornado_extension.message_receiver()
	def enter_room(self, message):
		yield True, {'system': 'hello!'}