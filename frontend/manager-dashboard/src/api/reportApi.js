import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:9000";

export const getMonthlyEmployeeReport = async (
  managerId,
  startDate,
  endDate
) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/employee/report`,
      {
        params: {
          manager_id: managerId,
          start_date: startDate,
          end_date: endDate,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching monthly report:", error);
    return [];
  }
};
