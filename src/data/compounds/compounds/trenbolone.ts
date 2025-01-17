import type { Compound } from '../types';

export const trenbolone: Compound = {
  name: "Trenbolone",
  slug: "trenbolone",
  category: "Anabolic Steroid",
  description:
    "Powerful compound known for dramatic physique changes and strength gains. Advanced users only.",
  anabolicRating: 500,
  androgenicRating: 500,
  halfLife: "Acetate: 1 day, Enanthate: 7-10 days, Hexahydrobenzylcarbonate: 14 days",
  detectionTime: "5-6 months",
  dosageRanges: {
    beginner: { min: 200, max: 300, unit: "mg/week" },
    intermediate: { min: 300, max: 500, unit: "mg/week" },
    advanced: { min: 500, max: 700, unit: "mg/week" },
  },
  sideEffects: {
    common: [
      "Insomnia",
      "Night sweats",
      "Anxiety",
      "Aggression",
      "Cardiovascular strain"
    ],
    uncommon: [
      "Respiratory issues",
      "Hair loss",
      "Acne",
      "Tren cough"
    ],
    rare: [
      "Kidney stress",
      "Severe cardiovascular issues",
      "Prolactin-related sides"
    ],
  },
  pctRequirements: {
    required: true,
    protocol: "Wait 2-3 weeks after last injection, HCG 1500IU EOD for 2 weeks, then Nolvadex 40/40/20/20mg and Clomid 100/100/50/50mg for 4 weeks. Consider Cabergoline for prolactin.",
    duration: "8 weeks",
  },
  interactions: [
    "Must be run with Testosterone base",
    "Careful with other 19-nors",
    "May require prolactin control",
    "Requires extensive health monitoring"
  ],
  references: [
    "DOI: 10.1530/eje.1.02338",
    "DOI: 10.1016/j.jsbmb.2011.03.015",
    "Journal of Animal Science, 2019",
    "Endocrinology Reviews, 2021"
  ],
};
