import * as React from "react";
import { Link, useLocation, useNavigate, Outlet } from "react-router-dom";
import {
    LayoutDashboard,
    Mail,
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
    const [user, setUser] = React.useState<any>(null);
    const location = useLocation();
    const navigate = useNavigate();

    React.useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (e) {
                console.error("Failed to parse user", e);
            }
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login");
    };

    const navItems = [
        { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
        { icon: Mail, label: "Emails", path: "/emails" },
        { icon: LinkIcon, label: "Connections", path: "/connected-accounts" },
        { icon: Activity, label: "Jobs", path: "/jobs" },
        { icon: CreditCard, label: "Transactions", path: "/transactions" },
        { icon: History, label: "Activity Log", path: "/activity" },
        { icon: Settings, label: "Settings", path: "/settings" },
    ];

    return (
        <div className="flex min-h-screen bg-background text-foreground">
            {/* Sidebar */}
            <aside
                className={cn(
                    "border-r border-border bg-card flex flex-col transition-all duration-300 ease-in-out z-30 relative",
                    isCollapsed ? "w-16" : "w-64"
                )}
            >
                <div className="p-6 flex items-center justify-between">
                    {!isCollapsed && (
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                                <ShieldCheck className="w-5 h-5 text-primary-foreground" />
                            </div>
                            <div className="flex flex-col">
                                <span className="text-xl font-bold tracking-tight text-foreground">Financial Agent</span>
                                {user?.role?.name === "admin" && (
                                    <span className="text-[10px] font-bold text-primary uppercase tracking-widest leading-none">Admin Level</span>
                                )}
                            </div>
                        </div>
                    )}
                    {isCollapsed && (
                        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center mx-auto">
                            <ShieldCheck className="w-5 h-5 text-primary-foreground" />
                        </div>
                    )}
                </div>

                <nav className="flex-1 px-3 space-y-1 mt-6">
                    {navItems.map((item) => {
                        const isActive = location.pathname === item.path;
                        const Icon = item.icon;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                title={isCollapsed ? item.label : ""}
                                className={cn(
                                    "flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors group",
                                    isActive
                                        ? "bg-secondary text-secondary-foreground"
                                        : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
                                )}
                            >
                                <Icon className={cn("w-5 h-5 shrink-0", isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground")} />
                                {!isCollapsed && (
                                    <span className="text-sm font-medium">
                                        {item.label}
                                    </span>
                                )}
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-border space-y-2">
                    <Button
                        variant="ghost"
                        size="sm"
                        className={cn("w-full justify-start text-muted-foreground hover:text-destructive hover:bg-destructive/10", isCollapsed && "justify-center px-0")}
                        onClick={handleLogout}
                    >
                        <LogOut className="w-4 h-4 shrink-0" />
                        {!isCollapsed && <span className="ml-2 font-medium">Log out</span>}
                    </Button>

                    <button
                        className="w-full flex items-center justify-center py-2 text-muted-foreground hover:text-foreground transition-colors"
                        onClick={() => setIsCollapsed(!isCollapsed)}
                    >
                        {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 h-screen overflow-y-auto">
                <div className="p-8 max-w-6xl mx-auto">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
