import './globals.css'

import { cn } from "@/lib/utils"
import { TooltipProvider } from "@/components/ui/tooltip"
import { Inter } from "next/font/google"
import type { ReactNode } from "react"
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { MainSidebar } from "@/components/main-sidebar"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "Brobot - the learning assistant",
  description: "Learn with ease with Brobot",
}

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={cn("flex min-h-svh flex-col antialiased", inter.className)}>
        <TooltipProvider delayDuration={0}>
          <SidebarProvider>
            <MainSidebar />
            <SidebarInset className="flex flex-col w-full">
              <header className="flex h-14 items-center gap-2 border-b px-4">
                <SidebarTrigger />
                <h1 className="text-lg font-semibold">What do you want to learn?</h1>
              </header>
              <div className="flex-grow h-full p-4">{children}</div>
            </SidebarInset>
          </SidebarProvider>
        </TooltipProvider>
      </body>
    </html>
  )
}

