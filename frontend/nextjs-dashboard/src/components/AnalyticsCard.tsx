interface AnalyticsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
}

export default function AnalyticsCard({ title, value, subtitle }: AnalyticsCardProps) {
  return (
    <div className="bg-white border border-[rgba(0,0,0,0.05)] rounded-[16px] p-6 flex flex-col justify-center">
      <h3 className="text-sm font-medium text-[#666666] mb-1">{title}</h3>
      <div className="text-3xl font-bold text-[#0d0d0d]">{value}</div>
      {subtitle && <p className="text-xs text-[#666666] mt-2">{subtitle}</p>}
    </div>
  );
}
