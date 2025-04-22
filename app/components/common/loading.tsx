export function Loading({ message = "Loading…" }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold">{message}</h1>
        </div>
    );
}