import "./envConfig.ts";

import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"; // Replace with your actual API URL
export let AUTH_HEADER = {
  headers: {
    Authorization: ``, // Assuming the token is stored in localStorage
  },
};

// Function to handle login and get JWT token
export const loginUser = async (username: string, password: string) => {
  try {
    // Make the POST request to the FastAPI /token endpoint
    const response = await axios.post(`${API_URL}/token`, {
      username,
      password,
    });

    // Extract the token from the response
    const { access_token } = response.data;

    localStorage.setItem("access_token", access_token);
    AUTH_HEADER.headers = {
      Authorization: `Bearer ${access_token}`, // Assuming the token is stored in localStorage
    };

    return access_token; // You can return the token if needed
  } catch (error) {
    console.error("Login failed:", error);
    throw new Error("Invalid credentials or server error");
  }
};

// Function to get the current user's data (assuming token is stored in localStorage)
export const getCurrentUser = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/me`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching user data", error);
    throw error;
  }
};

// Function to create a new project
export const createProject = async (name: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/projects/`,
      { name },
      AUTH_HEADER
    );
    return response.data;
  } catch (error) {
    console.error("Error creating project", error);
    throw error;
  }
};

// Function to list all projects
export const listProjects = async () => {
  try {
    const response = await axios.get(`${API_URL}/projects/`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching projects", error);
    throw error;
  }
};

// Function to create a new user
export const createUser = async (username: string, password: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/users/`,
      { username, password },
      AUTH_HEADER
    );

    // Extract the token from the response
    const { access_token } = response.data;

    localStorage.setItem("access_token", access_token);
    AUTH_HEADER.headers = {
      Authorization: `Bearer ${access_token}`,
    };

    return response.data;
  } catch (error) {
    console.error("Error creating user", error);
    throw error;
  }
};

// Function to list all users
export const listUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching users", error);
    throw error;
  }
};

// Function to create a new chamber
export const createChamber = async (name: string, projectId: string) => {
  try {
    const response = await axios.post(
      `${API_URL}/chambers/`,
      { name, projectId },
      AUTH_HEADER
    );
    return response.data;
  } catch (error) {
    console.error("Error creating chamber", error);
    throw error;
  }
};

// Function to list all chambers
export const listChambers = async () => {
  try {
    const response = await axios.get(`${API_URL}/chambers/`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching chambers", error);
    throw error;
  }
};

export const roleUser = async (
  username: string,
  roleId: string,
  projectId: string
) => {
  try {
    const response = await axios.post(
      `${API_URL}/role_user/`,
      { username, roleId, projectId },
      AUTH_HEADER
    );
    return response.data;
  } catch (error) {
    console.error("Error role user", error);
    throw error;
  }
};

// Function to create new parameters
export const createParameter = async (
  chamberId: string,
  soilMoistureLowerLimit: number,
  lightingRoutine: string,
  temperatureRange: string,
  ventilationSchedule: string,
  photoCaptureFrequency: string
) => {
  try {
    const response = await axios.post(
      `${API_URL}/parameters/`,
      {
        chamberId,
        soilMoistureLowerLimit,
        lightingRoutine,
        temperatureRange,
        ventilationSchedule,
        photoCaptureFrequency,
      },
      AUTH_HEADER
    );
    return response.data;
  } catch (error) {
    console.error("Error creating parameter", error);
    throw error;
  }
};

// Function to list all parameters
export const listParameters = async () => {
  try {
    const response = await axios.get(`${API_URL}/parameters/`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching parameters", error);
    throw error;
  }
};

// Function to upload a photo
export const uploadPhoto = async (chamberId: string, photo: File) => {
  try {
    const formData = new FormData();
    formData.append("photo", photo);
    formData.append("chamberId", chamberId);

    const response = await axios.post(`${API_URL}/photos/`, formData, {
      headers: {
        ...AUTH_HEADER.headers,
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading photo", error);
    throw error;
  }
};

// Function to list all photos
export const listPhotos = async () => {
  try {
    const response = await axios.get(`${API_URL}/photos/`, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching photos", error);
    throw error;
  }
};

// Function to create an estimate
export const createEstimate = async (
  chamberId: string,
  leafCount: number,
  greenArea: number,
  estimateDate?: string
) => {
  try {
    const response = await axios.post(
      `${API_URL}/estimates/`,
      { chamberId, leafCount, greenArea, estimateDate },
      AUTH_HEADER
    );
    return response.data;
  } catch (error) {
    console.error("Error creating estimate", error);
    throw error;
  }
};

// Function to list estimates
export const listEstimates = async (chamberId?: string) => {
  try {
    const url = chamberId
      ? `${API_URL}/estimates/?chamberId=${chamberId}`
      : `${API_URL}/estimates/`;
    const response = await axios.get(url, AUTH_HEADER);
    return response.data;
  } catch (error) {
    console.error("Error fetching estimates", error);
    throw error;
  }
};
