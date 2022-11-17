package main

import (
	"anaskhan96/soup"
	"fmt"
	"sync"
)

// const Header maps User-Agent to a string
func scrape(url string, wg *sync.Waitgroup, ch chan str) []string {
	defer wg.Done()
	soup.Header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
	chrome, err := soup.Get("https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome")
	if err != nil {
		fmt.Println(err)
	}
	ff, err := soup.Get("https://www.whatismybrowser.com/guides/the-latest-user-agent/firefox")
	if err != nil {
		fmt.Println(err)
	}
	safari, err := soup.Get("https://www.whatismybrowser.com/guides/the-latest-user-agent/safari")
	if err != nil {
		fmt.Println(err)
	}
	opera, err := soup.Get("https://www.whatismybrowser.com/guides/the-latest-user-agent/opera")
	if err != nil {
		fmt.Println(err)
	}
	edge, err := soup.Get("https://www.whatismybrowser.com/guides/the-latest-user-agent/edge")
	if err != nil {
		fmt.Println(err)
	}
	doc := soup.HTMLParse(chrome)
	doc1 := soup.HTMLParse(ff)
	doc2 := soup.HTMLParse(safari)
	doc3 := soup.HTMLParse(opera)
	doc4 := soup.HTMLParse(edge)
	var uas []string
	// we can parse them all in one go, they will be written to a single file anyway
	for _, link := range soup.FindAll("span", "class", "code") {
		ch <- link.Text()
		uas = append(uas, link.Text())
	}
	close(ch)
	return uas
}
