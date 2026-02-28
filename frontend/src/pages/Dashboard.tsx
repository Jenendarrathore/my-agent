import * as React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {
    Button,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Badge
} from "../components/ui";
import {
    Mail,
    AlertCircle,
    CheckCircle2,
    Plus,
    Zap,
    ArrowRight,
    Activity
} from "lucide-react";

export function Dashboard() {
    const [searchParams] = useSearchParams();
    const [accounts, setAccounts] = React.useState<any[]>([]);
    const status = searchParams.get("status");
    const provider = searchParams.get("provider");
    const navigate = useNavigate();

    const fetchAccounts = React.useCallback(async () => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/v1/connected-accounts/", {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setAccounts(data);
            }
        } catch (err) {
            console.error("Failed to fetch accounts", err);
        }
    }, []);

    React.useEffect(() => {
        fetchAccounts();
    }, [fetchAccounts]);

    const connectedCount = accounts.filter(a => a.token_expiry).length;
    const pendingCount = accounts.length - connectedCount;

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex justify-between items-end">
                <div className="space-y-1">
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">Dashboard</h1>
                    <p className="text-muted-foreground">Overview of your connected accounts and sync status.</p>
                </div>
                <div className="flex gap-2">
                    <Badge variant="success" className="h-8">
                        System Online
                    </Badge>
                </div>
            </div>

            {status === "success" && (
                <div className="flex items-center gap-3 p-4 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-100 animate-in slide-in-from-top-2 duration-300 dark:bg-emerald-900/10 dark:text-emerald-400 dark:border-emerald-800/30">
                    <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                    <span className="font-medium text-sm">Account {provider} connected successfully.</span>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Metric 1 */}
                <Card className="hover:border-primary/50 transition-colors">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Connected Accounts</CardTitle>
                        <Mail className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{connectedCount}</div>
                        <p className="text-xs text-muted-foreground mt-1">Active data sources</p>
                        <Button
                            variant="link"
                            size="sm"
                            className="p-0 h-auto mt-4 text-xs font-semibold"
                            onClick={() => navigate("/connected-accounts")}
                        >
                            View All <ArrowRight className="w-3 h-3 ml-1" />
                        </Button>
                    </CardContent>
                </Card>

                {/* Metric 2 */}
                <Card className="hover:border-amber-500/50 transition-colors">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Pending Auth</CardTitle>
                        <AlertCircle className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{pendingCount}</div>
                        <p className="text-xs text-muted-foreground mt-1">Needs attention</p>
                        <Button
                            variant="link"
                            size="sm"
                            className="p-0 h-auto mt-4 text-xs font-semibold text-amber-600 dark:text-amber-500"
                            onClick={() => navigate("/connected-accounts")}
                        >
                            Resolve Now <ArrowRight className="w-3 h-3 ml-1" />
                        </Button>
                    </CardContent>
                </Card>

                {/* Quick Action */}
                <Card className="bg-primary text-primary-foreground">
                    <CardHeader>
                        <CardTitle className="text-lg">Quick Start</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <p className="text-xs opacity-90">Add a new email account to begin syncing transactions.</p>
                        <Button
                            className="w-full bg-white text-primary hover:bg-slate-100 border-none font-semibold text-xs py-2"
                            onClick={() => navigate("/connected-accounts")}
                        >
                            <Plus className="w-3 h-3 mr-2" />
                            Add Account
                        </Button>
                    </CardContent>
                </Card>
            </div>

            <Card className="overflow-hidden">
                <CardHeader className="bg-muted/30">
                    <div className="flex items-center gap-2">
                        <Activity className="w-4 h-4 text-muted-foreground" />
                        <CardTitle className="text-lg">Recent Jobs</CardTitle>
                    </div>
                </CardHeader>
                <CardContent className="h-48 flex flex-col items-center justify-center gap-2 p-12 text-center">
                    <Zap className="h-8 w-8 text-muted-foreground opacity-20" />
                    <p className="text-sm text-muted-foreground max-w-xs">No recent sync activity found. Connect an account to start processing data.</p>
                    <Button variant="outline" size="sm" className="mt-4 text-xs" onClick={() => navigate("/connected-accounts")}>
                        Configure Sources
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
