"use client";
import { ScrollArea } from "./scroll-area"; // Assuming this is the correct path
import { useEffect, useState } from "react";

function getDateTime() {
  const date = new Date();
  const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;
  const formattedTime = `${date.getHours().toString().padStart(2, "0")}:${date
    .getMinutes()
    .toString()
    .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
  const dateTimeString = `${formattedDate} ${formattedTime}`;
  return dateTimeString;
}

export default function BotActivity() {
  const [logs, setLogs] = useState<{ date: string; msg: string }[]>([]);


  function updateLogs() {
    setLogs((prevLogs) => [
      ...prevLogs,
      { date: getDateTime(), msg: "Finding Trades" },
    ]);
  }

  useEffect(() => {
    // Initialize with the first log entry
    setLogs([{ date: getDateTime(), msg: "Bot initialized" }]);

    const intervalId = setInterval(() => {
      updateLogs();
    }, 2000);

    return () => clearInterval(intervalId);
  }, []);


  return (
    <div className="h-72 w-full rounded-md border p-4 bg-black overflow-y-auto">
        <ScrollArea className="w-full h-full overflow-y-auto">
          {logs.map((log) => (
            <Log key={log.date}>
              {log.date}: {log.msg}
            </Log>
          ))}
      </ScrollArea>
    </div>
  );
}

function Log({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full px-2 hover:bg-gray-900 hover:cursor-pointer p-2 font-mono text-sm">
      {children}
    </div>
  );
}
