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
    console.log(existingBroker);
    return existingBroker;
  } catch (error) {
    console.error("Error fetching broker:", error);
    throw error;
  }
}

export async function createBroker({
  brokerType,
  accessToken,
  apiKey,
  apiSecret,
}: {
  brokerType: string;
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
      
      return await prisma.broker.update({
        where: { userId },
        data: {
          broker_type: brokerType,
          access_token: accessToken,
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
