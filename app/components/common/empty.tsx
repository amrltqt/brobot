export function Empty({ message = "No items found" }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold text-muted-foreground">{message}</h1>
        </div>
    );
}