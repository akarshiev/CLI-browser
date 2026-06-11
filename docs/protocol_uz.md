# Browser Qanday Ishlaydi — Amaliy Qo'llanma

> HTTP protokoli asoslarini tushunish: TCP socketlardan to'lab request/response sikllarigacha.

---

## 1. Protocol nima?

**Protocol** — ikki kompyuter o'rtasida muloqot qilishda rioya qilinadigan qoidalar to'plami. Insonlar bir tilda gaplashsa, kompyuterlar ham ma'lumot almashish uchun umumiy qoidalar kerak.

Tarmoqlarda protokollar qatlam (layer) shaklida ishlaydi:

```
┌─────────────────────────┐
│   Ilova qatlami         │  <- HTTP, FTP, SMTP, DNS
├─────────────────────────┤
│   Transport qatlami     │  <- TCP, UDP
├─────────────────────────┤
│   Internet qatlami      │  <- IP
├─────────────────────────┤
│   Tarmoq kirish qatlami │  <- Ethernet, Wi-Fi
└─────────────────────────┘
```

**HTTP (HyperText Transfer Protocol)** — Ilova qatlamida ishlaydi. U client (browser) qanday so'rov yuborishini va server qanday javob qaytarishini belgilaydi.

Asosiy tushuncha: **HTTP TCP ustida ishlaydi**. HTTP xabar yuborishdan oldin TCP ulanishi o'rnatilishi kerak.

---

## 2. TCP: Asos

**TCP (Transmission Control Protocol)** — ikki kompyuter orasida ishonchli, tartibli ma'lumot yetkazib berishni ta'minlaydi.

Browser veb-sahifani so'rashdan oldin:

1. **Domain nomini IP manzilga aylantiradi** (DNS orqali)
2. **TCP ulanishini ochadi** server bilan (3 bosqichli handshake)

![HTTP Request over tcp connections](https://miro.medium.com/v2/resize:fit:1400/1*0eJLdKsz58XoJsg-aSrvUg.png)

Buni terminalda `nc` (netcat) orqali ko'rishingiz mumkin:

```bash
$ nc example.com 80
```

Bu example.com ga 80-port orqali xom TCP ulanish ochadi. Keyin qo'lda HTTP so'rov yozishingiz mumkin:

```
GET / HTTP/1.1
Host: example.com
Connection: close

```

Oxirgi header'dan keyin Enterni 2 marta bosing. Server HTML kontent bilan javob qaytaradi!

---

## 3. HTTP Request (So'rov)

HTTP so'rov — qat'iy formatga ega matn xabar:

```
METHOD /yo'l HTTP/1.1
Header1: qiymat1
Header2: qiymat2

[ixtiyoriy body]
```

### Misol (`nc` orqali):

```bash
$ nc example.com 80
GET / HTTP/1.1
Host: example.com
Connection: close

```

### So'rov qismlari:

| Qism | Tavsif |
|------|--------|
| **Method** | Qanday amal bajariladi: `GET` (o'qish), `POST` (yaratish), `PUT` (yangilash), `DELETE` (o'chirish) |
| **Yo'l** | Qaysi resurs: `/`, `/about`, `/api/users` |
| **Versiya** | HTTP versiyasi: `HTTP/1.1` yoki `HTTP/2` |
| **Headerlar** | Meta-ma'lumot: `Host`, `User-Agent`, `Accept`, `Cookie` |
| **Body** | POST/PUT bilan yuboriladigan ma'lumot (GET uchun ixtiyoriy) |

### Umumiy Methodlar:

- **GET** — Resursni o'qish (eng ko'p ishlatiladi, URL ga kirganda)
- **POST** — Yangi resurs yaratish (forma yuborish, ma'lumot yuklash)
- **PUT** — Mavjud resursni yangilash
- **DELETE** — Resursni o'chirish
- **HEAD** — GET ga o'xshaydi, lekin faqat headerlarni qaytaradi

---

## 4. HTTP Response (Javob)

Server so'rovni olgandan keyin javob yuboradi:

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1256
Connection: close

<!DOCTYPE html>
<html>
  <body>Salom, Dunyo!</body>
</html>
```

### Javob qismlari:

| Qism | Tavsif |
|------|--------|
| **Status kodi** | So'rov natijasi: `200` (OK), `404` (Topilmadi), `500` (Server xatosi) |
| **Headerlar** | Javob haqida meta-ma'lumot: kontent turi, uzunlik, kesh qoidalari |
| **Body** | Haqiqiy kontent (HTML, JSON, rasmlar, va boshqalar) |

### Umumiy Status kodlari:

| Kod | Ma'nosi | Qachon |
|-----|---------|--------|
| `200` | OK | So'rov muvaffaqiyatli bajarildi |
| `301` | Doimiy ko'chirildi | URL yo'naltirildi |
| `304` | O'zgarmagan | Kesh versiyasi hali yaroqli |
| `400` | Noto'g'ri so'rov | Xato format |
| `403` | Taqiqlangan | Ruxsat yo'q |
| `404` | Topilmadi | Resurs mavjud emas |
| `500` | Server xatosi | Server ishlamay qoldi |

---

## 5. Response Body (Javob tarkibi)

**Body** — server qaytaradigan haqiqiy kontent. Headerlar va body orasida doimo bo'sh qator (`\r\n\r\n`) bo'ladi.

```
HTTP/1.1 200 OK
Content-Type: text/html
                          // Bu bo'sh qator headerlarni body'dan ajratadi
<html><body>Salom</body></html>
```

Body bo'lishi mumkin:
- **HTML** — veb-sahifalar (`Content-Type: text/html`)
- **JSON** — API ma'lumotlari (`Content-Type: application/json`)
- **Binary** — rasmlar, fayllar (`Content-Type: image/png`)
- **Oddiy matn** — sodd matn (`Content-Type: text/plain`)

---

## 6. HTTP ning Stateless (Holatsiz) Tabiati

**HTTP stateless** — har bir so'rov mustaqil. Server oldingi so'rovlarni eslab qolmaydi.

```
So'rov 1: GET /login     // Server javob berdi
So'rov 2: GET /dashboard // Server: "Siz kimsiz?"
```

Bu soddalik va masshtablilik uchun qilingan. Lekin muammo tug'diradi: foydalanuvchilar qanday kirib qoladi?

### Yechimlar:

#### Cookies (Kukilar)
**Cookie** — server sizning browseringizga saqlashini so'raydigan kichik ma'lumot. Keyingi so'rovlarda browser avtomatik cookie'ni qaytaradi.

```
# Server javobida cookie o'rnatadi:
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123; Path=/; HttpOnly

# Browser avtomatik yuboradi:
GET /dashboard HTTP/1.1
Cookie: session_id=abc123
```

Cookie'lar browserda saqlanadi va har bir so'rov bilan avtomatik yuboriladi.

#### Sessions (Sessiyalar)
**Session** — server tomonida saqlanadigan tushuncha. Server foydalanuvchi ma'lumotlarini xotirada/bazada saqlaydi va session ID (cookie'da saqlanadi) orqali topadi.

```
Foydalanuvchi kiradi -> Server session yaratadi (xotirada saqlaydi)
                    -> Server session_id cookie'sini browserga yuboradi
Browser cookie yuboradi -> Server session ma'lumotlarini topadi
                       -> Siz kimligingizni biladi!
```

Cheklov: server qayta ishga tushsa, barcha sessiyalar yo'qoladi (agar bazaga saqlanmasa).

#### JWT (JSON Web Tokens)
**JWT** — sessiyalarga stateless alternativ. Server ma'lumotni token'ning o'zida kodlaydi, serverda saqlamaydi.

```
JWT = Header.Payload.Signature

eyJhbGci... .eyJ1c2VyIjoiQWxpIn0 .signature
   header       payload (ma'lumot)      imzolangan
```

Server token'ni imzolaydi, lekin saqlamaydi. So'rov kelganda, server faqat imzoni tekshiradi. Bu yaxshiroq masshtablanadi, chunki server tomonida saqlash kerak emas.

> **Eslatma:** JWT ilg'or mavzu. Browser asoslarini tushunish uchun cookie'lar va sessiyalar asosiy tushunchalardir.

---

## 7. Bizning CLI Browser: Kod tahlili

### Python versiyasi (`python/cli_browser.py`)

```python
# 1-qadam: TCP socket ochish
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 80))

