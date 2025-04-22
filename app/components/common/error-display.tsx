export function ErrorDisplay({ message = "Something went wrong" }) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold">Error</h1>
            <p>{message}</p>
        </div>
    );
}