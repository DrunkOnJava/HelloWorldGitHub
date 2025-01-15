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

export const compounds: Compound[] = [
  {
    name: "Testosterone",
    slug: "testosterone",
    category: "Anabolic Steroid",
    description:
      "The foundation of most cycles and the gold standard for TRT. Highly versatile and well-studied.",
    anabolicRating: 100,
    androgenicRating: 100,
    halfLife: "4.5-5 days (Enanthate)",
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
      ],
      uncommon: ["High blood pressure", "Water retention", "Mood changes"],
      rare: ["Liver stress", "Sleep apnea"],
    },
    pctRequirements: {
      required: true,
      protocol: "Standard PCT protocol",
      duration: "4-6 weeks",
    },
    interactions: ["AI may be needed", "HCG recommended"],
    references: ["DOI: 10.1056/NEJMoa1206168", "DOI: 10.1210/jc.2018-00229"],
  },
  {
    name: "Nandrolone",
    slug: "nandrolone",
    category: "Anabolic Steroid",
    description:
      "Known for joint healing properties and significant mass gains with lower androgenic effects.",
    anabolicRating: 125,
    androgenicRating: 37,
    halfLife: "6-7 days (Decanoate)",
    detectionTime: "18 months",
    dosageRanges: {
      beginner: { min: 200, max: 400, unit: "mg/week" },
      intermediate: { min: 400, max: 600, unit: "mg/week" },
      advanced: { min: 600, max: 800, unit: "mg/week" },
    },
    sideEffects: {
      common: ["Suppression", "Erectile dysfunction", "Mental side effects"],
      uncommon: ["Hair loss", "Acne", "Cardiovascular strain"],
      rare: ["Liver toxicity", "Progesterone-related sides"],
    },
    pctRequirements: {
      required: true,
      protocol: "Extended PCT protocol",
      duration: "6-8 weeks",
    },
    interactions: [
      "Must be run with Testosterone base",
      "Caution with 5a-reductase inhibitors",
    ],
    references: [
      "DOI: 10.1016/j.steroids.2009.02.006",
      "DOI: 10.2165/00007256-200434050-00003",
    ],
  },
  {
    name: "Trenbolone",
    slug: "trenbolone",
    category: "Anabolic Steroid",
    description:
      "Powerful compound known for dramatic physique changes and strength gains. Advanced users only.",
    anabolicRating: 500,
    androgenicRating: 500,
    halfLife: "2-3 days (Acetate)",
    detectionTime: "5-6 months",
    dosageRanges: {
      beginner: { min: 200, max: 300, unit: "mg/week" },
      intermediate: { min: 300, max: 500, unit: "mg/week" },
      advanced: { min: 500, max: 700, unit: "mg/week" },
    },
    sideEffects: {
      common: ["Insomnia", "Night sweats", "Anxiety", "Aggression"],
      uncommon: ["Respiratory issues", "Hair loss", "Acne"],
      rare: ["Kidney stress", "Cardiovascular issues"],
    },
    pctRequirements: {
      required: true,
      protocol: "Aggressive PCT protocol",
      duration: "8 weeks",
    },
    interactions: [
      "Must be run with Testosterone base",
      "Careful with other 19-nors",
    ],
    references: [
      "DOI: 10.1530/eje.1.02338",
      "DOI: 10.1016/j.jsbmb.2011.03.015",
    ],
  },
];
