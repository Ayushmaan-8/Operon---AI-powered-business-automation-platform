export const dynamic = "force-dynamic";

import Link from "next/link";
import { notFound } from "next/navigation";

async function getLeadDetail(id: string) {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/dashboard/leads/${id}`, { cache: "no-store", headers: { "Cache-Control": "no-cache"} });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error("Failed to fetch lead");
    return res.json();
  } catch (error) {
    console.error("Error fetching lead detail:", error);
    return null;
  }
}


export default async function LeadDetailPage({ params }: any) {
  const resolvedParams = await params;   // 👈 THIS is the key

  const id = resolvedParams?.id;

  if (!id) return notFound();

  const data = await getLeadDetail(id);
  
  console.log("DATA:", data);

  if (!data || !data.lead) {
    return notFound();
  }

  const { lead, ai_decision, action } = data;
  const reply = lead?.reply;

  return (
    <div className="flex flex-col gap-6">
      <Link href="/dashboard" className="text-sm font-medium text-[#666666] hover:text-[#0d0d0d] transition-colors inline-flex items-center gap-2">
        ← Back to Dashboard
      </Link>

      <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-6 sm:p-8">
        <h1 className="text-2xl font-bold text-[#0d0d0d] mb-1">{lead.name || "Unknown Lead"}</h1>
        <p className="text-sm text-[#666666] mb-6">{lead.email || "No email"}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Source</span>
            <span className="text-sm text-[#0d0d0d] capitalize">{lead.source || "Direct"}</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Status</span>
            <span className="text-sm text-[#0d0d0d] capitalize">{lead.status}</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Service Requested</span>
            <span className="text-sm text-[#0d0d0d]">{lead.service_requested || "N/A"}</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Budget</span>
            <span className="text-sm text-[#0d0d0d]">{lead.budget ? `$${lead.budget}` : "N/A"}</span>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-[rgba(0,0,0,0.05)]">
          <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider mb-3 block">Message</span>
          <p className="text-sm text-[#0d0d0d] whitespace-pre-wrap">{lead.message || "No message provided."}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Decision Card */}
        <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-6 sm:p-8">
          <h2 className="text-lg font-bold text-[#0d0d0d] mb-4 flex items-center gap-2">
            AI Analysis
            {ai_decision && (
              <span className="px-2 py-0.5 bg-[#18E299]/10 text-[10px] font-bold text-[#18E299] rounded uppercase tracking-wider">
                Score: {ai_decision.lead_score}
              </span>
            )}
          </h2>
          
          {ai_decision ? (
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Intent</span>
                <span className="text-sm text-[#0d0d0d]">{ai_decision.intent}</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Category</span>
                <span className="text-sm text-[#0d0d0d] capitalize">{ai_decision.category}</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Confidence</span>
                <span className="text-sm text-[#0d0d0d]">
                    {ai_decision?.confidence !== undefined
                        ? `${Math.round(Number(ai_decision.confidence) * 100)}%`
                        : "N/A"}
                </span>
              </div>
              <div className="flex flex-col gap-1 mt-2">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Reasoning</span>
                <p className="text-sm text-[#0d0d0d]">{ai_decision.reasoning}</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-[#666666]">No AI analysis available for this lead.</p>
          )}
        </div>

        {/* Action Taken Card */}
        <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-6 sm:p-8">
          <h2 className="text-lg font-bold text-[#0d0d0d] mb-4">Automated Action</h2>
          
          {action ? (
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Action Taken</span>
                <span className="text-sm font-medium text-[#0d0d0d] capitalize">{action.action.replace('_', ' ')}</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Priority</span>
                <span className="text-sm text-[#0d0d0d] capitalize">{action.priority}</span>
              </div>
              <div className="flex flex-col gap-1 mt-2">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider">Reason</span>
                <p className="text-sm text-[#0d0d0d]">{action.reason}</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-[#666666]">No automated action was triggered.</p>
          )}
        </div>

        {/* AI Reply Card */}
        <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-6 sm:p-8">
          <h2 className="text-lg font-bold text-[#0d0d0d] mb-4">AI Reply</h2>

          {reply ? (
            <div className="flex flex-col gap-4">
              <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider mb-2">Generated Response</span>
              <p className="text-sm text-[#0d0d0d] whitespace-pre-wrap">{reply}</p>

              <div className="mt-2 border-t border-[rgba(0,0,0,0.05)] pt-4">
                <span className="text-xs font-semibold text-[#666666] uppercase tracking-wider mb-2 block">Used For</span>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 bg-[#f0f0f0] text-xs font-medium text-[#666666] rounded capitalize">
                    {ai_decision?.category || "N/A"}
                  </span>
                  <span className="px-2 py-1 bg-[#f0f0f0] text-xs font-medium text-[#666666] rounded">
                    {ai_decision?.intent || "N/A"}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-sm text-[#666666]">No AI reply generated for this lead.</p>
          )}
        </div>

      </div>
    </div>
  );
}
