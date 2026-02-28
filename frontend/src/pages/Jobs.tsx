import * as React from "react";
import {
    Activity,
    Search,
    Filter,
    Calendar,
    Clock,
    CheckCircle2,
    XCircle,
    AlertCircle,
    RotateCcw,
    Eye,
    ArrowUpDown
} from "lucide-react";
import {
    Card,
    CardHeader,
    CardContent,
    Badge,
    Button,
    Input,
    Dialog,
    cn
} from "../components/ui";

interface Job {
    id: number;
    job_type: string;
    status: string;
    triggered_by: string;
    input_payload: any;
    output_payload: any;
    error_payload: any;
    retry_count: number;
    started_at: string | null;
    finished_at: string | null;
    created_at: string;
}

export function Jobs() {
    const [jobs, setJobs] = React.useState<Job[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [filterStatus, setFilterStatus] = React.useState<string>("");
    const [filterType, setFilterType] = React.useState<string>("");
    const [selectedJob, setSelectedJob] = React.useState<Job | null>(null);
    const [sortField, setSortField] = React.useState<keyof Job>("created_at");
    const [sortOrder, setSortOrder] = React.useState<"asc" | "desc">("desc");

    const fetchJobs = React.useCallback(async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("access_token");
            let url = `/api/v1/jobs/?limit=50`;
            if (filterStatus) url += `&status=${filterStatus}`;
            if (filterType) url += `&job_type=${filterType}`;

            const res = await fetch(url, {
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await res.json();
            setJobs(data);
        } catch (err) {
            console.error("Failed to fetch jobs", err);
        } finally {
            setLoading(false);
        }
    }, [filterStatus, filterType]);

    React.useEffect(() => {
        fetchJobs();
    }, [fetchJobs]);

    const handleSort = (field: keyof Job) => {
        if (sortField === field) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortField(field);
            setSortOrder("desc");
        }
    };

    const sortedJobs = [...jobs].sort((a, b) => {
        const valA = a[sortField];
        const valB = b[sortField];

        if (valA === null) return 1;
        if (valB === null) return -1;

        if (valA < valB) return sortOrder === "asc" ? -1 : 1;
        if (valA > valB) return sortOrder === "asc" ? 1 : -1;
        return 0;
    });

    const getStatusVariant = (status: string) => {
        switch (status) {
            case "SUCCESS": return "success";
            case "FAILED": return "error";
            case "RUNNING": return "info";
            case "QUEUED": return "warning";
            default: return "default";
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "SUCCESS": return <CheckCircle2 className="w-3.5 h-3.5 mr-1" />;
            case "FAILED": return <XCircle className="w-3.5 h-3.5 mr-1" />;
            case "RUNNING": return <Activity className="w-3.5 h-3.5 mr-1 animate-spin" />;
            case "QUEUED": return <Clock className="w-3.5 h-3.5 mr-1" />;
            default: return <AlertCircle className="w-3.5 h-3.5 mr-1" />;
        }
    };

    const formatDate = (dateStr: string | null) => {
        if (!dateStr) return "N/A";
        return new Date(dateStr).toLocaleString();
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex justify-between items-end">
                <div className="space-y-2">
                    <h1 className="text-4xl font-bold tracking-tight text-slate-900 italic">Job Management</h1>
                    <p className="text-slate-500 text-lg">Monitor and audit background tasks.</p>
                </div>
                <Button onClick={fetchJobs} variant="outline" size="sm" className="h-10">
                    <RotateCcw className={cn("w-4 h-4 mr-2", loading && "animate-spin")} />
                    Refresh
                </Button>
            </div>

            <Card className="border-slate-200/60 shadow-xl shadow-slate-200/20 bg-white/50 backdrop-blur-sm overflow-hidden">
                <CardHeader className="border-b border-slate-100 bg-slate-50/50">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div className="flex items-center gap-4 flex-1">
                            <div className="relative flex-1 max-w-sm">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                <Input
                                    placeholder="Search jobs..."
                                    className="pl-10 bg-white border-slate-200 focus:ring-primary/20"
                                />
                            </div>
                            <div className="flex items-center gap-2">
                                <Filter className="w-4 h-4 text-slate-400" />
                                <select
                                    className="bg-white border border-slate-200 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                                    value={filterStatus}
                                    onChange={(e) => setFilterStatus(e.target.value)}
                                >
                                    <option value="">All Statuses</option>
                                    <option value="SUCCESS">Success</option>
                                    <option value="FAILED">Failed</option>
                                    <option value="RUNNING">Running</option>
                                    <option value="QUEUED">Queued</option>
                                </select>
                                <select
                                    className="bg-white border border-slate-200 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                                    value={filterType}
                                    onChange={(e) => setFilterType(e.target.value)}
                                >
                                    <option value="">All Types</option>
                                    <option value="run_email_fetch">Email Fetch</option>
                                    <option value="run_email_extraction">Email Extraction</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="border-b border-slate-100 bg-slate-50/30">
                                    <th
                                        className="px-6 py-4 text-sm font-bold text-slate-600 cursor-pointer hover:text-primary transition-colors"
                                        onClick={() => handleSort("id")}
                                    >
                                        <div className="flex items-center">
                                            ID <ArrowUpDown className="w-3 h-3 ml-2 opacity-50" />
                                        </div>
                                    </th>
                                    <th
                                        className="px-6 py-4 text-sm font-bold text-slate-600 cursor-pointer hover:text-primary transition-colors"
                                        onClick={() => handleSort("job_type")}
                                    >
                                        <div className="flex items-center">
                                            Job Type <ArrowUpDown className="w-3 h-3 ml-2 opacity-50" />
                                        </div>
                                    </th>
                                    <th className="px-6 py-4 text-sm font-bold text-slate-600">Status</th>
                                    <th
                                        className="px-6 py-4 text-sm font-bold text-slate-600 cursor-pointer hover:text-primary transition-colors"
                                        onClick={() => handleSort("created_at")}
                                    >
                                        <div className="flex items-center">
                                            Triggered <ArrowUpDown className="w-3 h-3 ml-2 opacity-50" />
                                        </div>
                                    </th>
                                    <th className="px-6 py-4 text-sm font-bold text-slate-600">Duration</th>
                                    <th className="px-6 py-4 text-sm font-bold text-slate-600 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {loading && jobs.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                                            <div className="flex flex-col items-center gap-2">
                                                <Activity className="w-8 h-8 animate-spin text-primary/40" />
                                                <p>Loading jobs...</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : sortedJobs.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                                            <div className="flex flex-col items-center gap-2">
                                                <AlertCircle className="w-8 h-8 text-slate-300" />
                                                <p>No jobs found.</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : (
                                    sortedJobs.map((job) => (
                                        <tr key={job.id} className="hover:bg-slate-50/50 transition-colors group">
                                            <td className="px-6 py-4 text-sm font-medium text-slate-900">#{job.id}</td>
                                            <td className="px-6 py-4 text-sm text-slate-600">
                                                <code className="bg-slate-100 px-2 py-1 rounded text-xs font-mono">
                                                    {job.job_type}
                                                </code>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Badge variant={getStatusVariant(job.status)} className="font-bold">
                                                    {getStatusIcon(job.status)}
                                                    {job.status}
                                                </Badge>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-slate-500">
                                                <div className="flex flex-col">
                                                    <span className="flex items-center gap-1.5">
                                                        <Calendar className="w-3 h-3" />
                                                        {formatDate(job.created_at)}
                                                    </span>
                                                    <span className="text-xs text-slate-400 mt-1 italic">
                                                        by {job.triggered_by}
                                                    </span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-slate-500">
                                                {job.started_at && job.finished_at ? (
                                                    <span className="flex items-center gap-1.5">
                                                        <Clock className="w-3 h-3" />
                                                        {Math.round((new Date(job.finished_at).getTime() - new Date(job.started_at).getTime()) / 1000)}s
                                                    </span>
                                                ) : job.started_at ? (
                                                    <span className="text-blue-500 animate-pulse">Running...</span>
                                                ) : "N/A"}
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => setSelectedJob(job)}
                                                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                                                >
                                                    <Eye className="w-4 h-4 mr-2" />
                                                    View Details
                                                </Button>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>

            <Dialog
                isOpen={!!selectedJob}
                onClose={() => setSelectedJob(null)}
                title={`Job Details: #${selectedJob?.id}`}
            >
                {selectedJob && (
                    <div className="space-y-6">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Type</label>
                                <p className="text-sm font-semibold">{selectedJob.job_type}</p>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Trigger</label>
                                <p className="text-sm font-semibold">{selectedJob.triggered_by}</p>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Created</label>
                                <p className="text-sm">{formatDate(selectedJob.created_at)}</p>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Status</label>
                                <div>
                                    <Badge variant={getStatusVariant(selectedJob.status)}>
                                        {selectedJob.status}
                                    </Badge>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Input Payload</label>
                            <pre className="bg-slate-900 text-slate-50 p-4 rounded-lg text-xs overflow-x-auto font-mono">
                                {JSON.stringify(selectedJob.input_payload, null, 2)}
                            </pre>
                        </div>

                        {selectedJob.output_payload && (
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Output Result</label>
                                <pre className="bg-slate-900 text-blue-300 p-4 rounded-lg text-xs overflow-x-auto font-mono">
                                    {JSON.stringify(selectedJob.output_payload, null, 2)}
                                </pre>
                            </div>
                        )}

                        {selectedJob.error_payload && (
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider text-red-400">Error Payload</label>
                                <pre className="bg-red-950 text-red-200 p-4 rounded-lg text-xs overflow-x-auto font-mono border border-red-900">
                                    {JSON.stringify(selectedJob.error_payload, null, 2)}
                                </pre>
                            </div>
                        )}
                    </div>
                )}
            </Dialog>
        </div>
    );
}
