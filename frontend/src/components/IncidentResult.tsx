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
import type { IncidentAnalysis } from "../types/incident";
import InvestigationTimeline from "./InvestigationTimeline";

interface IncidentResultProps {
  result: IncidentAnalysis;
}

export default function IncidentResult({ result }: IncidentResultProps) {
  return (
    <Box display="flex" flexDirection="column" gap={3}>
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <Typography variant="h6">Incident Summary</Typography>
            <Chip label={result.severity.toUpperCase()} color="error" />
            <Chip label={`Confidence: ${result.confidence}`} />
          </Box>

          <Typography variant="subtitle2" color="text.secondary">
            Root Cause
          </Typography>
          <Typography variant="body1" mt={1}>
            {result.root_cause}
          </Typography>
        </CardContent>
      </Card>

      <InvestigationTimeline steps={result.investigation_steps} />

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recommendations
          </Typography>

          <List>
            {result.recommendations.map((recommendation, index) => (
              <Box key={`${recommendation.action}-${index}`}>
                <ListItem alignItems="flex-start">
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center" gap={1}>
                        <Typography fontWeight={600}>
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
                                : "default"
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

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Tools Used
          </Typography>

          <Box display="flex" flexWrap="wrap" gap={1}>
            {result.tools_used.map((tool) => (
              <Chip key={tool} label={tool} variant="outlined" />
            ))}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}