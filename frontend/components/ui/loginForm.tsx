"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { loginSchema } from "@/lib/zod";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { handleCredentialsSignin } from "@/app/actions/authActions";
import { useState } from "react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./tooltip";
import ErrorMessage from "./errorMessage";
import { useRouter } from "next/navigation";
import LoadingButton from "./loadingButton";

export default function LoginForm() {
  const router = useRouter();
  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const [passwordVisible, setPasswordVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [globalError, setGlobalError] = useState<string>("");

  async function onSubmit(values: z.infer<typeof loginSchema>) {
    try {
      setIsLoading(true);
      const result = await handleCredentialsSignin(values);

      if (result?.message) {
        setGlobalError(result.message);
      } else {
        router.push("/dashboard");
      }
      setIsLoading(false);
    } catch (error) {
      // console.log(`An unexpected error occurred. Please try again. ${error}`);
      console.error(`${error}`);
      setGlobalError("An unexpected error occurred. Please try again.");
    }
  }

  return (
    <>
      {globalError && <ErrorMessage error={globalError} />}
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="Enter your email" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <Input
                      type={passwordVisible ? "text" : "password"}
                      placeholder="Enter your password"
                      {...field}
                    />
                    <div
                      onClick={(e) => {
                        e.preventDefault();
                        setPasswordVisible(!passwordVisible);
                      }}
                      className="absolute bottom-1 right-2 text-xl"
                    >
                      <TooltipProvider>
                        {passwordVisible ? (
                          <Tooltip>
                            <TooltipTrigger>
                              <span role="img" aria-label="Hide password">
                                🙈
                              </span>
                            </TooltipTrigger>
                            <TooltipContent>Hide Password</TooltipContent>
                          </Tooltip>
                        ) : (
                          <Tooltip>
                            <TooltipTrigger>
                              <span role="img" aria-label="Show password">
                                👁️
                              </span>
                            </TooltipTrigger>
                            <TooltipContent>Show Password</TooltipContent>
                          </Tooltip>
                        )}
                      </TooltipProvider>
                    </div>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <LoadingButton
            type="submit"
            loading={isLoading}
            text="Log in"
            loadingText="Logging in"
            className="w-full"
          />
        </form>
      </Form>
    </>
  );
}
