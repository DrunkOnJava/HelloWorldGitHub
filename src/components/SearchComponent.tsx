import React, { useState } from "react";
import { compounds } from "../data/compounds";
import { getPath } from "../utils/paths";

interface Props {
  placeholder?: string;
}

interface Compound {
  slug: string;
  title: string;
  description: string;
  properties: {
    formula: string;
    molecularWeight: number;
    halfLife: string;
    anabolicRating: number;
    androgenicRating: number;
  };
}

function SearchComponent({ placeholder = "Search..." }: Props) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<Compound[]>([]);

  function handleSearch(event: React.ChangeEvent<HTMLInputElement>) {
    const term = event.target.value.toLowerCase();
    setSearchTerm(term);
    if (term.length > 0) {
      const results = compounds.filter((compound) => compound.title.toLowerCase().includes(term));
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  }

  return (
    <div className="relative">
      <input
        type="text"
        placeholder={placeholder}
        value={searchTerm}
        onInput={handleSearch}
        className="bg-gray-800 focus:bg-gray-700 text-white rounded-md py-2 px-4 w-full focus:outline-none"
      />
      {searchResults.length > 0 && (
        <ul className="absolute left-0 mt-2 w-full bg-gray-800 rounded-md shadow-lg z-10">
          {searchResults.map((compound) => (
            <li key={compound.slug} className="py-1">
              <a
                href={getPath(`/compounds/${compound.slug}`)}
                className="block px-4 py-2 text-white hover:bg-gray-700"
              >
                {compound.title}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SearchComponent;
