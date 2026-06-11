package main

/*
CLI Browser (Go) - HTTP Protocol ni tushunish uchun oddiy client.

Bu dastur browser qanday ishlashini ko'rsatadi:
1. TCP socket ochadi (net.Dial)
2. HTTP request yuboradi
3. Response ni to'liq o'qiydi (io.ReadAll)
4. Header va Body ni ajratadi

Ishlatish:
	go run main.go example.com
	go run main.go example.com/about
*/

import (
	"fmt"
	"net"
	"os"
	"regexp"
	"strings"
)

// parseURL URL ni host, path, port ga ajratadi
func parseURL(raw string) (host string, path string, port string) {
	// http:// yoki https:// ni olib tashlash
	raw = regexp.MustCompile(`^https?://`).ReplaceAllString(raw, "")

	port = "80"

	// Port ajratish
	if idx := strings.Index(raw, ":"); idx != -1 {
		hostPort := raw[:idx]
		rest := raw[idx+1:]

		if slashIdx := strings.Index(rest, "/"); slashIdx != -1 {
			port = rest[:slashIdx]
			path = rest[slashIdx:]
		} else {
			port = rest
		}
		host = hostPort
	} else {
		if slashIdx := strings.Index(raw, "/"); slashIdx != -1 {
			host = raw[:slashIdx]
			path = raw[slashIdx:]
		} else {
			host = raw
		}
	}

	if path == "" {
		path = "/"
	}

	return
}

// stripHTML HTML taglarni oddiy matnga aylantiradi
func stripHTML(html string) string {
	// <br>, <p>, <div> -> yangi qator
	re := regexp.MustCompile(`(?i)<br\s*/?>|</p>|</div>|</h[1-6]>`)
	result := re.ReplaceAllString(html, "\n")

	// Header taglari -> # matn
	hRe := regexp.MustCompile(`(?i)<h([1-6])>(.*?)</h\1>`)
	result = hRe.ReplaceAllString(result, "# $2")

	// Boshqa taglarni olib tashlash
	tagRe := regexp.MustCompile(`(?i)<[^>]+>`)
	result = tagRe.ReplaceAllString(result, "")

	// Bo'sh qatorlarni tozalash
	blankRe := regexp.MustCompile(`\n{3,}`)
	result = blankRe.ReplaceAllString(result, "\n\n")

	return strings.TrimSpace(result)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Ishlatish: go run main.go <host>")
		fmt.Println("Misol:     go run main.go example.com")
		fmt.Println("          go run main.go example.com/about")
		os.Exit(1)
	}

	raw := os.Args[1]
	host, path, port := parseURL(raw)

	fmt.Printf("%s:%s%s ga ulanmoqda...\n", host, port, path)

	// 1. TCP socket ochish
	conn, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		fmt.Printf("Xatolik %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	// 2. HTTP Request yasash
	request := fmt.Sprintf(
		"GET %s HTTP/1.1\r\n"+
			"Host: %s\r\n"+
			"User-Agent: CLI-Browser/1.0\r\n"+
			"Accept: text/html\r\n"+
			"Connection: close\r\n"+
			"\r\n",
		path, host,
	)

	// 3. Request yuborish
	_, err = conn.Write([]byte(request))
	if err != nil {
		fmt.Printf("Xato%v\n", err)
		os.Exit(1)
	}

	// 4. To'liq response o'qish
	buffer := make([]byte, 4096)
	var response strings.Builder

	for {
		n, err := conn.Read(buffer)
		if n > 0 {
			response.Write(buffer[:n])
		}
		if err != nil {
			break
		}
	}

	// 5. Header va Body ajratish
	resp := response.String()
	headers := ""
	body := ""

	if idx := strings.Index(resp, "\r\n\r\n"); idx != -1 {
		headers = resp[:idx]
		body = resp[idx+4:]
	} else {
		headers = resp
	}

	fmt.Printf("\n%s\n", strings.Repeat("=", 60))
	fmt.Println("HEADERS")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(headers)

	fmt.Printf("\n%s\n", strings.Repeat("=", 60))
	fmt.Println("BODY")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(stripHTML(body))
}
