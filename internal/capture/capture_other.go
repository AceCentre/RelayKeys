//go:build !darwin && !windows

package capture

import (
	"fmt"
	"log"
)

func (c *Capture) startPlatform() error {
	log.Println("[Capture] Platform input capture not yet implemented for this OS")
	log.Println("[Capture] Use relaykeys-cli for keyboard/mouse commands instead")
	c.mu.Lock()
	c.active = false
	c.mu.Unlock()
	return fmt.Errorf("capture not implemented on this platform")
}
