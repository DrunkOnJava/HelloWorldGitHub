export const compoundData = {
  name: "Trenbolone",
  category: "Anabolic Steroid",
  overview: {
    chemicalName: "19-nor-δ9,11-testosterone",
    halfLife: {
      acetate: "1 day",
      enanthate: "7-10 days",
      hexahydrobenzylcarbonate: "14 days",
    },
    detectionTime: "5-6 months",
  },
  dosageGuidelines: {
    calculator: {
      experienceLevels: ["Intermediate", "Advanced", "Expert"],
      goals: ["Bulking", "Cutting", "Recomposition"],
      recommendations: {
        intermediate: "200-300mg per week",
        advanced: "300-500mg per week",
        expert: "500-700mg per week",
      },
    },
  },
  effects: {
    benefits: [
      {
        title: "Muscle Hardening",
        description:
          "Exceptional ability to increase muscle density and hardness while reducing body fat.",
      },
      {
        title: "Strength Gains",
        description:
          "Dramatic improvements in strength and power output during training.",
      },
      {
        title: "Nutrient Partitioning",
        description:
          "Enhanced nutrient utilization, directing calories toward muscle growth rather than fat storage.",
      },
      {
        title: "Recovery Enhancement",
        description:
          "Accelerated recovery between training sessions due to increased protein synthesis.",
      },
    ],
  },
  sideEffects: {
    warning:
      "Trenbolone is one of the most potent anabolic steroids available. Regular blood work and careful monitoring of side effects is essential.",
    categories: [
      {
        type: "Cardiovascular",
        description:
          "Can significantly impact cardiovascular health through increased blood pressure and altered cholesterol levels.",
      },
      {
        type: "Androgenic",
        description:
          "Strong androgenic effects including potential hair loss, acne, and prostate issues.",
      },
      {
        type: "Mental",
        description:
          "May cause anxiety, insomnia, and increased aggression ('tren rage').",
      },
      {
        type: "Respiratory",
        description:
          "Can cause 'tren cough' and reduced cardiovascular endurance.",
      },
      {
        type: "Hormonal",
        description:
          "Severe suppression of natural testosterone production and potential prolactin-related issues.",
      },
    ],
  },
  pct: {
    protocol: [
      "Wait 2 weeks after last trenbolone injection (if acetate)",
      "Wait 3 weeks after last injection (if enanthate)",
      "HCG: 1500IU EOD for 2 weeks before starting SERMs",
      "Nolvadex: 40/40/20/20 mg per day (weeks 1-4)",
      "Clomid: 100/100/50/50 mg per day (weeks 1-4)",
      "Consider Cabergoline for prolactin management",
    ],
  },
  studies: [
    {
      title: "Nutrient Partitioning Effects",
      description:
        "Research demonstrates trenbolone's unique ability to simultaneously build muscle and reduce fat through enhanced nutrient partitioning.",
      source: "Journal of Animal Science, 2019",
    },
    {
      title: "Protein Synthesis Enhancement",
      description:
        "Studies show significantly increased protein synthesis rates compared to testosterone and other anabolic compounds.",
      source: "Endocrinology Reviews, 2021",
    },
    {
      title: "Metabolic Impact",
      description:
        "Research indicates profound effects on metabolic rate and fat oxidation during both rest and exercise.",
      source: "Metabolism Clinical and Experimental, 2020",
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
