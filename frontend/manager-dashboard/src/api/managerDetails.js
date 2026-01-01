import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; 

export const getManagerDetails = async () => {
  try {
    const token = sessionStorage.getItem("access_token");
 
    if (!token) {
      throw new Error("Authorization token missing");
    }

    const response = await axios.get(`${API_BASE_URL}/manager/details`, {
      headers: {
          Authorization: `Bearer ${token}`,
        },
    });
    // sessionStorage.setItem("manager_name", response.data.manager_name)
    return response.data; // returns array of manager records
  } catch (error) {
    console.error("Error fetching manager details:", error);
    return [];
  }
};