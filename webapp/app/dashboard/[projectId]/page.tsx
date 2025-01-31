"use client";

import React, { useCallback, useEffect, useState } from "react";
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
import {
  API_URL,
  AUTH_HEADER,
  createParameter,
  getPhotos,
  getProject,
} from "@/api";
import { Chart } from "react-google-charts";

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
  estimateDate: string;
  soilMoisture: number;
  temperature: number;
  waterLevel: number;
  humidity: number;
  lightState: number;
}

interface Project {
  id: string;
  name: string;
  role: string;
  chambers: Chamber[];
  estimates: Estimate[];
  parameters: Parameter[];
  photos: Photo[];
}

interface Photo {
  id: string;
  chamberId: string;
  captureDate: string;
  leafCount: number;
  greenArea: number;
}

export default function PlantMonitoringDashboard() {
  const router = useRouter();
  const [selectedChamber, setSelectedChamber] = useState("1");
  const [project, setProject] = useState<Project>({} as Project);
  const [photos, setPhotos] = useState<Photo[]>([]);
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
          // remove 3 houts from the time to match the time zone
          new Date(a.estimateDate).getTime() -
          new Date(b.estimateDate).getTime()
        );
      })
      .map((x) => {
        const date = new Date(x.estimateDate);
        const hours = date.getHours();
        date.setHours(hours - 3);
        return {
          ...x,
          estimateDate: date.toLocaleString(),
        };
      }) || [];

  const photoEstimates =
    project.photos
      ?.filter((photo: Photo) => photo.chamberId === selectedChamber)
      .sort((a, b) => {
        return (
          new Date(a.captureDate).getTime() - new Date(b.captureDate).getTime()
        );
      })
      .map((x) => {
        const date = new Date(x.captureDate);
        const hours = date.getHours();
        date.setHours(hours - 3);
        return {
          ...x,
          captureDate: date.toLocaleString(),
        };
      }) || [];

  const mainEstimate = estimates.at(-1);
  const mainPhotoEstimate = photoEstimates.at(-1);

  const greenAreaData = [
    ["x", "Green Area"],
    ...(photoEstimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : photoEstimates.map((photo: Photo) => [
          photo.captureDate,
          photo.greenArea,
        ])),
  ];

  const visibleLeavesData = [
    ["x", "Visible Leaves"],
    ...(photoEstimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : photoEstimates.map((photo: Photo) => [
          photo.captureDate,
          photo.leafCount,
        ])),
  ];

  const temperatureData = [
    ["x", "Temperature"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : estimates.map((estimate: Estimate) => [
          estimate.estimateDate,
          estimate.temperature,
        ])),
  ];

  const humidityData = [
    ["x", "Humidity"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : estimates.map((estimate: Estimate) => [
          estimate.estimateDate,
          estimate.humidity,
        ])),
  ];

  const soilMoistureData = [
    ["x", "Soil Moisture"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : estimates.map((estimate: Estimate) => [
          estimate.estimateDate,
          estimate.soilMoisture,
        ])),
  ];

  const lightStateData = [
    ["x", "Light State"],
    ...(estimates.length == 0
      ? [[new Date().toLocaleString(), 0]]
      : estimates.map((estimate: Estimate) => [
          new Date(estimate.estimateDate).toLocaleString(),
          Number(estimate.lightState),
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

  const temperatureOptions = {
    title: "Temperature Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Temperature (°C)" },
    legend: "none",
    colors: ["#ff0000"],
  };

  const humidityOptions = {
    title: "Humidity Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Humidity (%)" },
    legend: "none",
    colors: ["#ff0000"],
  };

  const soilMoistureOptions = {
    title: "Soil Moisture Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Soil Moisture (%)" },
    legend: "none",
    colors: ["#ff0000"],
  };

  const lightStateOptions = {
    title: "Light State Over Time",
    hAxis: { title: "Time" },
    vAxis: { title: "Light State" },
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

  const loopGetProject = useCallback(() => {
    return setTimeout(() => {
      getProject((projectId as string) || "").then((data) => {
        console.log(data);
        setProject(data);
      });
      loopGetProject();
    }, 10_000);
  }, [projectId]);

  useEffect(() => {
    getProject((projectId as string) || "").then((data) => {
      console.log(data);
      setProject(data);
      setSelectedChamber(data.chambers[0].id);
    });

    const timeout = loopGetProject();

    return () => {
      clearTimeout(timeout);
    };
  }, []);

  useEffect(() => {
    const currentChamberParams = project.parameters?.find(
      (param: Parameter) => param.chamberId === selectedChamber
    );
    if (currentChamberParams) {
      setParameters(currentChamberParams);
    }

    // Fetch photos for selected chamber
    getPhotos(selectedChamber).then((data) => {
      setPhotos(data);
    });
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
                      {mainEstimate?.temperature?.toFixed(2) || "- "}°C
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
                      {mainEstimate?.humidity?.toFixed(2) || "- "}%
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
                      {mainEstimate?.soilMoisture?.toFixed(2) || "- "}%
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Needs Reservoir Refill
                    </CardTitle>
                    <Waves className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {(mainEstimate?.waterLevel || 0) < 20 ? "Yes" : "No"}
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
                      {mainPhotoEstimate?.leafCount || "- "}
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
                      {mainPhotoEstimate?.greenArea?.toFixed(2) || "- "} cm²
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
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={temperatureData}
                    options={temperatureOptions}
                  />
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={humidityData}
                    options={humidityOptions}
                  />
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={soilMoistureData}
                    options={soilMoistureOptions}
                  />
                  <Chart
                    chartType="SteppedAreaChart"
                    width="100%"
                    height="400px"
                    data={lightStateData}
                    options={lightStateOptions}
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
                        readOnly={project.role === "viewer"}
                        disabled={project.role === "viewer"}
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
                        readOnly={project.role === "viewer"}
                        disabled={project.role === "viewer"}
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
                    <Label htmlFor="light-schedule">Ventilation Schedule</Label>
                    <div className="flex space-x-2">
                      <Input
                        id="vent-start"
                        type="time"
                        readOnly={project.role === "viewer"}
                        disabled={project.role === "viewer"}
                        placeholder="On Time"
                        value={parameters?.ventilationSchedule?.split("/")[0]}
                        onChange={(e) => {
                          setParameters({
                            ...parameters,
                            ventilationSchedule: `${e.target.value}/${
                              parameters?.ventilationSchedule?.split("/")[1]
                            }`,
                          });
                        }}
                      />
                      <Input
                        id="vent-off"
                        type="time"
                        readOnly={project.role === "viewer"}
                        disabled={project.role === "viewer"}
                        placeholder="Off Time"
                        value={parameters?.ventilationSchedule?.split("/")[1]}
                        onChange={(e) => {
                          setParameters({
                            ...parameters,
                            ventilationSchedule: `${
                              parameters?.ventilationSchedule?.split("/")[0]
                            }/${e.target.value}`,
                          });
                        }}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="temperature">Temperature (°C)</Label>
                    <Select
                      disabled={project.role === "viewer"}
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
                        {Array.from({ length: 16 }, (_x, i) => (
                          <SelectItem
                            key={i.toString() + "temperature-ee"}
                            value={String(i + 15)}
                          >
                            {i + 15}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="soil-moisture">Soil Moisture (%)</Label>
                    <Input
                      readOnly={project.role === "viewer"}
                      disabled={project.role === "viewer"}
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
                      readOnly={project.role === "viewer"}
                      disabled={project.role === "viewer"}
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
              {project.role === "admin" && (
                <Button onClick={() => updateParameters()} className="w-full">
                  Save Changes
                </Button>
              )}
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
                    {photos.map((photo: Photo) => (
                      <div
                        key={photo.id}
                        className="aspect-square bg-muted/50 rounded-md flex flex-col items-center justify-center text-muted-foreground"
                      >
                        <img
                          style={{ width: 200, height: 200 }}
                          className="object-cover"
                          src={`${API_URL}/photo/${photo.id}/`}
                          alt={photo.id}
                          onError={(e) => {
                            e.currentTarget.src =
                              "https://demofree.sirv.com/nope-not-here.jpg";
                          }}
                        />
                        <span className="text-muted-foreground">
                          {new Date(photo.captureDate).toLocaleString()}
                        </span>
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
