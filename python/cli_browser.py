#!/usr/bin/env python3
"""
CLI Browser - HTTP Protocol ni tushunish uchun oddiy client.

Bu dastur browser qanday ishlashini ko'rsatadi:
1. TCP socket ochadi
2. HTTP request yuboradi
3. Response ni to'liq o'qiydi
4. Header va Body ni ajratadi
"""

import socket
import sys
import re


def parse_url(url: str) -> tuple[str, str, int]:
    """
    URL ni parse qiladi.
    Misol: example.com/about -> (example.com, /about, 80)
    """
    # http:// yoki https:// ni olib tashlash
    url = re.sub(r'^https?://', '', url)

    # Port ajratish (example.com:8080)
    port = 80
    if ':' in url:
        host_port, path = url.split('/', 1) if '/' in url else (url, '')
        host, port_str = host_port.rsplit(':', 1)
        port = int(port_str)
    else:
        host = url.split('/')[0]
        path = url[len(host):]

    if not path:
        path = '/'

    return host, path, port


def fetch(host: str, path: str, port: int = 80) -> tuple[str, str]:
    """
    HTTP GET request yuboradi va (headers, body) qaytaradi.
    """
    # 1. TCP socket ochish
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)
    client.connect((host, port))

    # 2. HTTP Request yasash
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: CLI-Browser/1.0\r\n"
        "Accept: text/html\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    # 3. Request yuborish
    client.send(request.encode())

    # 4. To'liq response o'qish
    chunks = []
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            chunks.append(data)
        except socket.timeout:
            break

    client.close()
    response = b"".join(chunks).decode(errors="ignore")

    # 5. Header va Body ajratish
    if "\r\n\r\n" in response:
        headers, body = response.split("\r\n\r\n", 1)
    else:
        headers = response
        body = ""

    return headers, body


def strip_html(html: str) -> str:
    """HTML taglarni oddiy matnga aylantiradi."""
    # <br>, <p>, <div> -> yangi qator
    text = re.sub(r'<br\s*/?>|</p>|</div>|</h[1-6]>', '\n', html)
    # Header taglari -> # matn
    text = re.sub(r'<h([1-6])>(.*?)</h\1>', r'# \2', text)
    # Boshqa taglarni olib tashlash
    text = re.sub(r'<[^>]+>', '', text)
    # Bo'sh qatorlarni tozalash
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def main():
    if len(sys.argv) < 2:
        print("Ishlatish: python cli_browser.py <host>")
        print("Misol:     python cli_browser.py example.com")
        print("          python cli_browser.py example.com/about")
        sys.exit(1)

    url = sys.argv[1]
    host, path, port = parse_url(url)

    print(f"{host}:{port}{path} ga ulanmoqda...")

    try:
        headers, body = fetch(host, path, port)
    except Exception as e:
        print(f"Xatol {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("HEADERS")
    print('='*60)
    print(headers)

    print(f"\n{'='*60}")
    print("BODY")
    print('='*60)
    print(strip_html(body))


if __name__ == "__main__":
    main()
