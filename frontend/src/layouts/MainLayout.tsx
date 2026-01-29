import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />
      <main className="p-8">{children}</main>
    </div>
  );
}