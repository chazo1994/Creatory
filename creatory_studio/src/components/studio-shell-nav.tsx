"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/chat", label: "Chat" },
  { href: "/library", label: "Library" },
  { href: "/settings", label: "Settings" }
];

export function StudioShellNav() {
  const pathname = usePathname();

  return (
    <nav className="panel mb-3 flex flex-wrap items-center gap-2 p-2 text-sm">
      <span className="badge">Creator Studio</span>
      {links.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            key={link.href}
            href={link.href}
            className={`rounded-lg px-3 py-1.5 font-semibold transition ${
              active ? "bg-ink text-white" : "bg-white/70 text-black/70 hover:bg-white"
            }`}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
