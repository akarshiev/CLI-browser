import socket

host = input("Host: ")
port = int(input("Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"{host}:{port} ga ulanmoqda...")
client.connect((host, port))

print("Ulandi!")

client.close()
