"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { signinSchema } from "@/lib/zod";
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
import { Button } from "./button";
import {
  handleCredentialsSignin,
  handleSignUp,
} from "@/app/actions/authActions";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./tooltip";
import { useState } from "react";
import ErrorMessage from "./errorMessage";
import { useRouter } from "next/navigation";
import LoadingButton from "./loadingButton";

export default function SigninForm() {
  const router = useRouter();
  const form = useForm<z.infer<typeof signinSchema>>({
    resolver: zodResolver(signinSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const [passwordVisible, setPasswordVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [globalError, setGlobalError] = useState<string>("");

  async function onSubmit(values: z.infer<typeof signinSchema>) {
    try {
      setIsLoading(true);
      let result = await handleSignUp(values);
      if (result.success) {
        console.log("Account created successfully.");
        const valuesForSignin = {
          email: values.email,
          password: values.password,
        };

        result = await handleCredentialsSignin(valuesForSignin);

        if (result?.message) {
          setGlobalError(result.message);
        } else {
          router.push("/dashboard");
        }
      } else {
        setGlobalError(result.message);
      }
      setIsLoading(false);
    } catch (error) {
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
            text="Sign in"
            loadingText="Signing in"
            className="w-full"
          />
        </form>
      </Form>
    </>
  );
}
