"use client";

import React from "react";
import styles from "./BouncingDots.module.css";

interface BouncingDotsProps {
    dotCount?: number;
    size?: number;
    delay?: number;
}

export function BouncingDots({
    dotCount = 3,
    size = 8,
    delay = 0.2,
}: BouncingDotsProps) {
    return (
        <span className={styles.wrapper}>
            {Array.from({ length: dotCount }).map((_, i) => (
                <span
                    key={i}
                    className={styles.dot}
                    style={{
                        width: size,
                        height: size,
                        animationDelay: `${i * delay}s`,
                    }}
                />
            ))}
        </span>
    );
}