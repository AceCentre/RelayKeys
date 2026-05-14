//go:build windows

package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/acecentre/relaykeys/internal/config"
	"github.com/acecentre/relaykeys/internal/rpc"
	"github.com/acecentre/relaykeys/internal/webui"
	"github.com/kardianos/service"
)

type program struct {
	cfg       *config.Config
	httpSrv   *http.Server
	rpcServer *rpc.Server
	uiServer  *webui.Server
	cancel    func()
}

func createService(cfg *config.Config, httpSrv *http.Server, rpcServer *rpc.Server, uiServer *webui.Server, cancel func()) (service.Service, error) {
	svcConfig := &service.Config{
		Name:        "RelayKeys",
		DisplayName: "RelayKeys Daemon",
		Description: "RelayKeys BLE HID daemon - Bluetooth keyboard/mouse relay",
	}

	p := &program{
		cfg:       cfg,
		httpSrv:   httpSrv,
		rpcServer: rpcServer,
		uiServer:  uiServer,
		cancel:    cancel,
	}

	s, err := service.New(p, svcConfig)
	if err != nil {
		return nil, err
	}
	return s, nil
}

func runService(s service.Service) error {
	err := s.Run()
	if err != nil {
		return err
	}
	return nil
}

func (p *program) Start(s service.Service) error {
	log.Println("[Service] Starting...")
	return nil
}

func (p *program) Stop(s service.Service) error {
	log.Println("[Service] Stopping...")
	if p.cancel != nil {
		p.cancel()
	}
	if p.httpSrv != nil {
		p.httpSrv.Close()
	}
	return nil
}

func handleServiceCommand(action string, cfg *config.Config) error {
	svcConfig := &service.Config{
		Name:        "RelayKeys",
		DisplayName: "RelayKeys Daemon",
		Description: "RelayKeys BLE HID daemon - Bluetooth keyboard/mouse relay",
	}

	p := &program{cfg: cfg}
	s, err := service.New(p, svcConfig)
	if err != nil {
		return fmt.Errorf("failed to create service: %w", err)
	}

	switch action {
	case "install":
		err = s.Install()
		if err != nil {
			return fmt.Errorf("failed to install service: %w", err)
		}
		log.Println("Service installed successfully")
	case "uninstall":
		err = s.Uninstall()
		if err != nil {
			return fmt.Errorf("failed to uninstall service: %w", err)
		}
		log.Println("Service uninstalled successfully")
	case "start":
		err = s.Start()
		if err != nil {
			return fmt.Errorf("failed to start service: %w", err)
		}
		log.Println("Service started successfully")
	case "stop":
		err = s.Stop()
		if err != nil {
			return fmt.Errorf("failed to stop service: %w", err)
		}
		log.Println("Service stopped successfully")
	default:
		return fmt.Errorf("unknown service action: %s (use: install, uninstall, start, stop)", action)
	}
	return nil
}
