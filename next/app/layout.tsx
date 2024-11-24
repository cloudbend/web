import type { Metadata } from "next";
import { Noto_Sans as NotoSans } from "next/font/google";
import "./globals.css";

const notoSans = NotoSans({ subsets: ["latin"], fallback: ["sans-serif"] });

export const metadata: Metadata = {
  title: "Cloudbend",
  description: "Let us help you build the future",
};

const Layout = ({ children }: { children: React.ReactNode }) => (
  <html lang="en">
    <body
      className={`${notoSans.className} antialiased`}
    >
      {children}
    </body>
  </html>
);

export default Layout;
