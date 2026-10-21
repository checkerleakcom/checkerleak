"""
EmailService: Production-ready transactional email delivery.
Supports Resend API (Free Tier: 3,000 emails/month, zero latency, no blocked SMTP ports),
standard SMTP (Resend SMTP, SendGrid, Amazon SES, Mailgun, Postmark),
and graceful safe console logging fallback for development.
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
        """Sends an HTML transactional verification email with 1-click confirmation link."""
        verify_url = f"{self.base_url}/verify-email?token={token}"
        subject = "Verify your email — CheckerLeak.com"
        name = full_name or "there"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #07090e; color: #f8fafc; margin: 0; padding: 24px; }}
            .container {{ max-width: 540px; margin: 0 auto; background-color: #0d111a; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px; }}
            .logo {{ font-size: 20px; font-weight: 800; color: #38bdf8; margin-bottom: 24px; }}
            h1 {{ font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }}
            p {{ font-size: 14px; line-height: 1.6; color: #94a3b8; margin-bottom: 24px; }}
            .btn {{ display: inline-block; background-color: #06b6d4; color: #000000; font-weight: 700; text-decoration: none; padding: 12px 28px; border-radius: 10px; font-size: 14px; }}
            .token-box {{ margin-top: 24px; padding: 12px; background-color: #07090e; border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; font-family: monospace; font-size: 11px; word-break: break-all; color: #64748b; }}
            .footer {{ margin-top: 32px; font-size: 11px; color: #475569; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 16px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="logo">⚡ CheckerLeak.com</div>
            <h1>Verify your email address</h1>
            <p>Hi {name},<br><br>Thank you for creating an account on CheckerLeak. Click the button below to verify your email address and activate full API capabilities.</p>
            <a href="{verify_url}" class="btn" target="_blank">Verify Email Address</a>
            <div class="token-box">
              Or copy this verification link into your browser:<br>
              {verify_url}
            </div>
            <div class="footer">
              If you did not sign up for CheckerLeak, you can safely ignore this email.
            </div>
          </div>
        </body>
        </html>
        """

        text_body = f"Hi {name},\n\nPlease verify your email for CheckerLeak.com by visiting this link:\n{verify_url}\n\nThank you,\nCheckerLeak Team"

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
