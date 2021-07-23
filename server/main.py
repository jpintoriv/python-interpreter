from multiprocessing import Process
from intermediate import Intermediate
from interpreter import Interpreter
from supervisor import Supervisor
import socket


host = socket.gethostbyname(socket.gethostname())

PORT_INTERMEDIATE = 5550
PORT_SUPERVISOR = 5560
PORT_INTERPRETER = 5570

IPC_INTERMEDIATE = "tcp://"+host+":"+str(PORT_INTERMEDIATE)
IPC_SUPERVISOR = "tcp://"+host+":"+str(PORT_SUPERVISOR)
IPC_INTERPRETER = "tcp://"+host+":"+str(PORT_INTERPRETER)


intermediate = Intermediate(IPC_INTERMEDIATE, IPC_SUPERVISOR, IPC_INTERPRETER)
supervisor = Supervisor(IPC_INTERMEDIATE, IPC_SUPERVISOR, IPC_INTERPRETER)

supervisor_process = Process(target = supervisor.run)
supervisor_process.start()

intermediate_process = Process(target = intermediate.run)
intermediate_process.start()