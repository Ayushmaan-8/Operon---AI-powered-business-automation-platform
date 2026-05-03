import Link from "next/link";

interface LeadCardProps {
  id: string;
  name: string;
  email: string;
  status: string;
  source: string;
  created_at: string;
}


export default function LeadCard({ id, name, email, status, source, created_at }: LeadCardProps) {
  const date = new Date(created_at).toLocaleDateString();

  return (
    <Link href={`/dashboard/leads/${id}`}>
      <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-5 hover:border-[rgba(0,0,0,0.15)] transition-colors cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex flex-col">
          <span className="font-semibold text-[#0d0d0d]">{name || "Unknown Name"}</span>
          <span className="text-sm text-[#666666]">{email || "No email provided"}</span>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          <span className="px-3 py-1 bg-gray-50 text-xs font-medium text-[#666666] rounded-full border border-[rgba(0,0,0,0.05)] capitalize">
            {source || "Direct"}
          </span>
          <span className="px-3 py-1 bg-[#18E299]/10 text-xs font-medium text-[#18E299] rounded-full border border-[#18E299]/20 capitalize">
            {status}
          </span>
          <span className="text-xs text-[#666666] w-[80px] text-right">
            {date}
          </span>
        </div>
      </div>
    </Link>
  );
}
