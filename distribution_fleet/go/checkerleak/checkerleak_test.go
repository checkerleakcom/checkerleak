package checkerleak

import (
	"testing"
)

func TestNewClientRequiresAPIKey(t *testing.T) {
	_, err := NewClient("")
	if err == nil {
		t.Fatal("expected error when API key is empty, got nil")
	}
}

func TestNewClientSuccess(t *testing.T) {
	client, err := NewClient("clk_live_mock_key")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if client.APIKey != "clk_live_mock_key" {
		t.Fatalf("expected api key clk_live_mock_key, got %s", client.APIKey)
	}
}
