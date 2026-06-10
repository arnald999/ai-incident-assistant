import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
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

const labelProps = {
  inputLabel: {
    shrink: true,
  },
};

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
    <Card sx={{ borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h5" align="center" fontWeight={700} gutterBottom>
          Submit Incident Alert
        </Typography>

        <Box sx={{ display: "flex", flexDirection: "column", gap: 2.5, mt: 3 }}>
          <TextField
            label="Service Name"
            value={payload.service_name}
            slotProps={labelProps}
            onChange={(e) => handleChange("service_name", e.target.value)}
            fullWidth
          />

          <TextField
            select
            label="Alert Type"
            value={payload.alert_type}
            slotProps={labelProps}
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
            slotProps={labelProps}
            onChange={(e) => handleChange("message", e.target.value)}
            fullWidth
            multiline
            rows={4}
          />

          <TextField
            select
            label="Environment"
            value={payload.environment}
            slotProps={labelProps}
            onChange={(e) => handleChange("environment", e.target.value)}
            fullWidth
          >
            <MenuItem value="production">Production</MenuItem>
            <MenuItem value="staging">Staging</MenuItem>
            <MenuItem value="development">Development</MenuItem>
          </TextField>

          <Box sx={{ display: "flex", justifyContent: "center" }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => onSubmit(payload)}
              disabled={loading}
              startIcon={
                loading ? <CircularProgress size={18} color="inherit" /> : null
              }
              sx={{ px: 4, py: 1.2, fontWeight: 700 }}
            >
              {loading ? "Analyzing..." : "Analyze Incident"}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}