import * as React from "react";
import {
    Mail,
    Search,
    ArrowUpDown,
    Database,
    Calendar,
    RefreshCw,
    ExternalLink
} from "lucide-react";
import {
    Button,
    Input,
    Card,
    CardContent
} from "../components/ui";

interface EmailRecord {
    id: number;
    user_id: number;
    connected_account_id: number;
    provider: string;
    subject: string;
    received_at: string;
}

export function Emails() {
    const [emails, setEmails] = React.useState<EmailRecord[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [searchQuery, setSearchQuery] = React.useState("");
    const [sortOrder, setSortOrder] = React.useState<'asc' | 'desc'>('desc');

    const fetchEmails = React.useCallback(async () => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/v1/emails/", {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setEmails(data);
            }
        } catch (err) {
            console.error("Failed to fetch emails", err);
        } finally {
            setLoading(false);
        }
    }, []);

    React.useEffect(() => {
        fetchEmails();
    }, [fetchEmails]);

    const formatTime = (dateStr: string) => {
        const date = new Date(dateStr);
        return new Intl.DateTimeFormat('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        }).format(date);
    };

    const filteredEmails = emails
        .filter(email =>
            email.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
            email.provider.toLowerCase().includes(searchQuery.toLowerCase())
        )
        .sort((a, b) => {
            const dateA = new Date(a.received_at).getTime();
            const dateB = new Date(b.received_at).getTime();
            return sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
        });

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">Emails</h1>
                    <p className="text-muted-foreground">Review processed messages from your connected accounts.</p>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" onClick={fetchEmails} disabled={loading} className="font-semibold">
                        <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </Button>
                </div>
            </div>

            <Card className="border-border/50">
                <CardContent className="p-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                            <Input
                                placeholder="Search by subject or provider..."
                                className="pl-10 h-10 border-muted"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-10 w-10"
                            onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
                        >
                            <ArrowUpDown className="w-4 h-4" />
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <div className="rounded-lg border border-border bg-card shadow-sm overflow-hidden text-sm">
                <table className="w-full text-left">
                    <thead className="bg-muted/50 text-muted-foreground font-medium border-b border-border">
                        <tr>
                            <th className="px-6 py-4">Subject</th>
                            <th className="px-6 py-4">Source</th>
                            <th className="px-6 py-4">Received At</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                        {loading ? (
                            <tr>
                                <td colSpan={4} className="px-6 py-12 text-center text-muted-foreground">
                                    <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 opacity-50" />
                                    Loading messages...
                                </td>
                            </tr>
                        ) : filteredEmails.length === 0 ? (
                            <tr>
                                <td colSpan={4} className="px-6 py-12 text-center text-muted-foreground">
                                    <Mail className="w-6 h-6 mx-auto mb-2 opacity-50" />
                                    No emails found.
                                </td>
                            </tr>
                        ) : (
                            filteredEmails.map(email => (
                                <tr key={email.id} className="hover:bg-muted/30 transition-colors group">
                                    <td className="px-6 py-4 max-w-md">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 rounded-md bg-secondary text-primary">
                                                <Mail className="w-4 h-4" />
                                            </div>
                                            <span className="font-semibold text-foreground truncate">{email.subject || '(No Subject)'}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground">
                                            <Database className="w-3 h-3" />
                                            {email.provider.toUpperCase()} (ACC-{email.connected_account_id})
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-muted-foreground">
                                        <div className="flex items-center gap-1.5 uppercase text-[10px] font-bold tracking-tight">
                                            <Calendar className="w-3 h-3" />
                                            {formatTime(email.received_at)}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <Button variant="ghost" size="sm" className="h-8 py-0">
                                            View <ExternalLink className="w-3 h-3 ml-1" />
                                        </Button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
