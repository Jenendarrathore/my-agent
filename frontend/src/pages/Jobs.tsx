import * as React from "react";
import {
    RefreshCw,
    Search,
    Filter,
    ChevronRight,
    CheckCircle2,
    XCircle,
    Clock,
    AlertCircle,
    Info,
    ArrowUpDown,
    Database,
    Fingerprint
} from "lucide-react";
import {
    Button,
    Input,
    Card,
    CardContent,
    Badge,
    Dialog,
    useToast
} from "../components/ui";

interface Job {
    id: number;
    job_type: string;
    status: string;
    triggered_by: string;
    input_payload: any;
    output_payload: any;
    error_payload: any;
    user_id: number | null;
    retry_count: number;
    started_at: string | null;
    finished_at: string | null;
    created_at: string;
}

export function Jobs() {
    const [jobs, setJobs] = React.useState<Job[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [filterStatus, setFilterStatus] = React.useState<string>("all");
    const [searchQuery, setSearchQuery] = React.useState("");
    const [sortOrder, setSortOrder] = React.useState<'asc' | 'desc'>('desc');
    const [selectedJob, setSelectedJob] = React.useState<Job | null>(null);
    const [user, setUser] = React.useState<any>(null);
    const { addToast } = useToast();

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

    const isAdmin = user?.role?.name === "admin";

    const fetchJobs = React.useCallback(async () => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/v1/jobs/", {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setJobs(data);
            }
        } catch (err) {
            console.error("Failed to fetch jobs", err);
        } finally {
            setLoading(false);
        }
    }, []);

    React.useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 5000);
        return () => clearInterval(interval);
    }, [fetchJobs]);

    const handleSync = async () => {
        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/v1/jobs/sync", {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                addToast("Job synchronization initiated.", "success");
                fetchJobs();
            }
        } catch (err) {
            addToast("Failed to initiate sync.", "error");
        }
    };

    const getStatusIcon = (status: string) => {
        const s = status.toLowerCase();
        if (s === 'success' || s === 'completed') return <CheckCircle2 className="w-4 h-4 text-emerald-500" />;
        if (s === 'failed' || s === 'error') return <XCircle className="w-4 h-4 text-rose-500" />;
        if (s === 'running') return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
        return <Clock className="w-4 h-4 text-slate-400" />;
    };

    const getStatusBadge = (status: string) => {
        const s = status.toLowerCase();
        if (s === 'success' || s === 'completed') return <Badge variant="success">Completed</Badge>;
        if (s === 'failed' || s === 'error') return <Badge variant="error">Failed</Badge>;
        if (s === 'running') return <Badge variant="info">Running</Badge>;
        return <Badge variant="default">{status}</Badge>;
    };

    const formatJobType = (type: string) => {
        return type
            .replace(/([A-Z])/g, ' $1')
            .replace(/_/g, ' ')
            .replace(/^Job/, '')
            .replace(/Job$/, '')
            .trim()
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    };

    const formatTime = (dateStr: string) => {
        const date = new Date(dateStr);
        return new Intl.DateTimeFormat('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        }).format(date);
    };

    const getAccountId = (job: Job) => {
        const payload = job.input_payload || {};
        return payload.account_id || payload.connected_account_id || null;
    };

    const filteredJobs = jobs
        .filter(job => filterStatus === "all" || job.status.toLowerCase() === filterStatus.toLowerCase())
        .filter(job =>
            job.job_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (job.error_payload && JSON.stringify(job.error_payload).toLowerCase().includes(searchQuery.toLowerCase()))
        )
        .sort((a, b) => {
            const dateA = new Date(a.created_at).getTime();
            const dateB = new Date(b.created_at).getTime();
            return sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
        });

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">Background Jobs</h1>
                    <p className="text-muted-foreground">Monitor and manage asynchronous operations and data processing.</p>
                </div>
                <div className="flex items-center gap-2">
                    <Button onClick={handleSync} className="font-semibold px-6">
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Run Sync Jobs
                    </Button>
                </div>
            </div>

            <Card className="border-border/50">
                <CardContent className="p-4">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                            <Input
                                placeholder="Search jobs by type or error..."
                                className="pl-10 h-10 border-muted"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="flex items-center gap-2 border border-input rounded-md px-3 h-10 bg-background">
                                <Filter className="w-3.5 h-3.5 text-muted-foreground" />
                                <select
                                    className="bg-transparent text-sm font-medium focus:outline-none cursor-pointer"
                                    value={filterStatus}
                                    onChange={(e) => setFilterStatus(e.target.value)}
                                >
                                    <option value="all">All Statuses</option>
                                    <option value="pending">Pending</option>
                                    <option value="running">Running</option>
                                    <option value="success">Success</option>
                                    <option value="failed">Failed</option>
                                </select>
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
                    </div>
                </CardContent>
            </Card>

            <div className="rounded-lg border border-border bg-card shadow-sm overflow-hidden">
                <table className="w-full text-left text-sm">
                    <thead className="bg-muted/50 text-muted-foreground font-medium border-b border-border">
                        <tr>
                            <th className="px-6 py-4">Job Reference</th>
                            <th className="px-6 py-4">Status</th>
                            {isAdmin && <th className="px-6 py-4">User</th>}
                            <th className="px-6 py-4">Execution Time</th>
                            <th className="px-6 py-4">Source ID</th>
                            <th className="px-6 py-4 text-right">Operations</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                        {loading ? (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                                    <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 opacity-50" />
                                    <span className="text-xs uppercase tracking-wider font-semibold">Loading job history...</span>
                                </td>
                            </tr>
                        ) : filteredJobs.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                                    <Info className="w-6 h-6 mx-auto mb-2 opacity-50" />
                                    No records found matching your criteria.
                                </td>
                            </tr>
                        ) : (
                            filteredJobs.map(job => {
                                const accountId = getAccountId(job);
                                return (
                                    <tr key={job.id} className="hover:bg-muted/30 transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="p-2 rounded-md bg-secondary text-primary">
                                                    <Fingerprint className="w-4 h-4" />
                                                </div>
                                                <div className="flex flex-col">
                                                    <span className="font-semibold text-foreground">{formatJobType(job.job_type)}</span>
                                                    <span className="text-[10px] text-muted-foreground font-mono">#{job.id}</span>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                {getStatusIcon(job.status)}
                                                {getStatusBadge(job.status)}
                                            </div>
                                        </td>
                                        {isAdmin && (
                                            <td className="px-6 py-4">
                                                <Badge variant="outline" className="font-mono text-[10px]">USR-{job.user_id || 'SYS'}</Badge>
                                            </td>
                                        )}
                                        <td className="px-6 py-4 text-muted-foreground font-medium">
                                            {formatTime(job.created_at)}
                                        </td>
                                        <td className="px-6 py-4">
                                            {accountId ? (
                                                <div className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground">
                                                    <Database className="w-3 h-3" />
                                                    ACC-{accountId}
                                                </div>
                                            ) : (
                                                <span className="text-muted-foreground text-xs italic">System</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => setSelectedJob(job)}
                                                className="font-semibold text-xs h-8"
                                            >
                                                Inspect <ChevronRight className="w-3 h-3 ml-1" />
                                            </Button>
                                        </td>
                                    </tr>
                                );
                            })
                        )}
                    </tbody>
                </table>
            </div>

            <Dialog
                isOpen={!!selectedJob}
                onClose={() => setSelectedJob(null)}
                title={`Job Inspector [ID:${selectedJob?.id}]`}
            >
                {selectedJob && (
                    <div className="space-y-6">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Type</label>
                                <div className="p-2 rounded-md bg-muted/50 border border-border text-sm font-semibold">
                                    {selectedJob.job_type}
                                </div>
                            </div>
                            <div className="space-y-1">
                                <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Status</label>
                                <div className="flex items-center gap-2 p-2 rounded-md bg-muted/50 border border-border">
                                    {getStatusIcon(selectedJob.status)}
                                    <span className="text-sm font-semibold capitalize">{selectedJob.status}</span>
                                </div>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Created</label>
                                <div className="flex items-center gap-2 p-2 rounded-md bg-muted/50 border border-border text-xs font-medium">
                                    <Clock className="w-3 h-3" />
                                    {new Date(selectedJob.created_at).toLocaleString()}
                                </div>
                            </div>
                            <div className="space-y-1">
                                <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Retry Count</label>
                                <div className="flex items-center gap-2 p-2 rounded-md bg-muted/50 border border-border text-xs font-medium">
                                    <RefreshCw className="w-3 h-3" />
                                    {selectedJob.retry_count}
                                </div>
                            </div>
                        </div>

                        {selectedJob.error_payload && (
                            <div className="p-4 rounded-md bg-rose-50 border border-rose-100 dark:bg-rose-900/10 dark:border-rose-900/30 text-rose-700 dark:text-rose-400 space-y-2">
                                <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider">
                                    <AlertCircle className="w-4 h-4" />
                                    Error Details
                                </div>
                                <div className="p-4 rounded-md bg-slate-900 text-rose-400 font-mono text-[11px] overflow-auto max-h-48 border border-border shadow-inner">
                                    <pre>{JSON.stringify(selectedJob.error_payload, null, 2)}</pre>
                                </div>
                            </div>
                        )}

                        <div className="space-y-3">
                            <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Input Parameters</label>
                            <div className="p-4 rounded-md bg-slate-900 text-slate-300 font-mono text-[11px] overflow-auto max-h-48 border border-border shadow-inner">
                                <pre>{JSON.stringify(selectedJob.input_payload, null, 2)}</pre>
                            </div>
                        </div>

                        {selectedJob.output_payload && (
                            <div className="space-y-3">
                                <label className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Output Results</label>
                                <div className="p-4 rounded-md bg-slate-900 text-emerald-400 font-mono text-[11px] overflow-auto max-h-48 border border-border shadow-inner">
                                    <pre>{JSON.stringify(selectedJob.output_payload, null, 2)}</pre>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </Dialog>
        </div>
    );
}
