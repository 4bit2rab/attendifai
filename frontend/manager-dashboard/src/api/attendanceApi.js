import axios from "axios";

export const getAttendance = async (date) => {
  try {
    const response = await axios.get(`/api/attendance`, {
      params: { date }, // pass date to backend
    });
    return response.data; // returns array
  } catch (error) {
    console.error("Error fetching attendance:", error);
    return [];
  }
};
