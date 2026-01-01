import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const loginUser = async (credentials) => {
  try {
    const res = await axios.get(`${API_BASE_URL}/manager/login`, credentials);
    return res.data;
  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};

export const registerUser = async (data) => {
  try {
    const res = await axios.post(`${API_BASE_URL}/manager/register`, data);
    return res.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};
