import * as React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button, Input, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "../components/ui";
import { Eye, EyeOff, Loader2, UserPlus } from "lucide-react";

export function Register() {
    const [name, setName] = React.useState("");
    const [username, setUsername] = React.useState("");
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [showPassword, setShowPassword] = React.useState(false);
    const [error, setError] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const navigate = useNavigate();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const response = await fetch("/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    username,
                    primary_email: email,
                    password,
                }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || "Registration failed");
            }

            const data = await response.json();
            localStorage.setItem("access_token", data.access_token);

            // We might need to fetch user info after register or backend should return it
            // Let's assume user needs to login or we fetch it. 
            // Most of our routes expect 'user' in localStorage for UI display.
            // For now, let's redirect to login to be safe, or optimize later.
            navigate("/login?registered=true");
        } catch (err: any) {
            setError(err.message || "Failed to register");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-slate-50 p-4">
            <Card className="w-full max-w-md shadow-lg border-slate-200">
                <CardHeader className="space-y-1">
                    <div className="flex justify-center mb-2">
                        <div className="p-3 bg-primary/10 rounded-full">
                            <UserPlus className="w-6 h-6 text-primary" />
                        </div>
                    </div>
                    <CardTitle className="text-3xl font-bold tracking-tight text-center">Create Account</CardTitle>
                    <CardDescription className="text-center">
                        Sign up to start tracking your finances automatically
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleRegister}>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none">Full Name</label>
                            <Input
                                placeholder="John Doe"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none">Username</label>
                                <Input
                                    placeholder="johndoe"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium leading-none">Email</label>
                                <Input
                                    type="email"
                                    placeholder="john@example.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none">Password</label>
                            <div className="relative">
                                <Input
                                    type={showPassword ? "text" : "password"}
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="pr-10"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700"
                                >
                                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                </button>
                            </div>
                        </div>
                        {error && <p className="text-sm font-medium text-destructive bg-destructive/10 p-2 rounded">{error}</p>}
                    </CardContent>
                    <CardFooter className="flex flex-col space-y-4">
                        <Button className="w-full" type="submit" disabled={loading}>
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Creating account...
                                </>
                            ) : "Register"}
                        </Button>
                        <div className="text-center text-sm text-slate-500">
                            Already have an account?{" "}
                            <Link to="/login" className="text-primary font-medium hover:underline">
                                Sign In
                            </Link>
                        </div>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}
