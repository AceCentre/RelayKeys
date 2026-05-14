package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"syscall"
	"time"

	"github.com/acecentre/relaykeys/internal/blehid"
	"github.com/acecentre/relaykeys/internal/config"
	"github.com/acecentre/relaykeys/internal/macro"
	"github.com/acecentre/relaykeys/internal/rpc"
	"github.com/acecentre/relaykeys/internal/serial"
	"github.com/acecentre/relaykeys/internal/webui"
)

var version = "dev"

func main() {
	cfgPath := flag.String("config", "", "Path to config file")
	devFlag := flag.String("dev", "", "Serial device path (e.g. COM3)")
	baudFlag := flag.Int("baud", 0, "Baud rate")
	debugFlag := flag.Bool("debug", false, "Enable debug logging")
	noserialFlag := flag.Bool("noserial", false, "Run without serial hardware")
	listPortsFlag := flag.Bool("list-ports", false, "List available serial ports and exit")
	serviceFlag := flag.String("service", "", "Windows service: install, uninstall, start, stop")
	showVersion := flag.Bool("version", false, "Show version")
	flag.Parse()

	if *showVersion {
		fmt.Printf("relaykeys-daemon %s\n", version)
		os.Exit(0)
	}

	cfg, err := config.Load(*cfgPath)
	if err != nil {
		log.Fatalf("Config error: %v", err)
	}

	if *debugFlag {
		cfg.Debug = true
	}
	if *noserialFlag {
		cfg.NoSerial = true
	}
	if *devFlag != "" {
		cfg.Dev = *devFlag
	}
	if *baudFlag != 0 {
		cfg.Baud = *baudFlag
	}

	if *listPortsFlag {
		ports, err := serial.ListPorts()
		if err != nil {
			log.Fatalf("Error listing ports: %v", err)
		}
		if len(ports) == 0 {
			fmt.Println("No serial ports found.")
		}
		for _, p := range ports {
			fmt.Println(p)
		}
		os.Exit(0)
	}

	if *serviceFlag != "" {
		if err := handleServiceCommand(*serviceFlag, cfg); err != nil {
			log.Fatalf("Service error: %v", err)
		}
		os.Exit(0)
	}

	if err := runDaemon(cfg); err != nil {
		log.Fatalf("Daemon error: %v", err)
	}
}

func runDaemon(cfg *config.Config) error {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	rpcServer := rpc.NewServerWithConfig(nil, cfg.Username, cfg.Password)

	exePath, _ := os.Executable()
	exeDir := filepath.Dir(exePath)
	macroDir := filepath.Join(exeDir, "macros")
	if _, err := os.Stat(macroDir); os.IsNotExist(err) {
		macroDir = "macros"
	}
	macros := macro.NewManager(macroDir)

	uiServer := webui.New(nil, func(cmd string) string {
		return rpcServer.ProcessBleCmd(cmd)
	})
	uiServer.SetMacros(macros)

	addr := fmt.Sprintf("%s:%d", cfg.Host, cfg.Port)

	mux := http.NewServeMux()
	mux.HandleFunc("/", rpcServer.HandleRPC)
	mux.HandleFunc("/ui/", uiServer.HandleUI)
	mux.HandleFunc("/ws", uiServer.HandleWS)

	httpServer := &http.Server{Addr: addr, Handler: mux}

	go func() {
		log.Printf("HTTP server starting on %s", addr)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Printf("HTTP server error: %v", err)
		}
	}()

	log.Printf("RelayKeys daemon %s started (pid=%d)", version, os.Getpid())
	if cfg.Debug {
		log.Printf("Config: %+v", cfg)
	}

	if !cfg.NoSerial {
		go connectSerial(ctx, cfg, rpcServer, uiServer)
	} else {
		log.Println("Running in no-serial mode")
	}

	if runtime.GOOS == "windows" {
		svc, err := createService(cfg, httpServer, rpcServer, uiServer, cancel)
		if err == nil {
			log.Println("Running as Windows service")
			if err := runService(svc); err != nil {
				return err
			}
			return nil
		}
	}

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	select {
	case sig := <-sigCh:
		log.Printf("Received signal: %v", sig)
	case <-ctx.Done():
	}

	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer shutdownCancel()
	httpServer.Shutdown(shutdownCtx)

	log.Println("Daemon stopped")
	return nil
}

func connectSerial(ctx context.Context, cfg *config.Config, rpcServer *rpc.Server, uiServer *webui.Server) {
	for {
		select {
		case <-ctx.Done():
			return
		default:
		}

		hwPort, err := serial.Open(cfg)
		if err != nil {
			log.Printf("Serial open failed: %v", err)
			log.Println("Retrying serial connection in 5 seconds...")
			select {
			case <-ctx.Done():
				return
			case <-time.After(5 * time.Second):
				continue
			}
		}

		if err := hwPort.Init(); err != nil {
			log.Printf("Serial init warning: %v", err)
		}
		if err := blehid.InitSerial(hwPort); err != nil {
			log.Printf("BLE HID init warning: %v", err)
		}

		log.Println("Serial device connected")
		rpcServer.SetPort(hwPort)
		uiServer.SetPort(hwPort, func(cmd string) string {
			return rpcServer.ProcessBleCmd(cmd)
		})
		uiServer.RefreshDevices()

		<-ctx.Done()
		hwPort.Close()
		return
	}
}
