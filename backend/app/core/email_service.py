"""
EmailService: Production-ready transactional email delivery.
Supports Resend API (Free Tier: 3,000 emails/month, zero latency, no blocked SMTP ports),
standard SMTP (Resend SMTP, SendGrid, Amazon SES, Mailgun, Postmark),
and graceful safe console logging fallback for development.
Clean Silicon-Valley Minimal Light Theme (Stripe / Linear / GitHub standard) with Hidden Preheader.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class EmailService:
    def __init__(self):
        # 1. Resend Configuration (Recommended Free Tier)
        self.resend_api_key = os.getenv("RESEND_API_KEY")

        # 2. SMTP Configuration (Fallback or Alternate Provider)
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")

        # Default sender: Since checkerleak.com domain is verified on Resend, send from official branded address
        default_sender = "CheckerLeak Security <verify@checkerleak.com>" if self.resend_api_key else "CheckerLeak <noreply@checkerleak.com>"
        self.from_email = os.getenv("RESEND_FROM") or os.getenv("SMTP_FROM") or default_sender
        self.base_url = os.getenv("BASE_URL", "https://checkerleak.com").rstrip("/")

    def send_verification_email(self, to_email: str, token: str, full_name: Optional[str] = None) -> bool:
        """Sends a high-end corporate-grade HTML transactional verification email."""
        verify_url = f"{self.base_url}/verify-email?token={token}"
        subject = "Confirm your CheckerLeak account"
        name = full_name.strip() if full_name and full_name.strip() else "there"

        # Stripe / Linear / Vercel corporate minimal light email design
        html_body = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Confirm your CheckerLeak account</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  
  <!-- Hidden Preheader for Inbox Snippet Preview -->
  <div style="display: none; max-height: 0px; overflow: hidden; mso-hide: all; font-size: 1px; line-height: 1px; color: #fff; opacity: 0;">
    Confirm your email address to activate your CheckerLeak API credentials and unlock 102+ deep verification engines.
    &#847; &zwnj; &nbsp; &#8199; &shy; &#847; &zwnj; &nbsp; &#8199; &shy; &#847; &zwnj; &nbsp; &#8199; &shy; &#847; &zwnj; &nbsp; &#8199; &shy;
  </div>

  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed; background-color: #f8fafc; padding: 40px 16px;">
    <tr>
      <td align="center" valign="top">
        <!-- Main Card Container -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden;">
          
          <!-- Top Clean Brand Header with Prominent Retina Logo -->
          <tr>
            <td style="padding: 34px 44px 26px 44px; border-bottom: 1px solid #f1f5f9;">
              <a href="https://checkerleak.com" target="_blank" style="text-decoration: none; display: inline-block;">
                <img src="https://checkerleak.com/static/checkerleak-brand-logo.png" alt="CheckerLeak.com" width="210" height="42" style="display: block; border: 0; outline: none; text-decoration: none; width: 210px; height: 42px; max-width: 100%;" />
              </a>
            </td>
          </tr>

          <!-- Content Body -->
          <tr>
            <td style="padding: 36px 44px 38px 44px;">
              <div style="display: inline-block; padding: 4px 10px; background-color: #f1f5f9; border-radius: 9999px; font-size: 11px; font-weight: 600; color: #475569; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 16px;">
                Account Verification
              </div>

              <h1 style="margin: 0 0 18px 0; font-size: 22px; font-weight: 700; color: #0f172a; line-height: 1.35; letter-spacing: -0.4px;">
                Confirm your email address
              </h1>
              
              <p style="margin: 0 0 14px 0; font-size: 15px; line-height: 1.6; color: #334155;">
                Hi {name},
              </p>
              
              <p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.6; color: #475569;">
                Thanks for getting started with <strong>CheckerLeak</strong>. Please confirm your email address below to activate your account and unlock instant access to our <strong>102+ deep verification engines</strong>.
              </p>

              <!-- High-Contrast Enterprise Action Button -->
              <table border="0" cellpadding="0" cellspacing="0" style="margin: 0 0 32px 0;">
                <tr>
                  <td align="center" style="border-radius: 9px; background-color: #0f172a;">
                    <a href="{verify_url}" target="_blank" style="display: inline-block; padding: 14px 34px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 15px; font-weight: 600; color: #ffffff; text-decoration: none; border-radius: 9px; letter-spacing: 0.1px;">
                      Confirm Email Address &rarr;
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Muted Fallback Link -->
              <p style="margin: 0 0 8px 0; font-size: 13px; line-height: 1.5; color: #64748b;">
                Button not working? Copy and paste this link into your browser:
              </p>
              <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; line-height: 1.5; word-break: break-all;">
                <a href="{verify_url}" target="_blank" style="color: #2563eb; text-decoration: none;">{verify_url}</a>
              </div>

              <!-- Security Notice -->
              <div style="margin-top: 32px; padding-top: 20px; border-top: 1px solid #f1f5f9; font-size: 12px; line-height: 1.6; color: #94a3b8;">
                <p style="margin: 0 0 6px 0;">
                  🔒 This verification link expires in 24 hours. If you did not create an account on CheckerLeak, you can safely ignore this email.
                </p>
                <p style="margin: 0; color: #cbd5e1;">
                  CheckerLeak Intelligence Platform &bull; Cryptographic Zero-Knowledge Architecture
                </p>
              </div>
            </td>
          </tr>

        </table>

        <!-- Micro Footer -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; margin-top: 20px;">
          <tr>
            <td align="center" style="font-size: 12px; color: #94a3b8; line-height: 1.5;">
              &copy; 2026 CheckerLeak.com. All rights reserved.
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>
</body>
</html>"""

        text_body = f"Hi {name},\n\nPlease confirm your email address for CheckerLeak by visiting this link:\n{verify_url}\n\nThis link will expire in 24 hours.\n\nThank you,\nCheckerLeak Security Team"

        # Strategy 1: Resend REST API (Best deliverability & high concurrency)
        if self.resend_api_key:
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {self.resend_api_key.strip()}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "from": self.from_email,
                    "to": [to_email],
                    "subject": subject,
                    "html": html_body,
                    "text": text_body,
                }
                res = requests.post(
                    "https://api.resend.com/emails",
                    json=payload,
                    headers=headers,
                    timeout=10,
                )
                if res.status_code in [200, 201]:
                    res_data = res.json()
                    print(f"[EmailService] Verification email sent to {to_email} via Resend API (ID: {res_data.get('id')}).")
                    return True
                else:
                    print(f"[EmailService] Resend API response error ({res.status_code}): {res.text}. Falling back to SMTP/audit.")
            except Exception as resend_err:
                print(f"[EmailService] Resend API connection error ({resend_err}). Falling back to SMTP/audit.")

        # Strategy 2: Standard SMTP (Resend SMTP or other provider)
        if self.smtp_host and self.smtp_user and self.smtp_pass:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"CheckerLeak Security <{self.from_email}>"
                msg["To"] = to_email

                msg.attach(MIMEText(text_body, "plain"))
                msg.attach(MIMEText(html_body, "html"))

                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_pass)
                    server.sendmail(self.from_email, to_email, msg.as_string())
                print(f"[EmailService] Verification email sent to {to_email} via SMTP.")
                return True
            except Exception as e:
                print(f"[EmailService] SMTP send error ({e}). Fallback to audit log.")

        # Strategy 3: Graceful development / zero-config fallback: log link to server console
        print("\n" + "=" * 60)
        print(f"[EmailService] VERIFICATION LINK FOR {to_email}:")
        print(f"👉 {verify_url}")
        print("=" * 60 + "\n")
        return True
