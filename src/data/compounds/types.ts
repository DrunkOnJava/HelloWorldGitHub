export interface Compound {
  name: string;
  slug: string;
  category: string;
  description: string;
  anabolicRating: number;
  androgenicRating: number;
  halfLife: string;
  detectionTime: string;
  dosageRanges: {
    beginner: { min: number; max: number; unit: string };
    intermediate: { min: number; max: number; unit: string };
    advanced: { min: number; max: number; unit: string };
  };
  sideEffects: {
    common: string[];
    uncommon: string[];
    rare: string[];
  };
  pctRequirements: {
    required: boolean;
    protocol: string;
    duration: string;
  };
  interactions: string[];
  references: string[];
}
