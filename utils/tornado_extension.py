from tornado.websocket import WebSocketHandler
import threading
import json


class JsonWSThreadHandler(WebSocketHandler):

	def __init__(self, *args, **kwargs):
		# override
		super(JsonWSThreadHandler, self).__init__(*args, **kwargs)

		self.type_key = 'type'
		self.content_key = 'content'
		self.receivers = dict()

	def data_received(self, chunk):
		pass

	def check_origin(self, origin):
		return True

	def open(self, *args, **kwargs):
		pass

	def on_close(self):
		pass

	def on_message(self, message):

		try:
			message = json.loads(message)
			receiver = self.receivers[message[self.type_key]]

		except Exception as e:
			return

		receiver_thread = threading.Thread(target=receiver, args=(message,))
		receiver_thread.start()

	def reply(self, message, success, content):
		self.write_message({
			self.type_key: message[self.type_key],
			'success': success,
			self.content_key: content
		})

	def extract_content(self, message, keylist):
		content = message[self.content_key]
		result = []
		for key in keylist:
			result.append(content[key])

		if len(result) == 1:
			result = result[0]
		return result


def message_receiver(required_set=set(), defaults_dict=dict()):
	"""
	JsonWSThreadHandler 의 receiver 사용할 수 있는 decorator.
	message.content 의 required key 에 대해 validation 을 체크하고, optional key 에 대해선 default 값을 지정한다
	응답 메세지를 전송한다
	에러 자동 처리 후 에러 메세지도 전송한다

	:param required_set: required key 들의 집합 (string)
	:param defaults_dict: optional key 들과 디폴트 값들의 사전 (string : object)
	:return:
	"""
	def _(origin_function):
		def wrapper_function(self, message, *args, **kwargs):
			try:
				if self.content_key not in message:
					message[self.content_key] = {}

				# required set 안에 있는 것이 모두 있는지
				if not required_set.issubset(set(message[self.content_key].keys())):
					self.reply(message, False, {'system': 'Please check out the JSON API form. Missing some required contents.'})
					return

				# optional 값들이 없다면 default dict 에서 채워서 넣기
				for key, item in defaults_dict.items():
					if key not in message[self.content_key].keys():
						message[self.content_key][key] = item

				# origin function 이 generator 이므로 메세지 yield 할 때마다 전송
				generator = origin_function(self, message, *args, **kwargs)

				for success, content in generator:
					self.reply(message=message, success=success, content=content)

				return
			except Exception as e:
				self.reply(message, False, {'system': str(e)})

		return wrapper_function
	return _

