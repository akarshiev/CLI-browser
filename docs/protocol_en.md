# How a Browser Works — A Practical Guide

> Understanding the fundamentals of HTTP communication, from TCP sockets to request/response cycles.

---

## 1. What is a Protocol?

A **protocol** is a set of rules that two computers agree to follow when communicating. Just like humans need a shared language to talk, computers need shared rules to exchange data.

In networking, the most important protocols are layered:

```
┌─────────────────────────┐
│   Application Layer     │  ← HTTP, FTP, SMTP, DNS
├─────────────────────────┤
│   Transport Layer       │  ← TCP, UDP
├─────────────────────────┤
│   Internet Layer        │  ← IP
├─────────────────────────┤
│   Network Access Layer  │  ← Ethernet, Wi-Fi
└─────────────────────────┘
```

**HTTP (HyperText Transfer Protocol)** operates at the Application layer. It defines how a client (browser) sends requests and how a server sends responses back.

The key insight: **HTTP runs on top of TCP**. Before any HTTP message is sent, a TCP connection must be established first.

---

## 2. TCP: The Foundation

**TCP (Transmission Control Protocol)** provides reliable, ordered delivery of data between two computers.

Before a browser can request a webpage, it must:

1. **Resolve** the domain name to an IP address (via DNS)
2. **Open a TCP connection** to the server (3-way handshake)

```
Client                          Server
  │                               │
  │──── SYN (1) ────────────────>│
  │<─── SYN-ACK (2) ────────────│
  │──── ACK (3) ────────────────>│
  │                               │
  │    TCP Connection Ready!      │
```

You can see this yourself using `nc` (netcat) in a terminal:

```bash
$ nc example.com 80
```

This opens a raw TCP connection to example.com on port 80. You can then manually type an HTTP request:

```
GET / HTTP/1.1
Host: example.com
Connection: close

```

Press Enter twice after the last header. The server will respond with HTML content!

---

## 3. HTTP Request

An HTTP request is a text message that follows a strict format:

```
METHOD /path HTTP/1.1
Header1: value1
Header2: value2

[optional body]
```

### Example (using `nc`):

```bash
$ nc example.com 80
GET / HTTP/1.1
Host: example.com
Connection: close

```

### Parts of a Request:

| Part | Description |
|------|-------------|
| **Method** | What action to perform: `GET` (read), `POST` (create), `PUT` (update), `DELETE` (remove) |
| **Path** | Which resource: `/`, `/about`, `/api/users` |
| **Version** | HTTP version: `HTTP/1.1` or `HTTP/2` |
| **Headers** | Metadata: `Host`, `User-Agent`, `Accept`, `Cookie` |
| **Body** | Data sent with POST/PUT requests (optional for GET) |

### Common Methods:

- **GET** — Read a resource (most common, used when you visit a URL)
- **POST** — Create a new resource (submit a form, upload data)
- **PUT** — Update an existing resource
- **DELETE** — Remove a resource
- **HEAD** — Like GET but only returns headers, no body

---

## 4. HTTP Response

After receiving a request, the server sends back a response:

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1256
Connection: close

<!DOCTYPE html>
<html>
  <body>Hello, World!</body>
</html>
```

### Parts of a Response:

| Part | Description |
|------|-------------|
| **Status Code** | Result of the request: `200` (OK), `404` (Not Found), `500` (Server Error) |
| **Headers** | Metadata about the response: content type, length, caching rules |
| **Body** | The actual content (HTML, JSON, images, etc.) |

### Common Status Codes:

| Code | Meaning | When |
|------|---------|------|
| `200` | OK | Request succeeded |
| `301` | Moved Permanently | URL redirected |
| `304` | Not Modified | Cached version is still valid |
| `400` | Bad Request | Malformed request |
| `403` | Forbidden | No permission |
| `404` | Not Found | Resource doesn't exist |
| `500` | Internal Server Error | Server crashed |

---

## 5. The Response Body

The **body** is the actual content the server sends back. Between headers and body, there's always a blank line (`\r\n\r\n`).

```
HTTP/1.1 200 OK
Content-Type: text/html
                          ← This blank line separates headers from body
