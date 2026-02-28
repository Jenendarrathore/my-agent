import * as React from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ShieldCheck, Mail, Lock, Loader2, Eye, EyeOff } from "lucide-react";
import { Button, Input, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, useToast } from "../components/ui";

export function Login() {
    const [identifier, setIdentifier] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [isLoading, setIsLoading] = React.useState(false);
    const [showPassword, setShowPassword] = React.useState(false);
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { addToast } = useToast();

    const isRegistered = searchParams.get("registered") === "true";

    React.useEffect(() => {
        if (isRegistered) {
            addToast("Account created successfully. Please log in.", "success");
        }
    }, [isRegistered]);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const formData = new URLSearchParams();
            formData.append("username", identifier);
            formData.append("password", password);

            const res = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData,
            });

            if (res.ok) {
                const data = await res.json();
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("user", JSON.stringify(data.user));
                addToast("Authentication successful. Welcome back.", "success");
                navigate("/dashboard");
            } else {
                addToast("Invalid email or password.", "error");
            }
        } catch (err) {
            addToast("Failed to connect to authentication server.", "error");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-6">
            <div className="w-full max-w-md space-y-8 animate-in fade-in zoom-in-95 duration-500">
                <div className="flex flex-col items-center text-center space-y-2">
                    <div className="w-12 h-12 rounded-xl bg-primary flex items-center justify-center shadow-lg shadow-primary/20 mb-4">
                        <ShieldCheck className="w-7 h-7 text-primary-foreground" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight">Welcome Back</h1>
                    <p className="text-muted-foreground">Sign in to manage your automated financial agents.</p>
                </div>

                <Card className="border-border shadow-xl">
                    <CardHeader className="space-y-1">
                        <CardTitle className="text-xl">Sign In</CardTitle>
                        <CardDescription>Enter your credentials to access your secure dashboard.</CardDescription>
                    </CardHeader>
                    <form onSubmit={handleLogin}>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Email Address</label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 h-11"
                                        placeholder="user@example.com"
                                        type="email"
                                        value={identifier}
                                        onChange={(e) => setIdentifier(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Password</label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 pr-10 h-11"
                                        placeholder="••••••••"
                                        type={showPassword ? "text" : "password"}
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                                    >
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter className="flex flex-col space-y-4 pb-8">
                            <Button className="w-full h-11 font-bold tracking-tight" type="submit" disabled={isLoading}>
                                {isLoading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
                                Sign In
                            </Button>
                            <p className="text-center text-sm text-muted-foreground">
                                Don't have an account?{" "}
                                <Link to="/register" className="text-primary font-bold hover:underline underline-offset-4">
                                    Create account
                                </Link>
                            </p>
                        </CardFooter>
                    </form>
                </Card>
                <p className="text-center text-[10px] text-muted-foreground/50 uppercase tracking-[0.2em] font-medium">
                    Secure 256-bit encryption active
                </p>
            </div>
        </div>
    );
}
