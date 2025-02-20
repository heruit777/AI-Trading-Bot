"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { settingSchema } from "@/lib/zod";
import { z } from "zod";
import axios from "axios";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "./button";
import { Input } from "./input";
import { createBroker, fetchBroker } from "@/app/actions/actions";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import MoonLoader from "react-spinners/MoonLoader";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { parseNumber } from "@/lib/utils";

export default function SettingsPage() {
  const [loading, setLoading] = useState(false);
  const [isDisabled, setIsDisabled] = useState<number>(1);
  const { data: session } = useSession();
  const router = useRouter();

  const form = useForm<z.infer<typeof settingSchema>>({
    resolver: zodResolver(settingSchema),
    defaultValues: {
      accessToken: "",
      brokerType: "",
      balance: 10000,
      apiKey: "",
      apiSecret: "",
    },
  });

  const brokerType = form.watch("brokerType");

  async function onSubmit(values: z.infer<typeof settingSchema>) {
    console.log("Clicked");
    setLoading(true);
    try {
      console.log(values);
      const res = await createBroker(values);
      toast("Settings updated successfully 🎉");
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }

  const handleGetAccessToken = async () => {
    const clientId = form.watch("apiKey"); // Get API Key
    const clientSecret = form.watch("apiSecret"); // Get API Secret
    const userId = session?.user?.id; // Get User ID from session

    // Ensure values are provided before redirecting
    if (!clientId || !clientSecret) {
      toast.error("Please enter API Key and API Secret before proceeding.");
      return;
    }

    // Construct the URL with query parameters
    const url = `http://127.0.0.1:8000/login?client_id=${encodeURIComponent(
      clientId
    )}&client_secret=${encodeURIComponent(clientSecret)}&user_id=${userId}`;

    // router.push(url)
    const { data } = await axios.get(url);
    window.open(data.url, "_blank");
  };

  useEffect(() => {
    const status = localStorage.getItem("isWebsocketConnected");
    if (!status || status === '0') setIsDisabled(0);
    else setIsDisabled(1);
  }, []);

  useEffect(() => {
    (async () => {
      const brokerData = await fetchBroker();
      if (brokerData) {
        form.setValue("brokerType", brokerData.broker_type as string);
        form.setValue("balance", Number(brokerData.balance.toFixed(2)) as number);
        form.setValue("accessToken", brokerData.access_token as string);
        form.setValue("apiKey", brokerData.api_key as string);
        form.setValue("apiSecret", brokerData.api_secret as string);
      }
    })();
  }, [form]);
  return (
    <div className="mx-auto w-3/4 mt-10 px-10 py-5 rounded-lg border">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="brokerType"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-lg font-bold">Broker</FormLabel>
                <FormControl>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <SelectTrigger className="border border-gray-500">
                      <SelectValue placeholder="Select a broker" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="upstox">Upstox</SelectItem>
                      <SelectItem value="dummy">Dummy</SelectItem>
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {brokerType === "dummy" && (
            <FormField
              control={form.control}
              name="balance"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-lg font-bold">Balance</FormLabel>
                  <FormControl>
                    <div className="flex space-x-4">
                      <Input
                        placeholder="Enter Balance"
                        {...field}
                        disabled={isDisabled === 1}
                        className="border border-gray-500"
                        onChange={(e) =>
                          field.onChange(parseNumber(e.target.value))
                        }
                        // ISSUE: Balance can't be float in frontend
                      />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}
          {brokerType !== "dummy" && brokerType !== "" && (
            <>
              <div>
                Refer to the following link to generate the API Key and API
                Secret:
                <a
                  href="https://help.upstox.com/support/solutions/articles/258159-how-to-create-an-api-app-"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-blue-500 hover:underline"
                >
                  Guide to create upstox api app
                </a>
              </div>
              <FormField
                control={form.control}
                name="apiKey"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-lg font-bold">API Key</FormLabel>
                    <FormControl>
                      <div className="flex space-x-4">
                        <Input
                          placeholder="Enter your API Key"
                          {...field}
                          className="border border-gray-500"
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="apiSecret"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-lg font-bold">
                      API Secret
                    </FormLabel>
                    <FormControl>
                      <div className="flex space-x-4">
                        <Input
                          placeholder="Enter your API Secret"
                          {...field}
                          className="border border-gray-500"
                        />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="accessToken"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-lg font-bold">
                      Access Token
                    </FormLabel>
                    <FormControl>
                      <div className="flex space-x-4">
                        <Input
                          placeholder="Enter your access token"
                          {...field}
                          className="border border-gray-500"
                        />
                        <Button type="button" onClick={handleGetAccessToken}>
                          Get Access Token
                        </Button>
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </>
          )}
          <div className="flex">
            <Button
              type="submit"
              className={`w-1/2 mx-auto mt-5 ${loading && "bg-primary/90"}`}
            >
              {loading ? (
                <>
                  <MoonLoader
                    size={20}
                    aria-label="Loading Spinner"
                    data-testid="loader"
                  />
                  submitting
                </>
              ) : (
                "Submit"
              )}
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
}
