import BotActivity from "./botActivity";
import { Card, CardContent, CardHeader, CardTitle } from "./card";

export default function DashboardPage() {
  return (
    <div className="grid grid-rows-3 grid-cols-3 gap-4 h-full p-10">
      <Card className="bg-secondary rounded-lg my-auto h-fit">
        <div className="text-lg font-bold px-6 py-4">Account Overview</div>
        <CardContent>
          <AccountOverview />
        </CardContent>
      </Card>
      <Card className="bg-secondary rounded-lg my-auto h-fit">
        <div className="text-lg font-bold px-6 py-4">Strategy Statistics</div>
        <CardContent>
          <StrategyStats />
        </CardContent>
      </Card>
      <Card className="bg-secondary rounded-lg">
        <div className="text-lg font-bold px-6 py-4">Current Trade Details</div>
        <CardContent>
          <CurrentTradeContent />
        </CardContent>
      </Card>
      <Card className="col-span-3 row-span-2 bg-secondary">
        <CardHeader>
          <CardTitle>Bot Activity Logger</CardTitle>
        </CardHeader>
        <CardContent>
          <BotActivity />
        </CardContent>
      </Card>
    </div>
  );
}

function AccountOverview() {
  return (
    <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
      <div>Balance: 10,000</div>
      <div>Number of trades: 5</div>
      <div>Daily P&L: 100</div>
      <div>Monthly P&L: 5000</div>
    </div>
  );
}

function StrategyStats() {
  return (
    <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
      <div>Win Rate: 53.36%</div>
      <div>Profit factor: 2.0</div>
      <div>Average Winner: 500</div>
      <div>Average Loser: 100</div>
      <div>Winning Streak: 5</div>
      <div>Losing Streak: 2</div>
    </div>
  );
}

function CurrentTradeContent() {
  return (
    <div className="grid grid-rows-3 grid-cols-2 text-gray-300 font-semibold gap-4">
      <div>Trade Qty: 5</div>
      <div>Trade Type: Long</div>
      <div>Entry Price: ₹100</div>
      <div>Stop Loss: ₹80</div>
      <div>Target: ₹140</div>
    </div>
  );
}
