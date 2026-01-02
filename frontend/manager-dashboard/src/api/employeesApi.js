import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:9000";

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

// -------------------- Activity Threshold --------------------

// Get current activity threshold
export const getActivityThreshold = async () => {
  try {
    const token = sessionStorage.getItem("access_token");
    if (!token) throw new Error("Authorization token missing");

    const response = await axios.get(`${API_BASE_URL}/activity-threshold`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.data; // {id, idle_time_out}
  } catch (error) {
    console.error(
      "Error fetching activity threshold:",
      error.response?.data || error.message
    );
    return null;
  }
};

// Create or update activity threshold
export const createOrUpdateActivityThreshold = async (idleTimeOut) => {
  try {
    const token = sessionStorage.getItem("access_token");
    if (!token) throw new Error("Authorization token missing");

    const response = await axios.post(
      `${API_BASE_URL}/activity-threshold`,
      { idle_time_out: idleTimeOut },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data; // {id, idle_time_out}
  } catch (error) {
    console.error(
      "Error creating/updating activity threshold:",
      error.response?.data || error.message
    );
    return null;
  }
};

// Update activity threshold by ID (optional)
export const updateActivityThreshold = async (id, idleTimeOut) => {
  try {
    const token = sessionStorage.getItem("access_token");
    if (!token) throw new Error("Authorization token missing");

    const response = await axios.put(
      `${API_BASE_URL}/activity-threshold/${id}`,
      { idle_time_out: idleTimeOut },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data; // {id, idle_time_out}
  } catch (error) {
    console.error(
      "Error updating activity threshold:",
      error.response?.data || error.message
    );
    return null;
  }
};