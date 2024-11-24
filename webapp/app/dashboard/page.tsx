"use client";

import React, { useState } from "react";
import {
  Home,
  LogOut,
  Thermometer,
  Droplets,
  Leaf,
  Sprout,
  Waves,
  UserPlus,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";

export default function PlantMonitoringDashboard() {
  const router = useRouter();
  const [selectedChamber, setSelectedChamber] = useState("1");

  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex items-center justify-between p-4 bg-primary text-primary-foreground">
        <h1 className="text-2xl font-bold">Plant Monitoring Dashboard</h1>
        <nav className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              router.push("/projects");
            }}
          >
            <Home className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              router.push("/add-user");
            }}
          >
            <UserPlus className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              localStorage.clear();

              router.push("/");
            }}
          >
            <LogOut className="h-5 w-5" />
          </Button>
        </nav>
      </header>

      <main className="flex-grow p-6 bg-muted/40">
        <div className="max-w-7xl mx-auto space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Greenhouse Chamber Selection</CardTitle>
              <CardDescription>
                Choose a chamber to view its data
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Select
                value={selectedChamber}
                onValueChange={setSelectedChamber}
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select a chamber" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">Chamber 1</SelectItem>
                  <SelectItem value="2">Chamber 2</SelectItem>
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Tabs defaultValue="metrics" className="space-y-4">
            <TabsList>
              <TabsTrigger value="metrics">Metrics</TabsTrigger>
              <TabsTrigger value="controls">Controls</TabsTrigger>
              <TabsTrigger value="gallery">Photo Gallery</TabsTrigger>
            </TabsList>

            <TabsContent value="metrics" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Temperature
                    </CardTitle>
                    <Thermometer className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">23°C</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Humidity
                    </CardTitle>
                    <Droplets className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">63%</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Soil Moisture
                    </CardTitle>
                    <Waves className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">67%</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Visible Leaves
                    </CardTitle>
                    <Leaf className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">9</div>
                    <p className="text-xs text-muted-foreground">
                      +2 leaves since last week
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Green Area
                    </CardTitle>
                    <Sprout className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">30 cm²</div>
                    <p className="text-xs text-muted-foreground">
                      +8 cm² since last week
                    </p>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Growth Metrics Over Time</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-[200px] w-full bg-muted/50 rounded-md flex items-center justify-center text-muted-foreground">
                    Chart placeholder: Line graph showing temperature, humidity,
                    soil moisture, leaves, and green area over time for Chamber{" "}
                    {selectedChamber}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="controls" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>
                    Environmental Controls for Chamber {selectedChamber}
                  </CardTitle>
                  <CardDescription>
                    Adjust parameters for optimal growth
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="light-schedule">Light Schedule</Label>
                    <div className="flex space-x-2">
                      <Input id="light-on" type="time" placeholder="On Time" />
                      <Input
                        id="light-off"
                        type="time"
                        placeholder="Off Time"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="watering-schedule">Watering Schedule</Label>
                    <div className="flex space-x-2">
                      <Input
                        id="watering-time"
                        type="time"
                        placeholder="Watering Time"
                      />
                      <Select>
                        <SelectTrigger>
                          <SelectValue placeholder="Frequency" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="daily">Daily</SelectItem>
                          <SelectItem value="every-other-day">
                            Every Other Day
                          </SelectItem>
                          <SelectItem value="twice-weekly">
                            Twice Weekly
                          </SelectItem>
                          <SelectItem value="weekly">Weekly</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="temperature">Temperature (°C)</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select temperature range" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="18-22">18-22°C</SelectItem>
                        <SelectItem value="22-26">22-26°C</SelectItem>
                        <SelectItem value="26-30">26-30°C</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="soil-moisture">Soil Moisture (%)</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select soil moisture range" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="50-60">50-60%</SelectItem>
                        <SelectItem value="60-70">60-70%</SelectItem>
                        <SelectItem value="70-80">70-80%</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="gallery" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>
                    Photo Gallery for Chamber {selectedChamber}
                  </CardTitle>
                  <CardDescription>
                    Visual record of plant growth
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {[...Array(8)].map((_, i) => (
                      <div
                        key={i}
                        className="aspect-square bg-muted/50 rounded-md flex items-center justify-center text-muted-foreground"
                      >
                        Plant Image {i + 1}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
}
