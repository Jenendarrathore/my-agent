import * as React from "react";
import { Mail, Plus, Trash2, ShieldCheck, ExternalLink, ShieldAlert, Loader2, DownloadCloud } from "lucide-react";
import { Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Input, cn } from "../components/ui";

interface ConnectedAccount {
    id: number;
    provider: string;
    email: string;
    is_active: boolean;
    token_expiry: string | null;
}

export function ConnectedAccounts() {
    const [accounts, setAccounts] = React.useState<ConnectedAccount[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [isAdding, setIsAdding] = React.useState(false);
    const [newEmail, setNewEmail] = React.useState("");
    const [newProvider, setNewProvider] = React.useState("gmail");
    const [error, setError] = React.useState("");

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
        } finally {
            setLoading(false);
        }
    }, []);

    React.useEffect(() => {
        fetchAccounts();
    }, [fetchAccounts]);

    const handleAddAccount = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/v1/connected-accounts/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    provider: newProvider,
                    email: newEmail,
                })
            });
            if (res.ok) {
                setNewEmail("");
                setIsAdding(false);
                fetchAccounts();
            } else {
                const data = await res.json();
                setError(data.detail || "Failed to add account");
            }
        } catch (err) {
            setError("Something went wrong");
        }
    };

    const handleConnectOAuth = async (account: ConnectedAccount) => {
        if (account.provider !== 'gmail') {
            alert(`${account.provider.toUpperCase()} integration is coming soon!`);
            return;
        }
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch(`/api/v1/connected-accounts/${account.id}/authorize`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            if (data.authorization_url) {
                window.location.href = data.authorization_url;
            }
        } catch (err) {
            console.error("Failed to start OAuth", err);
        }
    };

    const handleImport = async (accountId: number) => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch(`/api/v1/connected-accounts/${accountId}/fetch?limit=10`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            if (res.ok) {
                alert(data.message);
            } else {
                alert(`Error: ${data.detail || 'Failed to trigger fetch'}`);
            }
        } catch (err) {
            console.error("Failed to trigger import", err);
        }
    };

    const handleDelete = async (accountId: number) => {
        if (!confirm("Are you sure you want to disconnect this account?")) return;
        try {
            const token = localStorage.getItem("access_token");
            await fetch(`/api/v1/connected-accounts/${accountId}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` }
            });
            fetchAccounts();
        } catch (err) {
            console.error("Failed to delete account", err);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex justify-between items-end">
                <div className="space-y-2">
                    <h1 className="text-4xl font-bold tracking-tight text-slate-900 italic">Connected Accounts</h1>
                    <p className="text-slate-500 text-lg">Manage your email sources and financial connections.</p>
                </div>
                <Button onClick={() => setIsAdding(true)} size="lg" className="shadow-md hover:scale-105 transition-transform">
                    <Plus className="w-5 h-5 mr-2" />
                    Add Account
                </Button>
            </div>

            {isAdding && (
                <Card className="border-primary shadow-xl animate-in slide-in-from-top-4 duration-300 overflow-hidden">
                    <div className="h-1 bg-primary animate-pulse" />
                    <CardHeader>
                        <CardTitle>Register New Source</CardTitle>
                        <CardDescription>Select a provider and enter the email address you want to connect.</CardDescription>
                    </CardHeader>
                    <form onSubmit={handleAddAccount}>
                        <CardContent className="space-y-6">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-slate-700">Provider</label>
                                    <select
                                        className="w-full flex h-12 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2"
                                        value={newProvider}
                                        onChange={(e) => setNewProvider(e.target.value)}
                                    >
                                        <option value="gmail">Gmail</option>
                                        <option value="outlook">Outlook</option>
                                        <option value="imap">IMAP</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-slate-700">Email Address</label>
                                    <Input
                                        placeholder="account@example.com"
                                        type="email"
                                        value={newEmail}
                                        onChange={(e) => setNewEmail(e.target.value)}
                                        required
                                        className="h-12"
                                    />
                                </div>
                            </div>
                            {error && <p className="text-sm text-destructive font-medium bg-destructive/10 p-3 rounded-lg border border-destructive/20">{error}</p>}
                        </CardContent>
                        <CardFooter className="gap-3 bg-slate-50/50 p-6">
                            <Button type="submit" size="lg">Save & Continue</Button>
                            <Button variant="outline" size="lg" onClick={() => setIsAdding(false)}>Cancel</Button>
                        </CardFooter>
                    </form>
                </Card>
            )}

            {loading ? (
                <div className="flex justify-center p-12">
                    <Loader2 className="w-12 h-12 animate-spin text-primary/30" />
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-6">
                    {accounts.length === 0 ? (
                        <div className="text-center p-20 bg-white rounded-2xl border-2 border-dashed border-slate-200 animate-in zoom-in duration-500">
                            <Mail className="w-16 h-16 text-slate-200 mx-auto mb-4" />
                            <h3 className="text-xl font-semibold text-slate-900">No sources yet</h3>
                            <p className="text-slate-500 mt-2">Add an email account to start syncing transactions.</p>
                            <Button variant="outline" className="mt-6" onClick={() => setIsAdding(true)}>
                                Get Started
                            </Button>
                        </div>
                    ) : (
                        accounts.map(account => (
                            <Card key={account.id} className="hover:shadow-lg transition-all duration-300 border-none group">
                                <CardContent className="p-8 flex items-center justify-between">
                                    <div className="flex items-center gap-6">
                                        <div className={cn(
                                            "p-4 rounded-2xl transition-colors duration-300",
                                            account.token_expiry ? 'bg-green-100/50 group-hover:bg-green-100' : 'bg-amber-100/50 group-hover:bg-amber-100'
                                        )}>
                                            <Mail className={cn(
                                                "w-7 h-7",
                                                account.token_expiry ? 'text-green-600' : 'text-amber-600'
                                            )} />
                                        </div>
                                        <div>
                                            <p className="font-bold text-xl text-slate-900">{account.email}</p>
                                            <div className="flex items-center gap-3 mt-1">
                                                <span className="text-xs uppercase font-extrabold text-slate-400 tracking-wider">
                                                    {account.provider}
                                                </span>
                                                {account.token_expiry ? (
                                                    <span className="flex items-center gap-1.5 text-xs text-green-600 font-bold bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                                                        <ShieldCheck className="w-3 h-3" />
                                                        ACTIVE
                                                    </span>
                                                ) : (
                                                    <span className="flex items-center gap-1.5 text-xs text-amber-600 font-bold bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                                                        <ShieldAlert className="w-3 h-3" />
                                                        MISSING AUTH
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        {account.token_expiry && (
                                            <Button
                                                variant="outline"
                                                size="default"
                                                className="border-primary text-primary hover:bg-primary/5 font-semibold"
                                                onClick={() => handleImport(account.id)}
                                            >
                                                <DownloadCloud className="w-4 h-4 mr-2" />
                                                Import Last 10
                                            </Button>
                                        )}
                                        {!account.token_expiry && (
                                            <Button
                                                size="lg"
                                                onClick={() => handleConnectOAuth(account)}
                                                className={cn("shadow-md", account.provider !== 'gmail' && "opacity-50 grayscale cursor-not-allowed")}
                                                variant={account.provider !== 'gmail' ? 'outline' : 'primary'}
                                            >
                                                <ExternalLink className="w-4 h-4 mr-2" />
                                                {account.provider === 'gmail' ? 'Authorize Now' : 'Coming Soon'}
                                            </Button>
                                        )}
                                        <Button
                                            variant="outline"
                                            size="icon"
                                            className="w-12 h-12 text-slate-400 hover:text-destructive hover:bg-destructive/10 border-slate-200"
                                            onClick={() => handleDelete(account.id)}
                                        >
                                            <Trash2 className="w-5 h-5" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
