import * as React from "react";
import { Link, useLocation, useNavigate, Outlet } from "react-router-dom";
import {
    LayoutDashboard,
    Settings,
    Link as LinkIcon,
    ChevronLeft,
    ChevronRight,
    LogOut,
    ShieldCheck,
    CreditCard,
    History,
    Activity
} from "lucide-react";
import { Button, cn } from "./ui";

export function MainLayout() {
    const [isCollapsed, setIsCollapsed] = React.useState(false);
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login");
    };

    const navItems = [
        { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
        { icon: LinkIcon, label: "Connected Accounts", path: "/connected-accounts" },
        { icon: Activity, label: "Jobs", path: "/jobs" },
        { icon: CreditCard, label: "Transactions", path: "/transactions" },
        { icon: History, label: "Activity", path: "/activity" },
        { icon: Settings, label: "Settings", path: "/settings" },
    ];

    return (
        <div className="flex min-h-screen bg-slate-50 transition-colors duration-300">
            {/* Sidebar */}
            <aside
                className={cn(
                    "bg-white border-r border-slate-200 flex flex-col transition-all duration-300 ease-in-out z-30",
                    isCollapsed ? "w-20" : "w-72"
                )}
            >
                <div className="p-6 flex items-center justify-between">
                    {!isCollapsed && (
                        <div className="flex items-center gap-2 animate-in fade-in zoom-in duration-300">
                            <ShieldCheck className="w-8 h-8 text-primary shrink-0" />
                            <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent italic">FinAgênt</span>
                        </div>
                    )}
                    {isCollapsed && <ShieldCheck className="w-8 h-8 text-primary mx-auto" />}
                </div>

                <nav className="flex-1 px-4 space-y-2 mt-4">
                    {navItems.map((item) => {
                        const isActive = location.pathname === item.path;
                        const Icon = item.icon;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={cn(
                                    "flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 group relative",
                                    isActive
                                        ? "bg-primary text-primary-foreground shadow-md"
                                        : "text-slate-600 hover:bg-slate-100"
                                )}
                            >
                                <Icon className={cn("w-5 h-5 shrink-0", isActive ? "text-white" : "text-slate-500 group-hover:text-primary")} />
                                {!isCollapsed && (
                                    <span className="font-semibold text-sm animate-in fade-in slide-in-from-left-2 duration-300">
                                        {item.label}
                                    </span>
                                )}
                                {isCollapsed && (
                                    <div className="absolute left-full ml-4 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 whitespace-nowrap">
                                        {item.label}
                                    </div>
                                )}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-slate-100 space-y-2">
                    <Button
                        variant="ghost"
                        className={cn("w-full justify-start text-slate-600 hover:text-destructive", isCollapsed && "justify-center")}
                        onClick={handleLogout}
                    >
                        <LogOut className="w-5 h-5 shrink-0" />
                        {!isCollapsed && <span className="ml-3 font-semibold">Logout</span>}
                    </Button>

                    <Button
                        variant="ghost"
                        size="icon"
                        className="w-full justify-center text-slate-400 hover:text-slate-600"
                        onClick={() => setIsCollapsed(!isCollapsed)}
                    >
                        {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
                    </Button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 h-screen overflow-y-auto overflow-x-hidden">
                <div className="p-8 max-w-6xl mx-auto">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
