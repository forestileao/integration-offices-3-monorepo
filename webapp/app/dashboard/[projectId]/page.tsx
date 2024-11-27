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
import { AUTH_HEADER, createParameter, getProject } from "@/api";
import { Chart } from "react-google-charts";

import firstTemplateImage from "@/assets/image.png";
import secondTemplateImage from "@/assets/image2.png";

interface Chamber {
  id: string;
  name: string;
}

interface Parameter {
  id: string;
  chamberId: string;
  soilMoistureLowerLimit: number;
  lightingRoutine: string;
  temperatureRange: string;
  ventilationSchedule: string;
  photoCaptureFrequency: string;
}

interface Estimate {
  id: string;
  chamberId: string;
  leafCount: number;
  greenArea: number;
  estimateDate: string;
  soilMoisture: number;
  temperature: number;
  humidity: number;
}

interface Project {
  id: string;
  name: string;
  chambers: Chamber[];
  estimates: Estimate[];
  parameters: Parameter[];
}

export default function PlantMonitoringDashboard() {
  const router = useRouter();
  const [selectedChamber, setSelectedChamber] = useState("1");
  const [project, setProject] = useState<Project>({} as Project);
  const { projectId } = useParams();

  const [parameters, setParameters] = useState<Parameter>({} as Parameter);

  const currentChamber = project.chambers?.find(
    (chamber: Chamber) => chamber.id === selectedChamber
  );

  const estimates =
    project.estimates
      ?.filter((estimate: Estimate) => estimate.chamberId === selectedChamber)
      .sort((a, b) => {
        return (
          new Date(b.estimateDate).getTime() -
          new Date(a.estimateDate).getTime()
        );
      }) || [];

  const mainEstimate = estimates[0];

  const greenAreaData = [
    ["x", "Green Area"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleTimeString(), 0]]
      : estimates.map((estimate: Estimate) => [
          new Date(estimate.estimateDate).toLocaleTimeString(),
          estimate.greenArea,
        ])),
  ];

  const visibleLeavesData = [
    ["x", "Visible Leaves"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleTimeString(), 0]]
      : estimates.map((estimate: Estimate) => [
          new Date(estimate.estimateDate).toLocaleTimeString(),
          estimate.leafCount,
        ])),
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

  const updateParameters = async () => {
    await createParameter(
      selectedChamber,
      parameters.soilMoistureLowerLimit,
      parameters.lightingRoutine,
      parameters.temperatureRange,
      parameters.ventilationSchedule,
      parameters.photoCaptureFrequency
    );

    await getProject((projectId as string) || "").then((data) => {
      setProject(data);
    });
  };

  useEffect(() => {
    getProject((projectId as string) || "").then((data) => {
      console.log(data);
      setProject(data);
      setSelectedChamber(data.chambers[0].id);
    });
  }, []);

  useEffect(() => {
    const currentChamberParams = project.parameters?.find(
      (param: Parameter) => param.chamberId === selectedChamber
    );
    if (currentChamberParams) {
      setParameters(currentChamberParams);
    }
  }, [selectedChamber]);

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
                  {project?.chambers?.map((chamber: Chamber) => (
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
                    <div className="text-2xl font-bold">
                      {mainEstimate?.temperature || "- "}°C
                    </div>
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
                    <div className="text-2xl font-bold">
                      {mainEstimate?.humidity || "- "}%
                    </div>
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
                    <div className="text-2xl font-bold">
                      {mainEstimate?.soilMoisture || "- "}%
                    </div>
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
                    <div className="text-2xl font-bold">
                      {mainEstimate?.leafCount || "- "}
                    </div>
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
                    <div className="text-2xl font-bold">
                      {mainEstimate?.greenArea || "- "} cm²
                    </div>
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
                      <Input
                        id="light-on"
                        type="time"
                        placeholder="On Time"
                        value={parameters?.lightingRoutine?.split("/")[0]}
                        onChange={(e) => {
                          setParameters({
                            ...parameters,
                            lightingRoutine: `${e.target.value}/${
                              parameters?.lightingRoutine?.split("/")[1]
                            }`,
                          });
                        }}
                      />
                      <Input
                        id="light-off"
                        type="time"
                        placeholder="Off Time"
                        value={parameters?.lightingRoutine?.split("/")[1]}
                        onChange={(e) => {
                          setParameters({
                            ...parameters,
                            lightingRoutine: `${
                              parameters?.lightingRoutine?.split("/")[0]
                            }/${e.target.value}`,
                          });
                        }}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="temperature">Temperature (°C)</Label>
                    <Select
                      value={parameters?.temperatureRange}
                      onValueChange={(value) => {
                        setParameters({
                          ...parameters,
                          temperatureRange: value,
                        });
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select temperature range" />
                      </SelectTrigger>
                      <SelectContent>
                        {[...Array(21)].map((_, i) => (
                          <SelectItem key={i} value={(i + 10).toString()}>
                            {(i + 10).toString()}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="soil-moisture">Soil Moisture (%)</Label>
                    <Input
                      id="soil-moisture"
                      type="number"
                      placeholder="Enter soil moisture level"
                      value={parameters?.soilMoistureLowerLimit}
                      onChange={(e) => {
                        setParameters({
                          ...parameters,
                          soilMoistureLowerLimit: Number(e.target.value),
                        });
                      }}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="photo-capture-frequency">
                      Photo Capture Frequency (mins)
                    </Label>
                    <Input
                      id="photo-capture-frequency"
                      type="number"
                      placeholder="Enter photo capture frequency"
                      value={parameters?.photoCaptureFrequency}
                      onChange={(e) => {
                        setParameters({
                          ...parameters,
                          photoCaptureFrequency: e.target.value,
                        });
                      }}
                    />
                  </div>
                </CardContent>
              </Card>
              <Button onClick={() => updateParameters()} className="w-full">
                Save Changes
              </Button>
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
                    <div className="aspect-square bg-muted/50 rounded-md flex flex-col items-center justify-center text-muted-foreground">
                      <img
                        style={{ width: 200, height: 200 }}
                        className="object-cover"
                        src={firstTemplateImage.src}
                        alt="wow"
                      />
                      <span className="text-muted-foreground">
                        {new Date("2024-11-27").toLocaleString()}
                      </span>
                    </div>
                    <div className="aspect-square bg-muted/50 rounded-md flex flex-col items-center justify-center text-muted-foreground">
                      <img
                        style={{ width: 200, height: 200 }}
                        className="object-cover"
                        src={secondTemplateImage.src}
                        alt="wow"
                      />
                      <span className="text-muted-foreground">
                        {new Date("2024-11-27").toLocaleString()}
                      </span>
                    </div>
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
