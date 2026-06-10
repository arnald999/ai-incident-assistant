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
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Investigation Timeline
        </Typography>

        <List>
          {steps.map((step, index) => (
            <ListItem key={`${step}-${index}`}>
              <ListItemIcon>
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