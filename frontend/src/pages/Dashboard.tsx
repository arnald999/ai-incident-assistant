import { useState } from "react";
import { Alert, Box, Container, Paper, Typography } from "@mui/material";
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
    <Box sx={{ minHeight: "100vh", bgcolor: "#f6f8fb" }}>
      <Container maxWidth="lg">
        <Box sx={{ py: 5 }}>
          <Box sx={{ textAlign: "center", mb: 4 }}>
            <Typography variant="h3" fontWeight={800} gutterBottom>
              AI Incident Assistant
            </Typography>

            <Typography variant="body1" color="text.secondary">
              Agent-powered incident investigation for SRE and platform teams.
            </Typography>
          </Box>

          <Paper elevation={0} sx={{ p: 3, borderRadius: 3 }}>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
              <AlertForm onSubmit={handleAnalyze} loading={loading} />

              {error && <Alert severity="error">{error}</Alert>}

              {result && <IncidentResult result={result} />}
            </Box>
          </Paper>

          <Box sx={{ textAlign: "center", mt: 4 }}>
            <Typography variant="caption" color="text.secondary">
              FastAPI • OpenRouter • Langfuse • React • Docker
            </Typography>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}