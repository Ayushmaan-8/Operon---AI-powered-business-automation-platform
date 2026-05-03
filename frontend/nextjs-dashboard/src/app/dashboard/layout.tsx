import Navbar from "@/components/Navbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen bg-[#fafafa]">
      <Navbar />
      <main className="flex-1 w-full max-w-5xl mx-auto p-6 md:p-8">
        {children}
      </main>
    </div>
  );
}
