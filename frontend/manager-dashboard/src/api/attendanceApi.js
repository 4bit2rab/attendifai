import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

export const getAttendance = async (date) => {
  try {
    const token = sessionStorage.getItem("access_token");
 
    if (!token) {
      throw new Error("Authorization token missing");
    }
 
    const response = await axios.get(`${API_BASE_URL}/attendance`, {
      params: { date },headers: {
          Authorization: `Bearer ${token}`,
        },
    });
    return response.data; // returns array of attendance records
  } catch (error) {
    console.error("Error fetching attendance:", error);
    return [];
  }
};
