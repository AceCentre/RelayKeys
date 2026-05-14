package webui

import (
	"embed"
)

//go:embed ui/*
var uiFS embed.FS
