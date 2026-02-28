import * as React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Button, Card, CardHeader, CardTitle, CardContent } from "../components/ui";
import { Mail, AlertCircle, CheckCircle2, Plus } from "lucide-react";

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
                <div className="space-y-2">
                    <h1 className="text-4xl font-bold tracking-tight text-slate-900 italic">Financial Dashboard</h1>
                    <p className="text-slate-500 text-lg">Your automated financial intelligence hub.</p>
                </div>
            </div>

            {status === "success" && (
                <div className="flex items-center gap-3 p-4 bg-green-50 text-green-700 rounded-xl border border-green-100 animate-in fade-in slide-in-from-top-2">
                    <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                    <span className="font-medium">Account {provider} connected successfully!</span>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="shadow-lg border-none bg-white p-6 flex flex-col justify-between hover:scale-[1.02] transition-transform">
                    <div className="space-y-4">
                        <div className="p-3 bg-blue-50 w-fit rounded-xl">
                            <Mail className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-slate-900">Connected Accounts</h3>
                            <p className="text-3xl font-bold text-primary">{connectedCount}</p>
                        </div>
                    </div>
                    <Button
                        variant="link"
                        className="px-0 w-fit h-auto mt-4 text-primary font-semibold"
                        onClick={() => navigate("/connected-accounts")}
                    >
                        Manage Sources →
                    </Button>
                </Card>

                <Card className="shadow-lg border-none bg-white p-6 flex flex-col justify-between hover:scale-[1.02] transition-transform">
                    <div className="space-y-4">
                        <div className="p-3 bg-amber-50 w-fit rounded-xl">
                            <AlertCircle className="w-6 h-6 text-amber-600" />
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-slate-900">Pending Authorization</h3>
                            <p className="text-3xl font-bold text-amber-600">{pendingCount}</p>
                        </div>
                    </div>
                    <Button
                        variant="link"
                        className="px-0 w-fit h-auto mt-4 text-amber-600 font-semibold"
                        onClick={() => navigate("/connected-accounts")}
                    >
                        Review Pending →
                    </Button>
                </Card>

                <Card className="shadow-lg border-none bg-gradient-to-br from-primary to-primary/80 text-primary-foreground p-6 hover:scale-[1.02] transition-transform">
                    <div className="h-full flex flex-col justify-between">
                        <h3 className="text-xl font-bold">Quick Actions</h3>
                        <div className="space-y-3 mt-4">
                            <Button
                                className="w-full bg-white text-primary hover:bg-slate-50 border-none shadow-sm"
                                onClick={() => navigate("/connected-accounts")}
                            >
                                <Plus className="w-4 h-4 mr-2" />
                                Add New Source
                            </Button>
                            <p className="text-xs text-primary-foreground/70 text-center italic">
                                More integrations coming soon
                            </p>
                        </div>
                    </div>
                </Card>
            </div>

            <Card className="shadow-lg border-none bg-white overflow-hidden">
                <CardHeader className="bg-slate-50/50">
                    <CardTitle className="text-xl">Recent Activity</CardTitle>
                </CardHeader>
                <CardContent className="h-48 flex items-center justify-center italic text-slate-400">
                    No recent activity found. Connect an account to start syncing.
                </CardContent>
            </Card>
        </div>
    );
}
