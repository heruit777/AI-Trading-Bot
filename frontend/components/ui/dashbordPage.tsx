import AccountOverview from "./accountOverview";
import BotActivity from "./botActivity";
import { Card, CardContent, CardHeader, CardTitle } from "./card";
import CurrentTradeContent from "./currentTradeContent";
import StrategyStats from "./strategyStats";

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
      {/* <Card className="col-span-3 row-span-2 bg-secondary">
        <CardHeader>
          <CardTitle>Bot Activity Logger</CardTitle>
        </CardHeader>
        <CardContent>
          <BotActivity />
        </CardContent>
      </Card> */}
    </div>
  );
}