# 2-qadam: HTTP so'rov yasash (matn formatida!)
request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# 3-qadam: So'rovni yuborish
client.send(request.encode())

# 4-qadam: Javobni loop orqali to'liq o'qish
chunks = []
while True:
    data = client.recv(4096)
    if not data:
        break
    chunks.append(data)
response = b"".join(chunks)

# 5-qadam: Headerlarni body'dan ajratish
headers, body = response.split("\r\n\r\n", 1)
```

### Go versiyasi (`go/main.go`)

```go
// 1-qadam: TCP ulanish ochish
conn, err := net.Dial("tcp", host+":"+port)

// 2-qadam: HTTP so'rov yasash
request := fmt.Sprintf(
    "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n",
    path, host,
)

// 3-qadam: So'rovni yuborish
conn.Write([]byte(request))

// 4-qadam: To'liq javobni o'qish (loop orqali)
buffer := make([]byte, 4096)
var response strings.Builder
for {
    n, err := conn.Read(buffer)
    if n > 0 { response.Write(buffer[:n]) }
    if err != nil { break }
}

// 5-qadam: Headerlarni body'dan ajratish
idx := strings.Index(resp, "\r\n\r\n")
headers = resp[:idx]
body = resp[idx+4:]
```

### Asosiy kuzatishlar:

1. **HTTP oddiy matn** — uni `nc` da qo'lda yozishingiz mumkin
2. **TCP avval bo'lishi kerak** — TCP ulanishisiz HTTP bo'lmaydi
3. **`\r\n\r\n`** — headerlar va body orasidagi sirli ajratuvchi
4. **`recv()` bo'laklarni oladi** — to'liq javob olish uchun loop kerak
5. **`Connection: close`** — serverga javobdan keyin ulanishni yopishni aytadi

---

## Xulosa

```
Browser so'raydi:                    Server javob beradi:
                                
1. DNS izlash                        -> IP manzil
2. TCP ulanish (3 bosqichli)         -> Ulanish tayyor
3. HTTP so'rovni yuborish            -> So'rovni qayta ishlash
4. HTTP javobni qabul qilish         -> Javobni yuborish
5. Headerlar + body ni parse qilish  -> Kontentni ko'rsatish
```

Butun internet — har bir veb-sayt, har bir API, har bir ilova — TCP ustidagi oddiy so'rov/javob sikli asosida qurilgan.

---

*Bog'lanish: [Ingliz versiyasi](protocol_en.md)*
