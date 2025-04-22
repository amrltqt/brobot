"use client";

import './globals.css'

import { cn } from "@/lib/utils"
import { TooltipProvider } from "@/components/ui/tooltip"
import { Inter } from "next/font/google"
import type { ReactNode } from "react"
import { HeaderProvider, useHeader } from "@/context/header-context";

import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { MainSidebar } from "@/components/main-sidebar"

const inter = Inter({ subsets: ["latin"] })

const Header = () => {
  const { header } = useHeader();
  return <h1 className="text-lg font-bold">{header}</h1>;
};


interface LayoutProps {
  children: ReactNode,
}

export default function Layout({ children }: LayoutProps) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="Learn with ease with Brobot" />
        <title>Brobot - the learning assistant</title>
      </head>
      <body className={cn("flex min-h-svh flex-col antialiased", inter.className)}>
        <TooltipProvider delayDuration={0}>
          <HeaderProvider>
            <SidebarProvider>
              <MainSidebar />
              <SidebarInset className="flex flex-col w-full">
                <header className="flex h-14 items-center gap-2 border-b px-4">
                  <SidebarTrigger />
                  <Header />
                </header>
                <div className="flex-grow h-full p-4">{children}</div>
              </SidebarInset>
            </SidebarProvider>
          </HeaderProvider>
        </TooltipProvider>
      </body>
    </html>
  )
}

