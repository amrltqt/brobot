"use client";

import { createContext, useContext, useState } from "react";

const HeaderContext = createContext<{ setHeader: (v: React.ReactNode) => void; header: React.ReactNode | null }>({
    setHeader: () => { },
    header: null,
});

export const HeaderProvider = ({ children }: { children: React.ReactNode }) => {
    const [header, setHeader] = useState<React.ReactNode>(null);
    return (
        <HeaderContext.Provider value={{ header, setHeader }}>
            {children}
        </HeaderContext.Provider>
    );
};

export const useHeader = () => useContext(HeaderContext);