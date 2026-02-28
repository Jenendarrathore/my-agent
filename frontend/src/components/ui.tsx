import * as React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export { cn };

const Button = React.forwardRef<
    HTMLButtonElement,
    React.ButtonHTMLAttributes<HTMLButtonElement> & {
        variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'destructive',
        size?: 'default' | 'sm' | 'lg' | 'icon'
    }
>(({ className, variant = 'primary', size = 'default', ...props }, ref) => {
    const variants = {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
    };

    const sizes = {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
    };

    return (
        <button
            className={cn(
                "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
                variants[variant],
                sizes[size],
                className
            )}
            ref={ref}
            {...props}
        />
    );
});
Button.displayName = "Button";

const Input = React.forwardRef<
    HTMLInputElement,
    React.InputHTMLAttributes<HTMLInputElement>
>(({ className, type, ...props }, ref) => {
    return (
        <input
            type={type}
            className={cn(
                "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                className
            )}
            ref={ref}
            {...props}
        />
    );
});
Input.displayName = "Input";

const Card = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div
        className={cn(
            "rounded-lg border bg-card text-card-foreground shadow-sm",
            className
        )}
        {...props}
    />
);

const CardHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div
        className={cn("flex flex-col space-y-1.5 p-6", className)}
        {...props}
    />
);

const CardTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h3
        className={cn(
            "text-2xl font-semibold leading-none tracking-tight",
            className
        )}
        {...props}
    />
);

const CardDescription = ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
    <p
        className={cn("text-sm text-muted-foreground", className)}
        {...props}
    />
);

const CardContent = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn("p-6 pt-0", className)} {...props} />
);

const CardFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div
        className={cn("flex items-center p-6 pt-0", className)}
        {...props}
    />
);

const Badge = ({ className, variant = 'default', ...props }: React.HTMLAttributes<HTMLDivElement> & { variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'outline' }) => {
    const variants = {
        default: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        success: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-400",
        warning: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
        error: "bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-400",
        info: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
        outline: "text-foreground",
    };
    return (
        <div className={cn("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2", variant === 'outline' ? "border-border" : "border-transparent", variants[variant], className)} {...props} />
    );
};

// Simplified Toast System
interface ToastProps {
    message: string;
    type?: 'success' | 'error' | 'info';
    id: number;
}

const ToastContext = React.createContext<{
    addToast: (message: string, type?: 'success' | 'error' | 'info') => void;
}>({ addToast: () => { } });

export const useToast = () => React.useContext(ToastContext);

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
    const [toasts, setToasts] = React.useState<ToastProps[]>([]);

    const addToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
        const id = Date.now();
        setToasts((prev) => [...prev, { message, type, id }]);
        setTimeout(() => {
            setToasts((prev) => prev.filter((t) => t.id !== id));
        }, 3000);
    };

    return (
        <ToastContext.Provider value={{ addToast }}>
            {children}
            <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
                {toasts.map((toast) => (
                    <div
                        key={toast.id}
                        className={cn(
                            "min-w-[300px] p-4 rounded-lg border bg-background shadow-lg animate-in slide-in-from-right-full fade-in duration-300 pointer-events-auto",
                            toast.type === 'success' ? "border-emerald-500/50" :
                                toast.type === 'error' ? "border-rose-500/50" :
                                    "border-border"
                        )}
                    >
                        <div className="font-medium text-sm text-foreground">{toast.message}</div>
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
};

// Refined Dialog Implementation
const Dialog = ({ isOpen, onClose, title, children }: { isOpen: boolean, onClose: () => void, title: string, children: React.ReactNode }) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-in fade-in duration-300">
            <div className="bg-background border border-border rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col animate-in zoom-in-95 duration-300">
                <div className="p-6 border-b border-border flex justify-between items-center">
                    <h2 className="text-lg font-semibold text-foreground">{title}</h2>
                    <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors p-1 rounded-md hover:bg-accent">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                <div className="p-6 overflow-y-auto flex-1">
                    {children}
                </div>
                <div className="p-4 border-t border-border flex justify-end gap-2 bg-muted/50 rounded-b-lg">
                    <Button variant="outline" onClick={onClose}>Close</Button>
                </div>
            </div>
        </div>
    );
};

export { Button, Input, Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent, Badge, Dialog };
