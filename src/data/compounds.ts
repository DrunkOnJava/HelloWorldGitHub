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
  },
  {
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
  },
  {
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
  },
];
