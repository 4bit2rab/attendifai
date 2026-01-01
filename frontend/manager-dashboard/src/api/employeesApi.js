import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:9000";

export const getEmployees = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get-all-employee`);
    return response.data;
  } catch (error) {
    console.error("Error fetching employees:", error);
    return [];
  }
};

export const createEmployee = async (employeeData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/create-employee`,
      employeeData,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  } catch (error) {
    console.error("Error creating employee:", error);
    return null;
  }
};
