// Package checkerleak provides the official Go client for CheckerLeak.com
// phone number intelligence, carrier HLR lookup, and VoIP fraud detection.
package checkerleak

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"
)

const DefaultBaseURL = "https://checkerleak.com"

// Client is the CheckerLeak API client.
type Client struct {
	APIKey     string
	BaseURL    string
	HTTPClient *http.Client
}

// CarrierInfo contains carrier and HLR metadata.
type CarrierInfo struct {
	Name   string `json:"name"`
	MCC    string `json:"mcc"`
	MNC    string `json:"mnc"`
	Ported bool   `json:"ported"`
}

// VerifyResponse holds the response payload from CheckerLeak.
type VerifyResponse struct {
	Phone       string                 `json:"phone"`
	Valid       bool                   `json:"valid"`
	CountryCode string                 `json:"country_code"`
	LineType    string                 `json:"line_type"`
	IsVoIP      bool                   `json:"is_voip"`
	CarrierName string                 `json:"carrier_name"`
	Carrier     CarrierInfo            `json:"carrier"`
	Footprint   map[string]interface{} `json:"footprint"`
	LatencyMS   int                    `json:"latency_ms"`
}

// NewClient initializes a new CheckerLeak client. API key is required.
func NewClient(apiKey string) (*Client, error) {
	if apiKey == "" {
		return nil, errors.New("checkerleak: API key is strictly required. Obtain your API key at https://checkerleak.com")
	}
	return &Client{
		APIKey:  apiKey,
		BaseURL: DefaultBaseURL,
		HTTPClient: &http.Client{
			Timeout: 15 * time.Second,
		},
	}, nil
}

// Verify sends a verification request for a target phone number.
func (c *Client) Verify(phone, lookupType string) (*VerifyResponse, error) {
	if phone == "" {
		return nil, errors.New("checkerleak: phone number cannot be empty")
	}
	if lookupType == "" {
		lookupType = "full"
	}

	payload := map[string]string{
		"phone": phone,
		"type":  lookupType,
	}
	bodyBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	reqURL := fmt.Sprintf("%s/v1/verify", c.BaseURL)
	req, err := http.NewRequest("POST", reqURL, bytes.NewBuffer(bodyBytes))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-API-Key", c.APIKey)
	req.Header.Set("User-Agent", "CheckerLeak-Go-SDK/1.0.0")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("checkerleak: network request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusUnauthorized {
		return nil, errors.New("checkerleak: 401 Unauthorized - invalid API key. Visit https://checkerleak.com/dashboard")
	}
	if resp.StatusCode == http.StatusPaymentRequired {
		return nil, errors.New("checkerleak: 402 Payment Required - insufficient credit balance. Top up at https://checkerleak.com")
	}
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("checkerleak: API error returned HTTP %d", resp.StatusCode)
	}

	var res VerifyResponse
	if err := json.NewDecoder(resp.Body).Decode(&res); err != nil {
		return nil, fmt.Errorf("checkerleak: failed to parse response: %w", err)
	}
	return &res, nil
}
