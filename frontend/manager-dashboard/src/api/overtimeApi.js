import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:9000"; // FastAPI backend

export const getOvertime = async (date) => {
  try {
    const token = sessionStorage.getItem("access_token");
    if (!token) throw new Error("Authorization token missing");

    const response = await axios.get(`${API_BASE_URL}/attendence`, {
      params: { date },
      headers: { Authorization: `Bearer ${token}` },
    });

    return response.data; // array of overtime records
  } catch (error) {
    console.error("Error fetching overtime:", error);
    return [];
  }
};
