package main

import (
	"github.com/atotto/clipboard"
)

func readClipboard() (string, error) {
	return clipboard.ReadAll()
}
