import { auth } from "@/auth";
import AuthenticatedNavbar from "@/components/ui/authenticatedNavbar";
import Sidebar from "@/components/ui/sidebar";

export default async function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await auth();
  if (!session) {
    return <div>Not Authenticated</div>;
  }
  return (
    <div className="h-screen flex flex-col">
      <AuthenticatedNavbar />
      <div className="flex flex-grow">
        <Sidebar />
        <div className="flex-grow">{children}</div>
      </div>
    </div>
  );
}
