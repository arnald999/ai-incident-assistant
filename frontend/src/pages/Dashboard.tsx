import { useState } from "react";
import { Alert, Box, Container, Typography } from "@mui/material";
import AlertForm, { type AlertPayload } from "../components/AlertForm";
import IncidentResult from "../components/IncidentResult";
import { analyzeIncident } from "../api/incidentApi";
import type { IncidentAnalysis } from "../types/incident";

export default function Dashboard() {
  const [result, setResult] = useState<IncidentAnalysis | null>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (payload: AlertPayload) => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeIncident(payload);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze incident. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box py={4}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          AI Incident Assistant
        </Typography>

        <Typography variant="body1" color="text.secondary" mb={3}>
          Submit a production alert and let the AI agent classify the incident,
          execute investigation tools, and generate a structured diagnosis.
        </Typography>

        <Box display="flex" flexDirection="column" gap={3}>
          <AlertForm onSubmit={handleAnalyze} loading={loading} />

          {error && <Alert severity="error">{error}</Alert>}

          {result && <IncidentResult result={result} />}
        </Box>
      </Box>
    </Container>
  );
}