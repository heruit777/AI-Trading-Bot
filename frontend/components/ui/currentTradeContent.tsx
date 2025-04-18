import { CardContent, CardHeader } from "./card";
import { TradeDetails } from "./dashboardClientPage";

export default function CurrentTradeContent({
  transaction_type,
  order_price,
  pnl,
  qty,
  sl_price,
  tp_price,
}: TradeDetails) {
  return (
    <>
      <CardHeader className="font-bold">Current Trade Details</CardHeader>
      <hr />
      <CardContent className="flex flex-col text-primary space-y-2 mt-5">
        <div className="space-x-2">
          <span className="font-bold">Stock Name:</span>
          <span className="text-primary">Reliance</span>
        </div>
        <div className="space-x-2">
          <span className="font-bold">Trade Qty:</span>
          <span className="text-primary">{qty}</span>
        </div>
        <div className="space-x-2">
          <span className="font-bold">Trade Type:</span>
          <span className="text-primary">{transaction_type}</span>
        </div>
        <div className="space-x-2">
          <span className="font-bold">Entry Price:</span>
          <span className="text-primary">{order_price}</span>
        </div>
        <div className="space-x-2">
          <span className="font-bold">Stop Loss:</span>
          <span className="text-primary">{sl_price}</span>
        </div>
        <div className="space-x-2">
          <span className="font-bold">Target:</span>
          <span className="text-primary">{tp_price}</span>
        </div>
        <div className="space-x-2">
          <span>PnL:</span>
          <span
            className={`font-bold ${
              pnl < 0 ? "text-red-400" : "text-green-400"
            }`}
          >
            {pnl.toFixed(2)}
          </span>
        </div>
      </CardContent>
    </>
  );
}
