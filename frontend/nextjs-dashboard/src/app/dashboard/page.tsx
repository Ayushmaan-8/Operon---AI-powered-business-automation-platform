export const dynamic = "force-dynamic";

import AnalyticsCard from "@/components/AnalyticsCard";
import LeadCard from "@/components/LeadCard";


async function getAnalytics() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/dashboard/analytics`, { cache: "no-store" });
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    console.error("Error fetching analytics:", error);
    return null;
  }
}

async function getLeads() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/dashboard/leads`, { cache: "no-store" });
    if (!res.ok) return [];
    return res.json();
  } catch (error) {
    console.error("Error fetching leads:", error);
    return [];
  }
}

export default async function DashboardPage() {
  const [analytics, leads] = await Promise.all([
    getAnalytics(),
    getLeads()
  ]);

  return (
    <div className="flex flex-col gap-10">
      <div>
        <h1 className="text-2xl font-bold text-[#0d0d0d] mb-6">Overview</h1>
        {analytics ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <AnalyticsCard title="Total Leads" value={analytics.total_leads} />
            <AnalyticsCard title="High Priority" value={analytics.high_priority} />
            <AnalyticsCard title="Medium Priority" value={analytics.medium_priority} />
            <AnalyticsCard title="Low Priority" value={analytics.low_priority} />
          </div>
        ) : (
          <p className="text-sm text-red-500">Failed to load analytics data.</p>
        )}
      </div>

      <div>
        <h2 className="text-xl font-bold text-[#0d0d0d] mb-4">Recent Leads</h2>
        <div className="flex flex-col gap-3">
          {leads.length > 0 ? (
            leads.map((item: any) => {
              const lead = item.lead || item; // handles both cases
              if (!lead?.id) return null; // skip broken data
              return (
              <LeadCard
                key={lead.id}
                id={lead.id}
                name={lead.name}
                email={lead.email}
                status={lead.status}
                source={lead.source}
                created_at={lead.created_at}
              />
              );
              console.log("ITEM:", item);
            })
          ) : (
            <div className="p-8 bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] text-center">
              <p className="text-sm text-[#666666]">No leads found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
