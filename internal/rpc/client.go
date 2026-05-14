package rpc

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync/atomic"
)

type Client struct {
	url    string
	id     atomic.Uint64
	header http.Header
}

func NewClient(url, username, password string) *Client {
	c := &Client{
		url:    url,
		header: http.Header{"Content-Type": []string{"application/json"}},
	}
	if username != "" || password != "" {
		c.header.Set("Authorization", basicAuth(username, password))
	}
	return c
}

func (c *Client) Call(method string, args ...interface{}) (string, error) {
	id := c.id.Add(1)

	params := make([]interface{}, len(args))
	for i, a := range args {
		params[i] = a
	}

	reqBody := map[string]interface{}{
		"jsonrpc": "2.0",
		"method":  method,
		"params":  []interface{}{params},
		"id":      id,
	}

	data, err := json.Marshal(reqBody)
	if err != nil {
		return "", fmt.Errorf("marshal request: %w", err)
	}

	req, err := http.NewRequest(http.MethodPost, c.url, bytes.NewReader(data))
	if err != nil {
		return "", fmt.Errorf("create request: %w", err)
	}
	for k, v := range c.header {
		req.Header[k] = v
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("rpc call failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusForbidden {
		return "", fmt.Errorf("authentication failed")
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("read response: %w", err)
	}

	var rpcResp struct {
		Result interface{}   `json:"result"`
		Error  *jsonRPCError `json:"error"`
	}
	if err := json.Unmarshal(body, &rpcResp); err != nil {
		return "", fmt.Errorf("parse response: %w (body: %s)", err, string(body))
	}

	if rpcResp.Error != nil {
		return "", fmt.Errorf("rpc error %d: %s", rpcResp.Error.Code, rpcResp.Error.Message)
	}

	switch v := rpcResp.Result.(type) {
	case string:
		return v, nil
	case []interface{}:
		parts := make([]string, len(v))
		for i, item := range v {
			parts[i] = fmt.Sprintf("%v", item)
		}
		return fmt.Sprintf("[%s]", joinStrings(parts, ",")), nil
	default:
		return fmt.Sprintf("%v", rpcResp.Result), nil
	}
}

func basicAuth(username, password string) string {
	creds := username + ":" + password
	return "Basic " + base64.StdEncoding.EncodeToString([]byte(creds))
}

func joinStrings(parts []string, sep string) string {
	result := ""
	for i, p := range parts {
		if i > 0 {
			result += sep
		}
		result += p
	}
	return result
}
