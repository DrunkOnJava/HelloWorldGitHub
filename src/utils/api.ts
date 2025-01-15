export interface ResearchPaper {
  id: string;
  title: string;
  abstract: string;
  url: string;
  authors?: string[];
  publicationDate?: string;
  journal?: string;
}

export async function fetchData<T>(url: string): Promise<T> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return (await response.json()) as T;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

export async function getResearchPaper(paperId: string): Promise<ResearchPaper> {
  // In a real application, this would fetch data from an API
  console.log(`Fetching research paper with ID: ${paperId}`);
  return {
    id: paperId,
    title: `Research Paper ${paperId}`,
    abstract: "This is a placeholder abstract for the research paper.",
    url: `https://example.com/research/${paperId}`,
    authors: ["John Doe", "Jane Smith"],
    publicationDate: "2023-01-15",
    journal: "Journal of Applied Science",
  };
}

export async function searchResearchPapers(query: string): Promise<ResearchPaper[]> {
  // Placeholder for searching research papers
  console.log(`Searching research papers with query: ${query}`);
  const mockPapers: ResearchPaper[] = Array.from({ length: 5 }, (_, i) => ({
    id: `paper-${i + 1}`,
    title: `Research Paper ${i + 1} on ${query}`,
    abstract: `This is a placeholder abstract for research paper ${i + 1} related to ${query}.`,
    url: `https://example.com/search-results?q=${query}`,
    authors: ["Researcher A", "Researcher B"],
    publicationDate: "2022-11-20",
    journal: "International Journal of Research",
  }));
  return mockPapers;
}
