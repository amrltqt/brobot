import { SessionMessageDTO } from "@/models/session";

export function sortMessagesByDate(
    messages: SessionMessageDTO[]
): SessionMessageDTO[] {
    return [...messages].sort(
        (a, b) =>
            new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    );
}

/**
 * Insère ou remplace un message dans la liste, puis trie par date.
 */
export function upsertAndSortMessages(
    messages: SessionMessageDTO[],
    newMsg: SessionMessageDTO
): SessionMessageDTO[] {
    const idx = messages.findIndex((m) => m.id === newMsg.id);
    const updated =
        idx >= 0
            ? // remplace l’ancien
            [...messages.slice(0, idx), newMsg, ...messages.slice(idx + 1)]
            : // ajoute en fin
            [...messages, newMsg];

    return sortMessagesByDate(updated);
}