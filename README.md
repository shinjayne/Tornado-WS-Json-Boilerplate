**Tornado WS Json Boilerplate** is for the developers who want to make json api server with tornado websocket framework.

## Core ability

1. json message form validation

2. smooth error handling while handling message

3.  easy reply with `yield`

4. achieve async using multiple sub thread  


## Tutorial 

#### step1 : Set your json form 

You can set your json api header key and content key. 

If you set your json form like below,  

```python

class SampleWSServer(tornado_extension.JsonWSThreadHandler):
	def __init__(self, *args, **kwargs):
		super(SampleWSServer, self).__init__(*args, **kwargs)
		
		self.type_key = 'head'
		self.content_key = 'body'
		
```

then your json api would be like this ... 

```json
//send
{
  "head": "say_hello",
  "body": {
    "name": "Jayne",
    "email": "shinjayne@gmail.com",
    "gender": "male"
  }
}

//response 
{
  "head": "say_hello",
  "success": true,
  "body": {
    "system" : "Hello Jayne ! Nice to meet you!"
  }
}
```

#### step2 : Create your receiver and set validation rule 

You can create your receiver with json validation check. 

When you create new reciever in `JsonWSThreadHandler`, you should decorate it with `@tornado_extension.message_reciever`.

```python
class SampleWSServer(tornado_extension.JsonWSThreadHandler):

	@tornado_extension.message_receiver(required_set={'name', 'email', 'gender'}, default_dict={'nation':'usa'})
	def say_hello_receiver(self, message):
	    name, email, gender, nation = self.extract_content(message, ['name', 'email', 'gender', 'nation'])
	
		yield True, {'system': 'Hello ' + name + '! Nice to meet you! Are you living in ' + nation + '?'}
```

And if someone send json message like this, (missing required key `email`)
```json
//send
{
  "head": "say_hello",
  "body": {
    "name": "Jayne",
    "gender": "male"
  }
}
```

then she(he) would receive this ... 
```json
{
  "head": "say_hello",
  "success": false,
  "body":  {
    "system": "Please check out the JSON API form. Missing some required contents."
   }
}

```


#### step3 : Register your receivers to router based on `self.type_key`
```python
class SampleWSServer(tornado_extension.JsonWSThreadHandler):
    def __init__(self, *args, **kwargs):
		super(SampleWSServer, self).__init__(*args, **kwargs)
		
		self.type_key = 'head'
		self.content_key = 'body'    
		
		# message router based on type key
		# if type key is 'say_hello', then say_hello_reciever handle that message
		self.receivers = {
		    'say_hello': self.say_hello_receiver
		}
```

#### step4 : Receiver is Python Generator! You can reply more than once! 

When a receiver received message, it runs on a single sub thread, so you can reply message more than once! 

```python
class SampleWSServer(tornado_extension.JsonWSThreadHandler):

	@tornado_extension.message_receiver(required_set={'name', 'email', 'gender'}, default_dict={'nation':'usa'})
	def say_hello_receiver(self, message):
	    name, email, gender, nation = self.extract_content(message, ['name', 'email', 'gender', 'nation'])
	
		yield True, {'system': 'Hello ' + name + '! Nice to meet you! Are you living in ' + nation + '?'}
		
		yield True, {'system': 'And your email is ' + email + '!'}
		
		yield True, {'system': 'And your gender is ' + gender + '!'}
		
		yield True, {'system': 'Good Bye!'}
```


## Waiting for your contribution ! 

Please send pull request or issue when you found some bugs or you improved this boilerplate code.