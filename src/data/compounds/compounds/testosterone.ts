import type { Compound } from '../types';

export const testosterone: Compound = {
  name: "Testosterone",
  slug: "testosterone",
  category: "Anabolic Steroid",
  description:
    "The foundation of most cycles and the gold standard for TRT. Highly versatile and well-studied.",
  anabolicRating: 100,
  androgenicRating: 100,
  halfLife: "Propionate: 2-3 days, Enanthate: 7-8 days, Cypionate: 8-9 days, Undecanoate: 21 days",
  detectionTime: "3-4 months",
  dosageRanges: {
    beginner: { min: 300, max: 500, unit: "mg/week" },
    intermediate: { min: 500, max: 750, unit: "mg/week" },
    advanced: { min: 750, max: 1000, unit: "mg/week" },
  },
  sideEffects: {
    common: [
      "Acne",
      "Hair loss",
      "Gynecomastia",
      "Increased body hair growth",
      "Water retention",
    ],
    uncommon: [
      "High blood pressure",
      "Mood changes",
      "Elevated estrogen",
      "Cholesterol changes"
    ],
    rare: [
      "Liver stress",
      "Sleep apnea",
      "Cardiovascular issues"
    ],
  },
  pctRequirements: {
    required: true,
    protocol: "Wait 2-3 weeks after last injection, HCG 1000IU EOD for 2 weeks, then Nolvadex 40/40/20/20mg and Clomid 50/50/25/25mg for 4 weeks",
    duration: "4-6 weeks",
  },
  interactions: [
    "AI may be needed for estrogen management",
    "HCG recommended for testicular function",
    "Regular blood work monitoring required"
  ],
  references: [
    "DOI: 10.1056/NEJMoa1206168",
    "DOI: 10.1210/jc.2018-00229",
    "New England Journal of Medicine, 2019",
    "Journal of Clinical Endocrinology & Metabolism, 2021"
  ],
};
