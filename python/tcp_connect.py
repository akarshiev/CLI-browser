import socket

host = input("Host: ")
port = int(input("Port (default 80): ") or "80")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"{host}:{port} ga ulanmoqda...")
client.connect((host, port))

print("Ulandi! TCP ulanish muvaffaqiyatli ochildi.")
print("(Bu bosqichda hali HTTP so'rov yuborilmagan.)")

client.close()
