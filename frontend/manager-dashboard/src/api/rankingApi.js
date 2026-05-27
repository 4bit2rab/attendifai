import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // CHANGE if backend URL differs
});

/**
 * Fetch AI productivity insights for manager
 */
export const getEmployeeRanking = async (
  start_date,
  end_date
) => {
  const token = sessionStorage.getItem("access_token");

  if (!token) {
    throw new Error("Auth token missing");
  }

  const response = await api.get(
    "/employee-ranking",
    {
      params: { start_date, end_date },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  // Always return safe structure
  return response.data.rankings || [];
};
