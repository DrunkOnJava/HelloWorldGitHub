export interface Protocol {
  id: string;
  name: string;
  description?: string;
  author?: string;
  createdDate?: Date;
  tags?: string[];
}

export interface CycleCompound {
  name: string;
  dosage: string;
  frequency: string;
}

export interface CyclePhase {
  name: string;
  description?: string;
  goal?: string;
  durationWeeks: number;
  compounds: CycleCompound[];
}

export interface CyclePlan {
  id: string;
  userId?: string;
  protocolId: string;
  startDate: Date;
  phases: CyclePhase[];
  notes?: string;
  lastUpdated?: Date;
}

export const sampleProtocols: Protocol[] = [
  {
    id: "protocol-1",
    name: "Beginner Cycle",
    description: "A basic cycle for beginners.",
    author: "AI Assistant",
    createdDate: new Date(),
    tags: ["beginner", "testosterone"],
  },
  {
    id: "protocol-2",
    name: "Intermediate Cycle",
    description: "An example of an intermediate cycle.",
    author: "AI Assistant",
    createdDate: new Date(),
    tags: ["intermediate", "testosterone", "deca"],
  },
];

export const sampleCyclePlan: CyclePlan = {
  id: "cycle-plan-1",
  protocolId: "protocol-1",
  startDate: new Date(),
  phases: [
    {
      name: "Bulking",
      description: "Initial phase to build muscle mass.",
      goal: "Mass gain",
      durationWeeks: 12,
      compounds: [{ name: "Testosterone Enanthate", dosage: "500mg", frequency: "weekly" }],
    },
    {
      name: "PCT",
      description: "Post cycle therapy to restore natural hormone production.",
      goal: "Hormone recovery",
      durationWeeks: 4,
      compounds: [
        { name: "Nolvadex", dosage: "40mg", frequency: "daily" },
        { name: "Clomid", dosage: "50mg", frequency: "daily" },
      ],
    },
  ],
  notes: "Example of a beginner cycle plan.",
  lastUpdated: new Date(),
};
