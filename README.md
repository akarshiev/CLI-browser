# CLI Browser — Browser Qanday Ishlaydi?

> Python va Go orqali yozilgan oddiy CLI browser. HTTP protokolini tushunish uchun amaliy qo'llanma.

## Nima uchun?

Browser — bu murakkab dastur. Lekin uning asosi juda oddiy:

```
TCP ulanish -> HTTP so'rov yuborish -> Javobni o'qish -> Ko'rsatish
```

Bu loyiha shu jarayonni qo'lda amalga oshiradi.

## Loyiha tuzilishi

```
.
├── python/
│   ├── tcp_connect.py      # 1-qadam: TCP ulanish
│   ├── get_method.py       # 2-qadam: HTTP GET so'rov
│   ├── browser_full.py     # 3-qadam: To'liq javob o'qish
│   └── cli_browser.py      # 4-qadam: To'liq CLI browser
├── go/
│   └── main.go             # Go versiyasi (barcha qadamlar bitta faylda)
├── docs/
│   ├── protocol_en.md      # HTTP protokoli haqida (Inglizcha)
│   └── protocol_uz.md      # HTTP protokoli haqida (O'zbekcha)
└── README.md               # Siz shu yerdasiz
```

## Ishlatish

### Python

```bash
# 1-qadam: TCP ulanish
python python/tcp_connect.py

# 2-qadam: HTTP GET so'rov
python python/get_method.py

# 3-qadam: To'liq javob
python python/browser_full.py

# 4-qadam: CLI browser
python python/cli_browser.py example.com
python python/cli_browser.py example.com/about
```

### Go

```bash
go run go/main.go example.com
go run go/main.go example.com/about
```

## Terminalda sinab ko'ring

Buni o'zingiz sinab ko'rishingiz mumkin:

```bash
# 1. TCP ulanish oching
$ nc example.com 80

# 2. HTTP so'rovni qo'lda yozing
GET / HTTP/1.1
Host: example.com
Connection: close

# 3. Enterni 2 marta bosing
# 4. Server javobini ko'rasiz!
```

## Qadamlar (bosqichma-bosqich)

### Commit 1: TCP ulanish
```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
```

Browser birinchi navbatda serverga TCP ulanish ochadi.

### Commit 2: HTTP GET so'rov
```python
request = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
client.send(request.encode())
```

HTTP so'rov matn formatida — siz uni qo'lda yozishingiz mumkin.

### Commit 3: To'liq javob o'qish
```python
chunks = []
while True:
    data = client.recv(4096)
    if not data:
        break
    chunks.append(data)
response = b"".join(chunks)
```

`recv()` faqat bitta paket oladi, shuning uchun loop kerak.

### Commit 4: Header va Body ajratish
```python
headers, body = response.split("\r\n\r\n", 1)
```

`\r\n\r\n` — headerlar va body orasidagi ajratuvchi.

## Asosiy tushunchalar

### Protocol nima?
Ikki kompyuter orasidagi muloqot qoidalari.

### HTTP Stateless
Har bir so'rov mustaqil — server oldingi so'rovlarni eslab qolmaydi.

### Cookie va Session
Server foydalanuvchilarni eslab qolish uchun cookie va session ishlatadi.

### JWT
Server tomonida ma'lumot saqlamasdan autentifikatsiya qilish usuli.

## Documentation

- [HTTP Protocol (EN)](docs/protocol_en.md)
- [HTTP Protocol (UZ)](docs/protocol_uz.md)

---

*Bizning CLI browser — bu oddiy, lekin asosiy tushunchalarni tushunishga yordam beradi.*
