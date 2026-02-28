import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
import { ShieldCheck, Mail, Lock, User, Loader2, ArrowRight } from "lucide-react";
import { Button, Input, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, useToast } from "../components/ui";

export function Register() {
    const [formData, setFormData] = React.useState({
        full_name: "",
        username: "",
        email: "",
        password: "",
    });
    const [isLoading, setIsLoading] = React.useState(false);
    const navigate = useNavigate();
    const { addToast } = useToast();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const res = await fetch("/api/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: formData.full_name,
                    username: formData.username,
                    primary_email: formData.email,
                    password: formData.password
                }),
            });

            if (res.ok) {
                addToast("Account created successfully.", "success");
                navigate("/login?registered=true");
            } else {
                const data = await res.json();
                addToast(data.detail || "Registration failed.", "error");
            }
        } catch (err) {
            addToast("Failed to connect to server.", "error");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-6">
            <div className="w-full max-w-xl space-y-8 animate-in fade-in zoom-in-95 duration-500">
                <div className="flex flex-col items-center text-center space-y-2">
                    <div className="w-12 h-12 rounded-xl bg-primary flex items-center justify-center shadow-lg shadow-primary/20 mb-4">
                        <ShieldCheck className="w-7 h-7 text-primary-foreground" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight">Create Your Account</h1>
                    <p className="text-muted-foreground">Start automating your financial data processing in minutes.</p>
                </div>

                <Card className="border-border shadow-xl">
                    <CardHeader className="space-y-1">
                        <CardTitle className="text-xl">Account Registration</CardTitle>
                        <CardDescription>Enter your details below to set up your secure workspace.</CardDescription>
                    </CardHeader>
                    <form onSubmit={handleRegister}>
                        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-8">
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Full Name</label>
                                <div className="relative">
                                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 h-11"
                                        placeholder="John Doe"
                                        value={formData.full_name}
                                        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Username</label>
                                <div className="relative">
                                    <ArrowRight className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 h-11"
                                        placeholder="johndoe"
                                        value={formData.username}
                                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="space-y-2 md:col-span-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Email Address</label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 h-11"
                                        placeholder="user@example.com"
                                        type="email"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="space-y-2 md:col-span-2">
                                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Secure Password</label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                    <Input
                                        className="pl-10 h-11"
                                        placeholder="••••••••"
                                        type="password"
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                        required
                                    />
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter className="flex flex-col space-y-4 pb-8">
                            <Button className="w-full h-11 font-bold tracking-tight" type="submit" disabled={isLoading}>
                                {isLoading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
                                Register Account
                            </Button>
                            <p className="text-center text-sm text-muted-foreground">
                                Already possess an account?{" "}
                                <Link to="/login" className="text-primary font-bold hover:underline underline-offset-4">
                                    Sign in instead
                                </Link>
                            </p>
                        </CardFooter>
                    </form>
                </Card>
            </div>
        </div>
    );
}
