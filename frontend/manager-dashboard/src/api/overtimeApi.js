import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const getOvertime = async () => {
  try {
    const token = sessionStorage.getItem("access_token");
    if (!token) throw new Error("Authorization token missing");

    const response = await axios.get(`${API_BASE_URL}/overtime`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching overtime:", error);
    return [];
  }
};

export const approveOvertime = async (payload) => {
  const token = sessionStorage.getItem("access_token");

  return axios.post(
    `${API_BASE_URL}/overtime/approve`,
    payload, // ✅ payload goes here
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};
