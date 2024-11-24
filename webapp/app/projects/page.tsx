"use client";

import React, { useEffect, useState } from "react";
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { LogOut, PlusCircle, Trash2, UserPlus } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useRouter } from "next/navigation";
import { createProject, listProjects } from "@/api";

interface Project {
  id: string;
  name: string;
  role: string;
}

export default function ProjectSelectionPage() {
  const router = useRouter();

  const [projects, setProjects] = useState<Project[]>([]);
  const [newProject, setNewProject] = useState({ name: "", description: "" });
  const { toast } = useToast();

  const handleAddProject = () => {
    if (newProject.name && newProject.description) {
      createProject(newProject.name).then((project) => {
        setProjects([...projects, project]);
        setNewProject({ name: "", description: "" });
      });
    }
  };

  const handleDeleteProject = (id: string) => {
    setProjects(projects.filter((project) => project.id !== id));
    toast({
      title: "Success",
      description: "Project deleted successfully",
    });
  };

  const handleOpenProject = (_id: string) => {
    router.push(`/dashboard/`);
  };

  useEffect(() => {
    listProjects().then((data) => {
      setProjects(data);
    });
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex items-center justify-between p-4 bg-primary text-primary-foreground">
        <h1 className="text-2xl font-bold">Projects</h1>
        <nav className="flex items-center space-x-4">
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
      <div className="min-h-screen bg-muted/40 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">Your Projects</h1>
          <div className="grid gap-6 md:grid-cols-2">
            {projects.map((project) => (
              <Card key={project.id}>
                <CardHeader>
                  <CardTitle>{project.name}</CardTitle>
                </CardHeader>
                <CardFooter className="flex justify-between">
                  <Button
                    className="flex-grow mr-2"
                    onClick={() => handleOpenProject(project.id)}
                  >
                    Open Project
                  </Button>
                  {project.role == "admin" && (
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button variant="destructive" size="icon">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                          <AlertDialogDescription>
                            This action cannot be undone. This will permanently
                            delete the project and remove all associated data.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>Cancel</AlertDialogCancel>
                          <AlertDialogAction
                            onClick={() => handleDeleteProject(project.id)}
                          >
                            Delete
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  )}
                </CardFooter>
              </Card>
            ))}
            <Dialog>
              <DialogTrigger asChild>
                <Card className="flex flex-col items-center justify-center cursor-pointer hover:bg-muted/60 transition-colors">
                  <CardContent className="pt-6">
                    <PlusCircle className="w-12 h-12 mb-4 text-muted-foreground" />
                    <p className="text-lg font-medium">Add New Project</p>
                  </CardContent>
                </Card>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New Project</DialogTitle>
                  <DialogDescription>
                    Create a new project for your plant monitoring experiments.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="project-name">Project Name</Label>
                    <Input
                      id="project-name"
                      value={newProject.name}
                      onChange={(e) =>
                        setNewProject({ ...newProject, name: e.target.value })
                      }
                      placeholder="Enter project name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="project-description">
                      Project Description
                    </Label>
                    <Input
                      id="project-description"
                      value={newProject.description}
                      onChange={(e) =>
                        setNewProject({
                          ...newProject,
                          description: e.target.value,
                        })
                      }
                      placeholder="Enter project description"
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button onClick={handleAddProject}>Add Project</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </div>
    </div>
  );
}
