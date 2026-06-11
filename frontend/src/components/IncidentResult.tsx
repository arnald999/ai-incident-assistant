import {
  Box,
  Card,
  CardContent,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import type { ChipProps } from "@mui/material";
import type { IncidentAnalysis } from "../types/incident";
import InvestigationTimeline from "./InvestigationTimeline";

interface IncidentResultProps {
  result: IncidentAnalysis;
}

const getSeverityColor = (severity: string): ChipProps["color"] => {
  if (severity === "critical" || severity === "high") return "error";
  if (severity === "medium") return "warning";
  return "success";
};

export default function IncidentResult({ result }: IncidentResultProps) {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
      <Card sx={{ borderRadius: 3 }}>
        <CardContent sx={{ p: 3, textAlign: "center" }}>
          <Typography variant="h5" sx={{ fontWeight: 700 }} gutterBottom>
            Incident Summary
          </Typography>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 1.5,
              mb: 2,
            }}
          >
            <Chip
              label={result.severity.toUpperCase()}
              color={getSeverityColor(result.severity)}
            />
            <Chip label={`Confidence: ${result.confidence}`} />
          </Box>

          <Typography variant="subtitle2" color="text.secondary">
            Root Cause
          </Typography>

          <Typography variant="body1" sx={{ mt: 1 }}>
            {result.root_cause}
          </Typography>
        </CardContent>
      </Card>

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
          gap: 3,
        }}
      >
        <Card sx={{ borderRadius: 3, height: "100%" }}>
          <CardContent sx={{ p: 3, textAlign: "center" }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }} gutterBottom>
              Tools Used
            </Typography>

            <Box
              sx={{
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                gap: 1,
                mt: 2,
              }}
            >
              {result.tools_used.map((tool) => (
                <Chip key={tool} label={tool} variant="outlined" />
              ))}
            </Box>
          </CardContent>
        </Card>

        <InvestigationTimeline steps={result.investigation_steps} />
      </Box>

      <Card sx={{ borderRadius: 3 }}>
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h5" align="center" sx={{ fontWeight: 700 }} gutterBottom>
            Recommendations
          </Typography>

          <List>
            {result.recommendations.map((recommendation, index) => (
              <Box key={`${recommendation.action}-${index}`}>
                <ListItem alignItems="flex-start" disableGutters>
                  <ListItemText
                    primary={
                      <Box
                        sx={{
                          display: "flex",
                          alignItems: "center",
                          gap: 1,
                          flexWrap: "wrap",
                        }}
                      >
                        <Typography sx={{ fontWeight: 700 }}>
                          {recommendation.action}
                        </Typography>
                        <Chip
                          size="small"
                          label={recommendation.priority}
                          color={
                            recommendation.priority === "high"
                              ? "error"
                              : recommendation.priority === "medium"
                                ? "warning"
                                : "success"
                          }
                        />
                      </Box>
                    }
                    secondary={recommendation.reason}
                  />
                </ListItem>

                {index < result.recommendations.length - 1 && <Divider />}
              </Box>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
}