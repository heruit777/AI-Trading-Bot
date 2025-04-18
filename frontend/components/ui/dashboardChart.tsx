"use client";

import { TrendingUp } from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { Tooltip } from "@radix-ui/react-tooltip";
import { NotInTradeComponent, PnlData } from "./dashboardClientPage";

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

const chartConfig = {
  positive: {
    color: "hsl(var(--chart-2))", // 2 for green and 5 for red
  },
  negative: {
    color: "hsl(var(--chart-5))",
  },
} satisfies ChartConfig;

export function DashboardChart({
  pnlData,
  time,
  stockName,
}: {
  pnlData: PnlData[];
  time: string;
  stockName: string;
}) {
  const gradientOffset = () => {
    const dataMax = Math.max(...pnlData.map((i) => i.pnl));
    const dataMin = Math.min(...pnlData.map((i) => i.pnl));

    if (dataMax <= 0) {
      return 0;
    }
    if (dataMin >= 0) {
      return 1;
    }

    return dataMax / (dataMax - dataMin);
  };
  const off = gradientOffset();
  return (
    <Card className="grow mr-5 h-full">
      {pnlData.length <= 0 ? (
        <NotInTradeComponent />
      ) : (
        <CardHeader className="h-96">
          <CardTitle>PnL Chart - Current Trade</CardTitle>
          <CardDescription>
            Trade executed at {time} on {stockName}
          </CardDescription>
          <CardContent>
            <ChartContainer config={chartConfig}>
              <AreaChart accessibilityLayer data={pnlData}>
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="time"
                  tickLine={true}
                  axisLine={false}
                  tickMargin={8}
                  //   tickFormatter={(value) => value.slice(0, 3)}
                />
                <YAxis tickLine={false} axisLine={false} tickMargin={8} />
                <ChartTooltip cursor={true} content={<ChartTooltipContent />} />
                <defs>
                  <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                    <stop
                      offset={off}
                      stopColor="var(--color-positive)"
                      stopOpacity={1}
                    />
                    <stop
                      offset={off}
                      stopColor="var(--color-negative)"
                      stopOpacity={1}
                    />
                  </linearGradient>
                </defs>
                <Area
                  dataKey="pnl"
                  type="monotone"
                  fill="url(#splitColor)"
                  fillOpacity={0.4}
                  stroke="url(#splitColor)"
                  stackId="a"
                />
              </AreaChart>
            </ChartContainer>
          </CardContent>
        </CardHeader>
      )}
    </Card>
  );
}
