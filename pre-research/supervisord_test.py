import xmlrpclib
server = xmlrpclib.Server('http://user:123@127.0.0.1:3030/RPC2')

methods = server.system.listMethods()
print methods
print server.supervisor.getState()
