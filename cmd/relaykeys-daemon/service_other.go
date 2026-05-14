//go:build !windows

package main

import (
	"fmt"
	"net/http"

	"github.com/acecentre/relaykeys/internal/config"
	"github.com/acecentre/relaykeys/internal/rpc"
	"github.com/acecentre/relaykeys/internal/webui"
)

func createService(cfg *config.Config, httpSrv *http.Server, rpcServer *rpc.Server, uiServer *webui.Server, cancel func()) (interface{}, error) {
	return nil, fmt.Errorf("service not supported on this platform")
}

func runService(svc interface{}) error {
	return fmt.Errorf("service not supported on this platform")
}

func handleServiceCommand(action string, cfg *config.Config) error {
	return fmt.Errorf("service commands not supported on this platform")
}
