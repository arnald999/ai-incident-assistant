import {
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

interface InvestigationTimelineProps {
  steps: string[];
}

export default function InvestigationTimeline({
  steps,
}: InvestigationTimelineProps) {
  return (
    <Card sx={{ borderRadius: 3, height: "100%" }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h5" align="center" sx={{ fontWeight: 700 }} gutterBottom>
          Investigation Timeline
        </Typography>

        <List>
          {steps.map((step, index) => (
            <ListItem key={`${step}-${index}`} alignItems="flex-start">
              <ListItemIcon sx={{ minWidth: 36 }}>
                <CheckCircleIcon color="success" />
              </ListItemIcon>
              <ListItemText primary={step} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}