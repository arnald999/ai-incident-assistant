import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  MenuItem,
  TextField,
  Typography,
} from "@mui/material";

export interface AlertPayload {
  service_name: string;
  alert_type: string;
  message: string;
  environment: string;
}

interface AlertFormProps {
  onSubmit: (payload: AlertPayload) => void;
  loading: boolean;
}

export default function AlertForm({ onSubmit, loading }: AlertFormProps) {
  const [payload, setPayload] = useState<AlertPayload>({
    service_name: "search-service",
    alert_type: "ServiceDegradation",
    message: "P95 latency increased from 150ms to 2.5s",
    environment: "production",
  });

  const handleChange = (field: keyof AlertPayload, value: string) => {
    setPayload((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Submit Incident Alert
        </Typography>

        <Box display="flex" flexDirection="column" gap={2}>
          <TextField
            label="Service Name"
            value={payload.service_name}
            onChange={(e) => handleChange("service_name", e.target.value)}
            fullWidth
          />

          <TextField
            select
            label="Alert Type"
            value={payload.alert_type}
            onChange={(e) => handleChange("alert_type", e.target.value)}
            fullWidth
          >
            <MenuItem value="ServiceDegradation">Service Degradation</MenuItem>
            <MenuItem value="CrashLoopBackOff">CrashLoopBackOff</MenuItem>
            <MenuItem value="HighCPUUsage">High CPU Usage</MenuItem>
            <MenuItem value="MemoryPressure">Memory Pressure</MenuItem>
          </TextField>

          <TextField
            label="Message"
            value={payload.message}
            onChange={(e) => handleChange("message", e.target.value)}
            fullWidth
            multiline
            rows={3}
          />

          <TextField
            select
            label="Environment"
            value={payload.environment}
            onChange={(e) => handleChange("environment", e.target.value)}
            fullWidth
          >
            <MenuItem value="production">Production</MenuItem>
            <MenuItem value="staging">Staging</MenuItem>
            <MenuItem value="development">Development</MenuItem>
          </TextField>

          <Button
            variant="contained"
            size="large"
            onClick={() => onSubmit(payload)}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Incident"}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}