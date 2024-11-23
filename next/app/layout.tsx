import type { Metadata } from "next";
import { Noto_Sans as NotoSans, Noto_Sans_Mono as NotoSansMono } from "next/font/google";
import "./globals.css";

const notoSans = NotoSans({ subsets: ["latin"] });
const notoSansMono = NotoSansMono({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Cloudbend",
  description: "Bend the cloud to your will",
};

const Layout = ({ children }: { children: React.ReactNode }) => (
  <html lang="en">
    <body
      className={`${notoSans.className} ${notoSansMono.className} antialiased`}
    >
      {children}
    </body>
  </html>
);

export default Layout;
