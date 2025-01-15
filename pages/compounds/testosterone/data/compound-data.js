export const compoundData = {
  name: "Testosterone",
  category: "Anabolic Steroid",
  overview: {
    chemicalName: "4-Androsten-17β-ol-3-one",
    halfLife: {
      propionate: "2-3 days",
      enanthate: "7-8 days",
      cypionate: "8-9 days",
      undecanoate: "21 days",
    },
    detectionTime: "3-4 months",
  },
  dosageGuidelines: {
    calculator: {
      experienceLevels: ["Beginner", "Intermediate", "Advanced"],
      goals: ["Bulking", "Cutting", "TRT"],
      recommendations: {
        beginner: "300-500mg per week",
        intermediate: "500-750mg per week",
        advanced: "750-1000mg per week",
        trt: "100-200mg per week",
      },
    },
  },
  effects: {
    benefits: [
      {
        title: "Muscle Growth",
        description:
          "Primary anabolic hormone responsible for muscle protein synthesis and growth.",
      },
      {
        title: "Strength Enhancement",
        description:
          "Significant increases in muscular strength and power output.",
      },
      {
        title: "Recovery",
        description:
          "Enhanced recovery capabilities and reduced muscle breakdown.",
      },
      {
        title: "Bone Density",
        description: "Improved bone mineral density and skeletal strength.",
      },
      {
        title: "Mental Well-being",
        description:
          "Enhanced mood, motivation, and sense of well-being when properly balanced.",
      },
    ],
  },
  sideEffects: {
    warning:
      "While testosterone is the most well-studied anabolic steroid, proper monitoring and management of side effects is still essential.",
    categories: [
      {
        type: "Estrogenic",
        description:
          "Can aromatize into estrogen, potentially causing water retention, gynecomastia, and blood pressure issues.",
      },
      {
        type: "Androgenic",
        description:
          "May cause acne, male pattern baldness in genetically predisposed individuals, and body hair growth.",
      },
      {
        type: "Cardiovascular",
        description:
          "Can affect cholesterol levels and hematocrit, requiring regular blood work monitoring.",
      },
      {
        type: "Hormonal",
        description:
          "Natural testosterone production suppression requiring proper PCT protocol.",
      },
    ],
  },
  pct: {
    protocol: [
      "Wait 2 weeks after last testosterone injection (if propionate)",
      "Wait 3 weeks after last injection (if enanthate/cypionate)",
      "HCG: 1000IU EOD for 2 weeks before starting SERMs",
      "Nolvadex: 40/40/20/20 mg per day (weeks 1-4)",
      "Clomid: 50/50/25/25 mg per day (weeks 1-4)",
      "Consider AI during cycle for estrogen management",
    ],
  },
  studies: [
    {
      title: "Muscle Protein Synthesis",
      description:
        "Research confirms testosterone's direct role in stimulating muscle protein synthesis and reducing protein breakdown.",
      source: "New England Journal of Medicine, 2019",
    },
    {
      title: "Dose Response Relationship",
      description:
        "Studies demonstrate clear dose-dependent relationship between testosterone levels and muscle mass gains.",
      source: "Journal of Clinical Endocrinology & Metabolism, 2021",
    },
    {
      title: "Long-term Safety",
      description:
        "Long-term studies show relative safety of therapeutic testosterone use when properly monitored.",
      source: "European Journal of Endocrinology, 2020",
    },
  ],
  quickNavigation: [
    {
      title: "Overview",
      id: "overview",
    },
    {
      title: "Dosage Guidelines",
      id: "dosage",
    },
    {
      title: "Effects & Benefits",
      id: "effects",
    },
    {
      title: "Side Effects",
      id: "side-effects",
    },
    {
      title: "PCT Requirements",
      id: "pct",
    },
    {
      title: "Studies & Research",
      id: "studies",
    },
  ],
};
