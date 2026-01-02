import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // your FastAPI URL
});

export const getWeeklySummary = async () => {
  const token = sessionStorage.getItem("access_token");

  if (!token) {
    throw new Error("Auth token missing");
  }

  const response = await api.get(
    "/weekly/productivity-summary", // match backend
    {
      headers: {
        Authorization: `Bearer ${token}`, // send token in header
      },
    }
  );

  return response.data;
};
