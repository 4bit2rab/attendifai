import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const assignShift = async (employeeId, shiftCode) => {
  const res = await axios.put(
    `${API_BASE_URL}/assign-shift/${employeeId}`,
    null,
    {
      params: {
        shift_code: shiftCode,
      },
    }
  );

  return res.data;
};

export const getEmployees = async () => {
  try {
    const token = sessionStorage.getItem("access_token");
 
    if (!token) {
      throw new Error("Authorization token missing");
    }
 
    const response = await axios.get(
      `${API_BASE_URL}/manager/employees`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
 
    // Axios already ensures 2xx success
    return response.data.employees; // return only employees array
  } catch (error) {
    console.error(
      "Error fetching employees:",
      error.response?.data || error.message
    );
    return [];
  }
};