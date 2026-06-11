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

# To'liq response ni o'qish - recv() faqat bitta paket oladi,
# shuning uchun loop orqali hamma ma'lumotni olamiz
chunks = []
while True:
    data = client.recv(4096)
    if not data:
        break
    chunks.append(data)

response = b"".join(chunks)
print(response.decode(errors="ignore"))

client.close()
