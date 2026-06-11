import socket

host = input("Host: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 80))

request = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

client.send(request.encode())

response = client.recv(4096)

print(response.decode(errors="ignore"))

client.close()
