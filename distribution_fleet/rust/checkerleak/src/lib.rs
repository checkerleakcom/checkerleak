//! # CheckerLeak Rust SDK
//!
//! Official Rust client for [CheckerLeak.com](https://checkerleak.com) — All-in-one phone intelligence,
//! carrier HLR lookup, VoIP fraud detection, and 102+ platform footprint checks.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use thiserror::Error;

const DEFAULT_BASE_URL: &str = "https://checkerleak.com";

#[derive(Error, Debug)]
pub enum CheckerLeakError {
    #[error("API Key is required. Obtain yours at https://checkerleak.com")]
    MissingApiKey,
    #[error("401 Unauthorized: Invalid API Key. Manage keys at https://checkerleak.com/dashboard")]
    Unauthorized,
    #[error("402 Payment Required: Credit balance depleted. Top up at https://checkerleak.com")]
    PaymentRequired,
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),
    #[error("API returned error code {0}: {1}")]
    ApiError(u16, String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CarrierDetails {
    pub name: Option<String>,
    pub mcc: Option<String>,
    pub mnc: Option<String>,
    pub ported: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerifyResponse {
    pub phone: String,
    pub valid: Option<bool>,
    pub country_code: Option<String>,
    pub line_type: Option<String>,
    pub is_voip: Option<bool>,
    pub carrier_name: Option<String>,
    pub carrier: Option<CarrierDetails>,
    pub footprint: Option<HashMap<String, serde_json::Value>>,
    pub latency_ms: Option<u64>,
}

#[derive(Clone)]
pub struct Client {
    api_key: String,
    base_url: String,
    http: reqwest::blocking::Client,
}

impl Client {
    /// Create a new CheckerLeak API client. API key is required.
    pub fn new(api_key: impl Into<String>) -> Result<Self, CheckerLeakError> {
        let key = api_key.into();
        if key.trim().is_empty() {
            return Err(CheckerLeakError::MissingApiKey);
        }

        let http = reqwest::blocking::Client::builder()
            .timeout(std::time::Duration::from_secs(15))
            .build()?;

        Ok(Self {
            api_key: key,
            base_url: DEFAULT_BASE_URL.to_string(),
            http,
        })
    }

    /// Verify an international phone number.
    pub fn verify(&self, phone: &str, lookup_type: Option<&str>) -> Result<VerifyResponse, CheckerLeakError> {
        let url = format!("{}/v1/verify", self.base_url);
        let t = lookup_type.unwrap_or("full");

        let body = serde_json::json!({
            "phone": phone,
            "type": t
        });

        let resp = self
            .http
            .post(&url)
            .header("X-API-Key", &self.api_key)
            .header("User-Agent", "CheckerLeak-Rust-SDK/0.1.0")
            .json(&body)
            .send()?;

        let status = resp.status();
        if status == reqwest::StatusCode::UNAUTHORIZED {
            return Err(CheckerLeakError::Unauthorized);
        }
        if status == reqwest::StatusCode::PAYMENT_REQUIRED {
            return Err(CheckerLeakError::PaymentRequired);
        }
        if !status.is_success() {
            let txt = resp.text().unwrap_or_default();
            return Err(CheckerLeakError::ApiError(status.as_u16(), txt));
        }

        let res: VerifyResponse = resp.json()?;
        Ok(res)
    }
}