<html><body>Hello</body></html>
```

The body can be:
- **HTML** — web pages (`Content-Type: text/html`)
- **JSON** — API data (`Content-Type: application/json`)
- **Binary** — images, files (`Content-Type: image/png`)
- **Plain text** — simple text (`Content-Type: text/plain`)

---

## 6. Stateless Nature of HTTP

**HTTP is stateless** — each request is independent. The server does NOT remember previous requests.

```
Request 1: GET /login     → Server responds ✓
Request 2: GET /dashboard → Server: "Who are you?" ❌
```

This is by design for simplicity and scalability. But it creates a problem: how do you keep users logged in?

### Solutions:

#### Cookies
A **cookie** is a small piece of data the server asks your browser to store. On subsequent requests, the browser automatically sends the cookie back.

```
# Server response sets a cookie:
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123; Path=/; HttpOnly

# Browser automatically sends it back:
GET /dashboard HTTP/1.1
Cookie: session_id=abc123
```

Cookies are stored by the browser and sent with every request to that domain.

#### Sessions
A **session** is a server-side concept. The server stores user data in memory/database, and uses a session ID (stored in a cookie) to look it up.

```
User logs in → Server creates session (stores in memory)
             → Server sends session_id cookie to browser
Browser sends cookie → Server looks up session data
                     → Knows who you are!
```

The limitation: if the server restarts, all sessions are lost (unless persisted to a database).

#### JWT (JSON Web Tokens)
**JWT** is a stateless alternative to sessions. Instead of storing data on the server, the data is encoded in the token itself.

```
JWT = Header.Payload.Signature

eyJhbGci... .eyJ1c2VyIjoiQWxpIn0 .signature
   header       payload (data)      signed
```

The server signs the token but doesn't store it. When a request comes in, the server just verifies the signature. This scales better because no server-side storage is needed.

> **Note:** JWT is advanced territory. For understanding browser fundamentals, cookies and sessions are the key concepts.

---

## 7. Our CLI Browser: Code Walkthrough

### Python Version (`python/cli_browser.py`)

```python
# Step 1: Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 80))

# Step 2: Build HTTP request (text format!)
request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# Step 3: Send request
client.send(request.encode())

# Step 4: Read response in a loop
chunks = []
while True:
    data = client.recv(4096)
    if not data:
        break
    chunks.append(data)
response = b"".join(chunks)

# Step 5: Split headers from body
headers, body = response.split("\r\n\r\n", 1)
```

### Go Version (`go/main.go`)

```go
// Step 1: Open TCP connection
conn, err := net.Dial("tcp", host+":"+port)

// Step 2: Build HTTP request
request := fmt.Sprintf(
    "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n",
    path, host,
)

// Step 3: Send request
conn.Write([]byte(request))

// Step 4: Read full response (loop)
buffer := make([]byte, 4096)
var response strings.Builder
for {
    n, err := conn.Read(buffer)
    if n > 0 { response.Write(buffer[:n]) }
    if err != nil { break }
}

// Step 5: Split headers from body
idx := strings.Index(resp, "\r\n\r\n")
headers = resp[:idx]
body = resp[idx+4:]
```

### Key Observations:

1. **HTTP is just text** — you can type it by hand in `nc`
2. **TCP must come first** — no HTTP without a TCP connection
3. **`\r\n\r\n`** — the magic separator between headers and body
4. **`recv()` reads chunks** — you must loop to get the full response
5. **`Connection: close`** — tells the server to close the connection after responding

---

## Summary

```
Browser asks:                    Server answers:
                                
1. DNS lookup                    → IP address
2. TCP connect (3-way handshake) → Connection ready
3. Send HTTP request             → Process request
4. Receive HTTP response         → Send response
5. Parse headers + body          → Display content
```

The entire web — every website, every API, every app — is built on this simple request/response cycle over TCP.

---

*See also: [Uzbek version](protocol_uz.md)*
