import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const getMonthlyReport = async (year, month) => {
    const token = sessionStorage.getItem("access_token");
 
    if (!token) {
      throw new Error("Authorization token missing");
    }
 
    const response = await axios.get(
      `${API_BASE_URL}/report`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
            year,
            month,
            },
      }
    );
  return response.data;
};
