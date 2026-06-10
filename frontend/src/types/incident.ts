export interface Recommendation {
  action: string;
  reason: string;
  priority: string;
}

export interface IncidentAnalysis {
  severity: string;
  root_cause: string;
  confidence: number;
  recommendations: Recommendation[];
  tools_used: string[];
  investigation_steps: string[];
}