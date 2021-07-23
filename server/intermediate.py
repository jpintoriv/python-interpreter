import time
import json
import zmq
from multiprocessing import Queue 
class Intermediate:

	ipc_address = None
	ipc_supervisor = None
	ipc_interpreter = None
	context = None
	playloads_queue = None

	def __init__(self, ipc_address, ipc_supervisor, ipc_interpreter):
		self.ipc_address = ipc_address
		self.ipc_supervisor = ipc_supervisor
		self.ipc_interpreter = ipc_interpreter
		self.context = zmq.Context()

		playloads_queue = Queue()

	def get_state(self):
		message = {"channel":"get_state"}
		socket_supervisor = self.context.socket(zmq.REQ)
		socket_supervisor.connect(self.ipc_supervisor)
		socket_supervisor.send_json(message)
		state = socket_supervisor.recv_json()
		socket_supervisor.disconnect(self.ipc_supervisor)
		return state

	def send_heartbreak(self):
		pass

	def send_playload(self, playload):
		pass
	
	def run(self):
		socket = self.context.socket(zmq.REP)
		print("Binding intermediate in: "+self.ipc_address)
		socket.bind(self.ipc_address)
		print("Binding intermediate ok")

		state = self.get_state()

		while True:
			message = socket.recv_json()
			print("Mensaje recibido por intermediate:")
			print(message)

			if(message["channel"]=="notify_state"):
				state = message[""]
			
			if(message["channel"]=="RUN" or message["channel"]=="KILL"):
				self.playloads_queue.put(message)

			if(message["channel"]=="HEARTBEAT"):
				self.send_heartbreak()

			if(state == "FREE"):
				if(not self.playloads_queue.empty()):
					playload = playloads_queue.get()
					self.send_playload(playload)