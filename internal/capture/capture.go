package capture

import (
	"strings"
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

var ModifierMap = map[string]bool{
	"LCTRL": true, "LSHIFT": true, "LALT": true, "LMETA": true,
	"RCTRL": true, "RSHIFT": true, "RALT": true, "RMETA": true,
}

func IsModifier(key string) bool {
	return ModifierMap[strings.ToUpper(key)]
}
