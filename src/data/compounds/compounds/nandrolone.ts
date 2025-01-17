import type { Compound } from '../types';

export const nandrolone: Compound = {
  name: "Nandrolone",
  slug: "nandrolone",
  category: "Anabolic Steroid",
  description:
    "Known for joint healing properties and significant mass gains with lower androgenic effects.",
  anabolicRating: 125,
  androgenicRating: 37,
  halfLife: "Decanoate: 15 days, Phenylpropionate: 2-3 days",
  detectionTime: "18 months",
  dosageRanges: {
    beginner: { min: 200, max: 300, unit: "mg/week" },
    intermediate: { min: 300, max: 400, unit: "mg/week" },
    advanced: { min: 400, max: 600, unit: "mg/week" },
  },
  sideEffects: {
    common: [
      "Suppression",
      "Erectile dysfunction",
      "Mental side effects",
      "Progesterone-related issues"
    ],
    uncommon: [
      "Hair loss",
      "Acne",
      "Cardiovascular strain",
      "Joint pain masking"
    ],
    rare: [
      "Liver toxicity",
      "Severe HPTA suppression"
    ],
  },
  pctRequirements: {
    required: true,
    protocol: "Wait 3 weeks after last injection, HCG 1000IU EOD for 2 weeks, then Nolvadex 40/40/20/20mg and Clomid 100/100/50/50mg for 4 weeks",
    duration: "6-8 weeks",
  },
  interactions: [
    "Must be run with Testosterone base",
    "Caution with 5a-reductase inhibitors",
    "May require prolactin control",
    "Regular blood work essential"
  ],
  references: [
    "DOI: 10.1016/j.steroids.2009.02.006",
    "DOI: 10.2165/00007256-200434050-00003",
    "Journal of Orthopaedic Research, 2018",
    "Endocrine Reviews, 2020"
  ],
};
