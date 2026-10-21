import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CheckerLeak Executive Cockpit — Telephony & Revenue Intelligence",
  description: "Linear Dark-Tech Admin Dashboard with real-time carrier telemetry, VoIP fraud detection, and financial auditing.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="font-sans antialiased bg-[#07090e] text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
