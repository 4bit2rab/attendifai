import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:9000"; // FastAPI backend

export const getAttendance = async (date) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/attendance`, {
      params: { date },
    });
    return response.data; // returns array of attendance records
  } catch (error) {
    console.error("Error fetching attendance:", error);
    return [];
  }
};
