#!/usr/bin/python

from struct import *


# https://reference.opcfoundation.org/Core/Part6/v105/docs/7.1.2


def str_to_bytes(s):
    return bytes(s, 'utf-8')

# message header
message_type = str_to_bytes("HEL")
reserved = str_to_bytes("F")

# message body
protocol_version = 0
receive_buffer_size = 8192
send_buffer_size = 8192
max_message_size = 0
max_chunk_count = 0
#endpoint_url = str_to_bytes("X" * 4097) # one character too long
endpoint_url = str_to_bytes("opc.tcp://nmap.org:1337")
#endpoint_url = str_to_bytes("opc.tcp://echo.koti.kontu:53530")


message_size = 5 * 4 + len(endpoint_url) + 8 + 4 # 5 * 4 for the integers, len(endpoint_url) for the string, 8 for the header

hellomessage = pack(f"3ssIIIIIII{len(endpoint_url)}s", 
                    message_type, 
                    reserved, 
                    message_size, 
                    protocol_version,
                    receive_buffer_size, 
                    send_buffer_size, 
                    max_message_size, 
                    max_chunk_count,
                    len(endpoint_url),
                    endpoint_url)



import socket

HOST = "172.16.1.8"
PORT = 53530

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(hellomessage)
    print(f"Sent {hellomessage!r}")
    data = s.recv(1024)

print(f"Received {data!r}")