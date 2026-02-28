import * as React from "react";
import {
    Mail,
    Plus,
    Trash2,
    ShieldCheck,
    ShieldAlert,
    Loader2,
    DownloadCloud,
    ExternalLink
} from "lucide-react";
import {
    Button,
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
    CardFooter,
    Input,
    Badge,
    useToast,
    cn
} from "../components/ui";

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
    const [isSubmitting, setIsSubmitting] = React.useState(false);
    const { addToast } = useToast();

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
        setIsSubmitting(true);
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
                addToast("New account connected successfully.", "success");
                setNewEmail("");
                setIsAdding(false);
                fetchAccounts();
            } else {
                const data = await res.json();
                addToast(data.detail || "Connection failed.", "error");
            }
        } catch (err) {
            addToast("Failed to connect account.", "error");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleConnectOAuth = async (account: ConnectedAccount) => {
        if (account.provider !== 'gmail') {
            addToast(`${account.provider.toUpperCase()} integration is coming soon.`, "info");
            return;
        }
        try {
            addToast("Redirecting to authorization...", "info");
            const token = localStorage.getItem("access_token");
            const res = await fetch(`/api/v1/connected-accounts/${account.id}/authorize`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            if (data.authorization_url) {
                window.location.href = data.authorization_url;
            }
        } catch (err) {
            addToast("Failed to reach authorization portal.", "error");
        }
    };

    const handleImport = async (accountId: number) => {
        try {
            addToast("Batch fetch triggered.", "info");
            const token = localStorage.getItem("access_token");
            const res = await fetch(`/api/v1/connected-accounts/${accountId}/fetch?limit=10`, {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            if (res.ok) {
                addToast("Inporting latest transactions...", "success");
            } else {
                addToast(data.detail || "Import failed.", "error");
            }
        } catch (err) {
            addToast("Connection error.", "error");
        }
    };

    const handleDelete = async (accountId: number) => {
        if (!confirm("Are you sure you want to disconnect this account?")) return;
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch(`/api/v1/connected-accounts/${accountId}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                addToast("Account disconnected.", "success");
                fetchAccounts();
            } else {
                addToast("Disconnection failed.", "error");
            }
        } catch (err) {
            addToast("Network error.", "error");
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex justify-between items-end">
                <div className="space-y-1">
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">Account Connections</h1>
                    <p className="text-muted-foreground">Link your financial data sources for automated processing.</p>
                </div>
                <Button onClick={() => setIsAdding(true)} size="default" className="font-semibold">
                    <Plus className="w-4 h-4 mr-2" />
                    New Connection
                </Button>
            </div>

            {isAdding && (
                <Card className="animate-in slide-in-from-top-4 duration-300">
                    <CardHeader>
                        <CardTitle className="text-xl">Connect New Account</CardTitle>
                        <CardDescription>Select a provider and enter the email address you wish to synchronize.</CardDescription>
                    </CardHeader>
                    <form onSubmit={handleAddAccount}>
                        <CardContent className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Provider</label>
                                    <select
                                        className="w-full flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                                        value={newProvider}
                                        onChange={(e) => setNewProvider(e.target.value)}
                                    >
                                        <option value="gmail">Google (Gmail)</option>
                                        <option value="outlook">Outlook</option>
                                        <option value="imap">IMAP</option>
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Email Address</label>
                                    <Input
                                        placeholder="user@example.com"
                                        type="email"
                                        value={newEmail}
                                        onChange={(e) => setNewEmail(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter className="gap-2 bg-muted/30 p-4 border-t border-border">
                            <Button type="submit" disabled={isSubmitting} size="sm">
                                {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
                                Save Connection
                            </Button>
                            <Button variant="ghost" size="sm" onClick={() => setIsAdding(false)}>Cancel</Button>
                        </CardFooter>
                    </form>
                </Card>
            )}

            {loading ? (
                <div className="flex flex-col items-center justify-center p-24 text-muted-foreground opacity-50">
                    <Loader2 className="w-8 h-8 animate-spin mb-4" />
                    <p className="text-xs font-semibold uppercase tracking-widest">Fetching connections...</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4">
                    {accounts.length === 0 ? (
                        <div className="flex flex-col items-center justify-center p-24 border-2 border-dashed border-border rounded-lg text-center gap-4">
                            <Mail className="w-12 h-12 text-muted-foreground opacity-20" />
                            <div className="space-y-1">
                                <h3 className="text-lg font-semibold text-foreground">No Connections Yet</h3>
                                <p className="text-sm text-muted-foreground max-w-xs mx-auto">Start by adding an email account to initialize automated transaction processing.</p>
                            </div>
                            <Button variant="outline" className="mt-2" onClick={() => setIsAdding(true)}>
                                Add Your First Account
                            </Button>
                        </div>
                    ) : (
                        accounts.map(account => (
                            <Card key={account.id} className="hover:border-primary/30 transition-colors">
                                <CardContent className="p-6 flex items-center justify-between">
                                    <div className="flex items-center gap-6">
                                        <div className={cn(
                                            "w-12 h-12 rounded-lg flex items-center justify-center",
                                            account.token_expiry ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400' : 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400'
                                        )}>
                                            <Mail className="w-6 h-6" />
                                        </div>
                                        <div>
                                            <p className="font-bold text-lg text-foreground">{account.email}</p>
                                            <div className="flex items-center gap-3 mt-1">
                                                <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                                                    {account.provider}
                                                </span>
                                                <div className="w-1 h-1 rounded-full bg-border" />
                                                {account.token_expiry ? (
                                                    <Badge variant="success" className="h-5 px-2">
                                                        <ShieldCheck className="w-3 h-3 mr-1" />
                                                        Active
                                                    </Badge>
                                                ) : (
                                                    <Badge variant="warning" className="h-5 px-2">
                                                        <ShieldAlert className="w-3 h-3 mr-1" />
                                                        Auth Required
                                                    </Badge>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        {account.token_expiry && (
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleImport(account.id)}
                                                className="text-xs h-9"
                                            >
                                                <DownloadCloud className="w-3.5 h-3.5 mr-2" />
                                                Import Data
                                            </Button>
                                        )}
                                        {!account.token_expiry && (
                                            <Button
                                                size="sm"
                                                onClick={() => handleConnectOAuth(account)}
                                                className={cn("text-xs h-9", account.provider !== 'gmail' && "opacity-50 grayscale cursor-not-allowed")}
                                                variant={account.provider === 'gmail' ? 'primary' : 'outline'}
                                            >
                                                Authorize
                                                <ExternalLink className="w-3.5 h-3.5 ml-2" />
                                            </Button>
                                        )}
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="h-9 w-9 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                                            onClick={() => handleDelete(account.id)}
                                        >
                                            <Trash2 className="w-4 h-4" />
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
