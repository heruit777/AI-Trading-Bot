"use client";

import { useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import TradeInfoSkeleton from "./skeletons/tradeInfoSkeleton";

interface TradeDetails {
  transaction_type: string;
  order_price: number;
  pnl: number;
  qty: number;
  sl_price: number;
  tp_price: number;
}

export default function CurrentTradeContent() {
  const { data: session, status, update } = useSession();
  const [isLoading, setIsLoading] = useState<Boolean>(true);
  const [tradeDetails, setTradeDetails] = useState<TradeDetails>();

  useEffect(() => {
    update();
    const userId = session?.user?.id; // Get User ID from session
    if (!userId) {
      return;
    }
    console.log(userId);
    let ws: WebSocket;
    try {
      ws = new WebSocket(`ws://127.0.0.1:8000/ws/trade-updates/${userId}`);

      ws.onopen = () => {
        console.log("Connected to WebSocket");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Received Trade Data:", data);
          setTradeDetails(data as TradeDetails);
          setIsLoading(false);
        } catch (error) {
          console.log(`Error parsing websocket message: ${error}`);
        }
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:" + error);
      };

      ws.onclose = () => {
        console.log("WebSocket connection closed");
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
      {isLoading ? (
        <TradeInfoSkeleton />
      ) : (
        <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
          <div>Trade Qty: {tradeDetails?.qty}</div>
          <div>Trade Type: {tradeDetails?.transaction_type}</div>
          <div>Entry Price: {tradeDetails?.order_price}</div>
          <div>Stop Loss: {tradeDetails?.sl_price}</div>
          <div>Target: {tradeDetails?.tp_price}</div>
          <div>PnL: {tradeDetails?.pnl.toFixed(2)}</div>
        </div>
      )}
    </>
  );
}
