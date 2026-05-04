import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GIX Return Assistant",
  description: "Equipment return tracking for GIX Makerspace",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${geist.className} bg-gray-50 min-h-screen`}>
        <nav className="bg-purple-800 text-white px-4 py-3 flex items-center gap-6 flex-wrap">
          <Link href="/" className="font-bold text-lg tracking-tight">
            GIX Return Assistant
          </Link>
          <Link href="/events" className="text-purple-200 hover:text-white text-sm">
            Events
          </Link>
        </nav>
        <main className="max-w-5xl mx-auto px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
