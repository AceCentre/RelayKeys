package capture

import (
	"log"
	"strings"
	"sync"
)

type Event struct {
	Type      string   `json:"type"`
	Key       string   `json:"key,omitempty"`
	Modifiers []string `json:"modifiers,omitempty"`
	Down      bool     `json:"down"`
	DX        int      `json:"dx,omitempty"`
	DY        int      `json:"dy,omitempty"`
	WheelY    int      `json:"wheelY,omitempty"`
	WheelX    int      `json:"wheelX,omitempty"`
	Button    string   `json:"button,omitempty"`
}

type Handler func(Event)

type Capture struct {
	mu             sync.Mutex
	active         bool
	kbEnabled      bool
	msEnabled      bool
	handler        Handler
	stop           chan struct{}
}

func New(h Handler) *Capture {
	return &Capture{
		handler:         h,
		kbEnabled:       true,
		stop:            make(chan struct{}),
	}
}

func (c *Capture) Start() error {
	c.mu.Lock()
	if c.active {
		c.mu.Unlock()
		return nil
	}
	c.active = true
	c.mu.Unlock()

	log.Println("[Capture] Starting platform input capture...")
	return c.startPlatform()
}

func (c *Capture) Stop() {
	c.mu.Lock()
	if !c.active {
		c.mu.Unlock()
		return
	}
	c.active = false
	c.mu.Unlock()

	close(c.stop)
	c.stop = make(chan struct{})
	log.Println("[Capture] Stopped")
}

func (c *Capture) IsActive() bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.active
}

func (c *Capture) SetKeyboardEnabled(v bool) {
	c.mu.Lock()
	c.kbEnabled = v
	c.mu.Unlock()
}

func (c *Capture) SetMouseEnabled(v bool) {
	c.mu.Lock()
	c.msEnabled = v
	c.mu.Unlock()
}

func (c *Capture) emit(e Event) {
	switch e.Type {
	case "keyevent":
		if !c.isKBEnabled() {
			return
		}
	case "mousemove", "mousebutton", "mousescroll":
		if !c.isMSEnabled() {
			return
		}
	}
	c.handler(e)
}

func (c *Capture) isKBEnabled() bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.kbEnabled
}

func (c *Capture) isMSEnabled() bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.msEnabled
}

var ModifierMap = map[string]bool{
	"LCTRL": true, "LSHIFT": true, "LALT": true, "LMETA": true,
	"RCTRL": true, "RSHIFT": true, "RALT": true, "RMETA": true,
}

func IsModifier(key string) bool {
	return ModifierMap[strings.ToUpper(key)]
}
