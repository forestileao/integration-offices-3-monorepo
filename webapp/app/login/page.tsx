"use client";

import React, { useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { AUTH_HEADER, loginUser } from "@/api";

export default function LoginPage() {
  const router = useRouter();
  const usernameRef = React.useRef<HTMLInputElement>(null);
  const passwordRef = React.useRef<HTMLInputElement>(null);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const username = usernameRef.current?.value || "";
    const password = passwordRef.current?.value || "";

    loginUser(username, password).then(() => {
      router.push("/projects");
    });
  };

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    AUTH_HEADER.headers = {
      Authorization: `Bearer ${token}`, // Assuming the token is stored in localStorage
    };

    if (token) {
      router.push("/projects");
    }
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen bg-muted/40">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl text-center">
            Plant Monitoring System
          </CardTitle>
          <CardDescription className="text-center">
            Login to access your projects
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="usernamame">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  required
                  ref={usernameRef}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  required
                  ref={passwordRef}
                />
              </div>
            </div>
            <Button type="submit" className="w-full mt-6">
              Log In
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-muted-foreground">
            {"Don't have an account? "}
            <Button
              variant="link"
              className="p-0"
              onClick={() => {
                router.push("/create-account");
              }}
            >
              Create Account
            </Button>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}
