// import axios from "axios";

// const API_BASE_URL = "http://127.0.0.1:8000";

// // Fetch all shifts
// export const getShifts = async () => {
//   try {
//     const response = await axios.get(`${API_BASE_URL}/shifts`);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching shifts:", error);
//     return [];
//   }
// };

// // Delete a shift by shift_code
// export const deleteShift = async (shift_code) => {
//   try {
//     await axios.delete(`${API_BASE_URL}/shifts/${shift_code}`);
//     return true;
//   } catch (error) {
//     console.error("Error deleting shift:", error);
//     return false;
//   }
// };

import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

// Fetch all shifts
export const getShifts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/shifts`);
    return response.data; // returns array of shift objects
  } catch (error) {
    console.error("Error fetching shifts:", error);
    return [];
  }
};

// Add a new shift
export const addShift = async (shiftData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/create-shift`,
      shiftData,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding shift:", error);
    return null;
  }
};

// Update an existing shift
export const updateShift = async (shift_code, shiftData) => {
  try {
    const response = await axios.put(
      `${API_BASE_URL}/update-shift-time/${shift_code}`,
      shiftData,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  } catch (error) {
    console.error("Error updating shift:", error);
    return null;
  }
};

// Delete a shift
export const deleteShift = async (shift_code) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/delete-shift/${shift_code}`);
    return true;
  } catch (error) {
    console.error("Error deleting shift:", error);
    return null;
  }
};
