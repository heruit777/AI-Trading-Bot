"use server";
import { prisma } from "@/prisma/prisma";
import { auth } from "@/auth";

export async function fetchBroker() {
  try {
    // Fetch the logged-in user
    const session = await auth(); // Make sure auth function is set up to get the session
    if (!session || !session.user?.id) {
      throw new Error("User is not authenticated");
    }

    const userId = session.user.id; // Ensure user ID is fetched from session

    // Check if broker already exists for this user
    const existingBroker = await prisma.broker.findUnique({
      where: { userId },
    });

    if (!existingBroker) return null;
    // console.log(existingBroker);
    return existingBroker;
  } catch (error) {
    console.error("Error fetching broker:", error);
    throw error;
  }
}

export async function createBroker({
  brokerType,
  balance,
  accessToken,
  apiKey,
  apiSecret,
}: {
  brokerType: string;
  balance?: number | undefined;
  accessToken?: string | undefined;
  apiKey?: string | undefined;
  apiSecret?: string | undefined;
}) {
  try {
    // Fetch the logged-in user
    const session = await auth(); // Make sure auth function is set up to get the session
    if (!session || !session.user?.id) {
      throw new Error("User is not authenticated");
    }

    const userId = session.user.id; // Ensure user ID is fetched from session
    // console.log(brokerType, accessToken, apiVersion, apiKey, apiSecret);
    // Check if broker already exists for this user
    // Validate the input data (ensure none of the values are null or undefined)
    // if (!brokerType || !accessToken || !apiVersion || !apiKey || !apiSecret) {
    //   throw new Error(
    //     "Missing required fields: brokerType, accessToken, apiVersion, apiKey, or apiSecret"
    //   );
    // }

    const existingBroker = await prisma.broker.findUnique({
      where: { userId },
    });

    if (existingBroker) {
      // Update existing broker
      console.log(
        "Exisint user issue",
        brokerType,
        typeof accessToken,
        typeof balance,
        typeof apiKey,
        typeof apiSecret
      );
      return await prisma.broker.update({
        where: { userId },
        data: {
          broker_type: brokerType,
          access_token: accessToken,
          balance: balance,
          api_version: "2.0",
          api_key: apiKey,
          api_secret: apiSecret,
        },
      });
    } else {
      // Create new broker
      return await prisma.broker.create({
        data: {
          userId,
          broker_type: brokerType,
          access_token: accessToken,
          balance: balance,
          api_version: "2.0",
          api_key: apiKey,
          api_secret: apiSecret,
        },
      });
    }
  } catch (error) {
    console.error("Error creating/updating broker:", error);
    throw error;
  }
}

export async function getTradeDetails(userId: string) {
  try {
    if (!userId) return { pnl: 0, tradeCount: 0 };
    const todayMidnight = new Date();
    todayMidnight.setUTCHours(0, 0, 0, 0);

    const userWithTrades = await prisma.broker.findUnique({
      where: { userId },
      include: { trades: { where: { createdAt: { gte: todayMidnight } } } },
    });

    if (!userWithTrades || userWithTrades.trades.length === 0) return { pnl: 0, tradeCount: 0 };

    const pnl = userWithTrades.trades.reduce((acc, cur) => {
      return acc + cur.pnl;
    }, 0);
    const tradeCount = userWithTrades.trades.length;
    return { pnl, tradeCount };
  } catch (error) {
    console.log(error);
  }
}

// {
//   id: 6,
//   date: "2025-01-19",
//   stock: "TSLA",
//   type: "Sell",
//   quantity: 5,
//   entryPrice: 700.0,
//   exitPrice: 690.0,
//   pnl: "-50.00",
// },
interface TradeHistory {
  id: string;
  data: string;
  stock: string;
  type: string;
  quantity: number;
  entryPrice: number;
  exitPrice: number;
  pnl: number;
}
export async function getTradeHistory(userId: string) {
  try {
    // await new Promise(res => setTimeout(res, 3000));
    const userWithTrades = await prisma.broker.findUnique({
      where: { userId },
      include: { trades: {orderBy: {createdAt: 'desc'}} },
    });
    if (!userWithTrades) return [];
    // const data: TradeHistory[] = []
    return userWithTrades.trades.map((val, index) => {
      return {
        id: index + 1,
        created: new Date(val.createdAt).toUTCString(),
        stockName: "Reliance",
        quantity: val.quantity,
        entry_price: val.entry_price,
        exit_price: val.exit_price,
        tradeType: val.tradeType,
        pnl: val.pnl.toFixed(2),
      };
    });
  } catch (error) {
    console.log(error);
  }
}
