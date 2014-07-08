import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.6', 12002)

sock.connect(server_address)
print 'Opening connection'
f = open('IBEOReading.txt','w')
dat = ''
dat_size = 1024*1024*3
try:
    while dat_size > 0:
        inp = sock.recv(dat_size).encode('hex')
        dat_size -= len(inp)
        dat += inp
    
finally:
    print 'closing socket'
    sock.close()
    print 'writing to file data with ',len(dat),' bytes'
    f.write(dat)
    f.close()
