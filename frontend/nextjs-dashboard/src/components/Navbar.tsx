import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full border-b border-[rgba(0,0,0,0.05)] bg-white px-6 py-4 flex items-center justify-between">
      <Link href="/dashboard" className="text-xl font-bold tracking-tight text-[#0d0d0d]">
        Operon <span className="text-[#18E299]">AI</span>
      </Link>
      <div className="flex gap-4">
        <Link href="/dashboard" className="text-sm font-medium text-[#666666] hover:text-[#0d0d0d] transition-colors">
          Dashboard
        </Link>
      </div>
    </nav>
  );
}
