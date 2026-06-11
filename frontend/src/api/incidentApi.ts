import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const analyzeIncident = async (payload: any) => {
  const response = await axios.post(
    `${API_URL}/api/alerts/analyze`,
    payload
  );

  return response.data;
};