import time
import json
import zmq

class Interpreter:

	ipc_address = None
	ipc_supervisor = None
	ipc_intermediate = None

	def __init__(self, ipc_intermediate, ipc_supervisor, ipc_address):
		self.ipc_address = ipc_address
		self.ipc_supervisor = ipc_supervisor
		self.ipc_intermediate = ipc_intermediate
	
	def run():
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind(ipc_address)

		while True:
			message = socket.recv_json()
			print("Mensaje recibido por interprete")