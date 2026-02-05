import type { Metadata } from "next";
import { Chivo, Space_Grotesk } from "next/font/google";

import { Providers } from "./providers";
import "./globals.css";

const heading = Chivo({
  subsets: ["latin"],
  variable: "--font-heading",
  weight: ["500", "700", "900"]
});

const body = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-body",
  weight: ["400", "500", "600", "700"]
});

export const metadata: Metadata = {
  title: "Creatory Studio",
  description: "Creator-first multi-agent orchestration studio"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${heading.variable} ${body.variable}`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
