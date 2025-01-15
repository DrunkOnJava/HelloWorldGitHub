export const compoundData = {
  name: "Nandrolone",
  category: "Anabolic Steroid",
  overview: {
    chemicalName: "19-nortestosterone",
    halfLife: {
      decanoate: "15 days",
      phenylpropionate: "2-3 days",
    },
    detectionTime: "18 months",
  },
  dosageGuidelines: {
    calculator: {
      experienceLevels: ["Beginner", "Intermediate", "Advanced"],
      goals: ["Bulking", "Cutting", "Recomposition"],
      recommendations: {
        beginner: "200-300mg per week",
        intermediate: "300-400mg per week",
        advanced: "400-600mg per week",
      },
    },
  },
  effects: {
    benefits: [
      {
        title: "Joint Health",
        description:
          "Increased collagen synthesis and joint lubrication for better recovery.",
      },
      {
        title: "Lean Mass Gains",
        description:
          "Steady, quality muscle gains with less water retention than testosterone.",
      },
      {
        title: "Recovery Enhancement",
        description:
          "Significant improvement in recovery time between training sessions.",
      },
    ],
  },
  sideEffects: {
    warning:
      "Regular blood work monitoring is essential. Nandrolone can mask joint issues due to its pain-relieving properties.",
    categories: [
      {
        type: "Progestin Activity",
        description:
          "Can cause progesterone-related side effects, requiring careful estrogen management.",
      },
      {
        type: "Androgenic",
        description: "Lower androgenic side effects compared to testosterone.",
      },
      {
        type: "HPTA Suppression",
        description:
          "Strong suppression of natural testosterone production, requiring thorough PCT.",
      },
    ],
  },
  pct: {
    protocol: [
      "Wait 3 weeks after last nandrolone injection (if decanoate)",
      "HCG: 1000IU EOD for 2 weeks before starting SERMs",
      "Nolvadex: 40/40/20/20 mg per day (weeks 1-4)",
      "Clomid: 100/100/50/50 mg per day (weeks 1-4)",
    ],
  },
  studies: [
    {
      title: "Joint Health Benefits",
      description:
        "Research shows nandrolone's positive effects on collagen synthesis and joint repair mechanisms.",
      source: "Journal of Orthopaedic Research, 2018",
    },
    {
      title: "Muscle Growth Mechanisms",
      description:
        "Studies indicate unique muscle-building properties with lower androgenic activity compared to testosterone.",
      source: "Endocrine Reviews, 2020",
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
