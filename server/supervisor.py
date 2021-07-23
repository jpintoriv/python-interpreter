import time
import json
import zmq

class Supervisor:
	__STATES = {
		1 : "FREE",
		2 : "BUSSY",
		3 : "KILLING",
		4 : "ERROR"
	}

	state = None
	ipc_address = None
	ipc_interpreter = None
	ipc_intermediate = None
	context = None

	def __init__(self, ipc_intermediate, ipc_address, ipc_interpreter):
		self.state = self.__STATES[1]
		self.ipc_address = ipc_address
		self.ipc_intermediate = ipc_intermediate
		self.ipc_interpreter = ipc_interpreter
		self.context = zmq.Context()

	def get_state(self):
		return {"state":self.state}

	def set_state(self, new_state):
		self.state = new_state

		return self.get_state()

	def notify_changes(self):
		message = {"channel":"notify_state", "state":self.state}
		socket_intermediate = self.context.socket(zmq.REQ)
		socket_intermediate.connect(self.ipc_intermediate)
		socket_intermediate.send_json(message)
		socket_intermediate.disconnect(self.ipc_intermediate)
	
	def run(self):
		socket = self.context.socket(zmq.REP)
		print("Binding supervisor in: "+self.ipc_address)
		socket.bind(self.ipc_address)
		print("Binding supervisor ok")

		while True:
			message = socket.recv_json()

			print("Mensaje recibido por supervisor:")
			print(message)

			if(message["channel"] == "get_state"):
				socket.send_json(self.get_state())

			if(message["channel"] == "set_state"):
				new_state = self.set_state(message["new_state"])
				self.notify_changes()