"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";

import AccountOverview from "./accountOverview";
import BotActivity from "./botActivity";
import { Card, CardContent, CardHeader, CardTitle } from "./card";
import CurrentTradeContent from "./currentTradeContent";
import StrategyStats from "./strategyStats";
import { DashboardChart } from "./dashboardChart";
import { Info } from "lucide-react";
import { getTradeDetails } from "@/app/actions/actions";
import { Skeleton } from "./skeleton";

export interface TradeDetails {
  transaction_type: string;
  order_price: number;
  pnl: number;
  qty: number;
  sl_price: number;
  tp_price: number;
  ltp: number;
  time: string;
}

export interface PnlData {
  time: string;
  pnl: number;
}

const dummyTradeDetails = {
  transaction_type: "buy",
  order_price: 15.6,
  pnl: 1.45,
  qty: 15,
  sl_price: 13.2,
  tp_price: 17.9,
  ltp: 15.2,
};

const dummyPnLData = [
  { time: "10:00:00", pnl: 50 },
  { time: "10:01:00", pnl: 30 },
  { time: "10:02:00", pnl: -20 },
  { time: "10:03:00", pnl: 40 },
  { time: "10:04:00", pnl: -50 },
  { time: "10:05:00", pnl: 80 },
  { time: "10:06:00", pnl: 100 },
  { time: "10:07:00", pnl: -10 },
  { time: "10:08:00", pnl: 60 },
  { time: "10:09:00", pnl: -30 },
  { time: "10:10:00", pnl: 20 },
  { time: "10:11:00", pnl: 90 },
  { time: "10:12:00", pnl: -70 },
  { time: "10:13:00", pnl: 30 },
  { time: "10:14:00", pnl: 50 },
  { time: "10:15:00", pnl: -40 },
];

export default function DashboardClientPage() {
  const { data: session, status } = useSession();
  const [tradeCount, setTradeCount] = useState<number>(0);
  const [todayPnl, setTodayPnl] = useState<number>(0);
  const [isLoadingTradeDetails, setIsLoadingTradeDetails] = useState(true);
  const [time, setTime] = useState<string>("");
  const [tradeDetails, setTradeDetails] = useState<TradeDetails | null>();
  const [pnlData, setPnlData] = useState<PnlData[]>([]);

  useEffect(() => {
    if (status === "loading") return; // Prevent running until session is ready

    const fn = async () => {
      // setIsLoadingTradeDetails(true);
      const data = await getTradeDetails(session?.user?.id as string);
      setTodayPnl(data ? data.pnl : 0);
      // setIsLoadingTradeDetails(false);
    };
    fn();
  }, [tradeCount]);

  useEffect(() => {
    if (status === "loading") return; // Prevent running until session is ready

    const fn = async () => {
      console.log(session?.user?.id);
      setIsLoadingTradeDetails(true);
      const data = await getTradeDetails(session?.user?.id as string);
      console.log(data);
      setTradeCount(data ? data.tradeCount : 0);
      setTodayPnl(data ? data.pnl : 0);
      setIsLoadingTradeDetails(false);
    };
    fn();
    const userId = session?.user?.id; // Get User ID from session
    if (!userId) {
      return;
    }
    // console.log(userId);
    let ws: WebSocket;
    try {
      ws = new WebSocket(`ws://127.0.0.1:8000/ws/trade-updates/${userId}`);

      ws.onopen = () => {
        console.log("Connected to WebSocket");
        localStorage.setItem("isWebsocketConnected", "1");
      };

      ws.onmessage = (event) => {
        try {
          const data: TradeDetails | null = JSON.parse(event.data);
          console.log("Received Trade Data:", data);
          // setTodayPnl(todayPnl + (data ? data.pnl : 0));
          setTime(data ? data.time : "");
          setPnlData((prevState) => {
            if (!data) return [];
            const date = new Date().toLocaleTimeString();
            return [
              ...prevState,
              { time: date, pnl: Number(data.pnl.toFixed(2)) },
            ];
          });
          setTradeDetails((td) => {
            if (!td) return data;
            if (
              td?.order_price !== data?.order_price ||
              td?.sl_price !== data?.sl_price
            ) {
              setTradeCount((prevState) => {
                console.log(`Trade Count ${prevState + 1}`);
                return prevState + 1;
              });
            }
            return data;
          });
        } catch (error) {
          console.log(`Error parsing websocket message: ${error}`);
        }
      };

      ws.onerror = (error) => {
        console.log("WebSocket error:" + error);
      };

      ws.onclose = () => {
        console.log("WebSocket connection closed");
        localStorage.setItem("isWebsocketConnected", "0");
      };
    } catch (error) {
      console.error(`Error establishing connection with websocket ${error}`);
    }
    return () => {
      try {
        if (ws && ws.readyState === WebSocket.OPEN) {
          console.log(
            `Closing WebSocket connection... ReadyState: ${ws.readyState}`
          );
          ws.close();
        }
      } catch (error) {
        console.error(`Error closing websocker ${error}`);
      }
    };
  }, [session?.user?.id]);

  return (
    <>
      <div className="flex flex-col h-full p-10">
        <div className="h-10 mb-5 flex items-center space-x-10">
          <div className="border rounded-lg p-2 space-x-2 flex items-center min-w-36">
            <div className="font-bold text-sm">Trade Count:</div>
            {isLoadingTradeDetails ? (
              <Skeleton className="h-5 w-8 rounded" />
            ) : (
              <div className="text-primary">{tradeCount}</div>
            )}
          </div>
          <div className="border rounded-lg p-2 space-x-2 flex items-center min-w-48">
            <div className="font-bold text-sm ">Today's PnL:</div>
            {isLoadingTradeDetails ? (
              <Skeleton className="h-5 w-20 rounded" />
            ) : (
              <div className="text-primary">{todayPnl.toFixed(2)}</div>
            )}
          </div>
        </div>
        <div className="flex h-full items-center">
          <DashboardChart pnlData={pnlData} time={time} stockName="Reliance" />
          {/* <Card className="grow mr-5">
        <DashboardChart />
      </Card> */}
          <Card className="w-80 h-96">
            {tradeDetails ? (
              <CurrentTradeContent {...tradeDetails} />
            ) : (
              <NotInTradeComponent />
            )}
          </Card>
        </div>
      </div>
    </>
  );
}

export function NotInTradeComponent() {
  return (
    <div className="flex justify-center items-center flex-col h-full w-full rounded-lg bg-secondary text-muted-foreground">
      <Info />
      <div>Currently not in trade</div>
    </div>
  );
}
