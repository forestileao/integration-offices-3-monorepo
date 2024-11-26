"use client";

import React, { useEffect, useState } from "react";
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
import { useParams, useRouter } from "next/navigation";
import { AUTH_HEADER, getProject } from "@/api";
import { Chart } from "react-google-charts";

interface Chamber {
  id: string;
  name: string;
}

interface Project {
  id: string;
  name: string;
  chambers: Chamber[];
}

export default function PlantMonitoringDashboard() {
  const router = useRouter();
  const [selectedChamber, setSelectedChamber] = useState("1");
  const [project, setProject] = useState<Project>({} as Project);
  const { projectId } = useParams();

  const currentChamber = project.chambers?.find(
    (chamber: Chamber) => chamber.id === selectedChamber
  );

  const greenAreaData = [
    ["x", "Green Area"],
    [0, 0],
    [1, 10],
    [2, 23],
    [3, 17],
    [4, 18],
    [5, 9],
    [6, 11],
    [7, 27],
    [8, 33],
    [9, 40],
    [10, 32],
    [11, 35],
  ];

  const visibleLeavesData = [
    ["x", "Visible Leaves"],
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 3],
    [5, 3],
    [6, 4],
    [7, 4],
    [8, 5],
    [9, 5],
    [10, 6],
    [11, 7],
  ];

  const greenAreaOptions = {
    title: "Green Area Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Green Area (cm²)" },
    legend: "none",
    colors: ["#2ECC71"],
  };

  const visibleLeavesOptions = {
    title: "Visible Leaves Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Visible Leaves" },
    legend: "none",
    colors: ["#ff0000"],
  };

  useEffect(() => {
    getProject((projectId as string) || "").then((data) => {
      console.log(data);
      setProject(data);
      setSelectedChamber(data.chambers[0].id);
    });
  }, []);

  if (!AUTH_HEADER.headers.Authorization) {
    router.push("/");
    return null;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex items-center justify-between p-4 bg-primary text-primary-foreground">
        <h1 className="text-2xl font-bold">
          Plant Monitoring Dashboard{project.id && ` - ${project.name}`}
        </h1>
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
                  {project?.chambers?.map((chamber: any) => (
                    <SelectItem key={chamber.id} value={chamber.id}>
                      {chamber.name}
                    </SelectItem>
                  ))}
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
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={greenAreaData}
                    options={greenAreaOptions}
                  />
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={visibleLeavesData}
                    options={visibleLeavesOptions}
                  />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="controls" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>
                    Environmental Controls for {currentChamber?.name}
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
                    <Input
                      id="soil-moisture"
                      type="number"
                      placeholder="Enter soil moisture level"
                      defaultValue={57}
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="gallery" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>
                    Photo Gallery for {currentChamber?.name}
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
