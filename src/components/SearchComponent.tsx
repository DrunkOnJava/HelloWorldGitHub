import React, { useState } from "react";
import { compounds } from "../data/compounds";
import { getPath } from "../utils/paths";

interface Props {
  placeholder?: string;
}

interface Compound {
  name: string;
  slug: string;
  category: string;
  description: string;
  anabolicRating: number;
  androgenicRating: number;
  halfLife: string;
}

function SearchComponent({ placeholder = "Search..." }: Props) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<Compound[]>([]);

  function handleSearch(event: React.ChangeEvent<HTMLInputElement>) {
    const term = event.target.value.toLowerCase();
    setSearchTerm(term);
    console.log('Search term:', term);
    if (term.length > 0) {
      const results = compounds.filter((compound) =>
        compound.name.toLowerCase().includes(term) ||
        compound.description.toLowerCase().includes(term)
      );
      console.log('Search results:', results);
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  }

  return (
    <div className="relative">
      <div className="relative flex items-center">
        <input
          type="text"
          placeholder={placeholder}
          value={searchTerm}
          onChange={handleSearch}
          className="bg-gray-800/80 focus:bg-gray-700 text-white rounded-xl py-2.5 pl-10 pr-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all duration-200 placeholder-gray-400"
        />
        <svg
          className="absolute left-3 w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
      {searchResults.length > 0 && (
        <ul className="absolute left-0 mt-2 w-full bg-gray-800/95 backdrop-blur-sm rounded-xl shadow-lg shadow-black/50 z-50 border border-gray-700/50 divide-y divide-gray-700/50 overflow-hidden transition-all duration-200">
          {searchResults.map((compound) => (
            <li key={compound.slug}>
              <a
                href={getPath(`/compounds/${compound.slug}`)}
                className="block px-4 py-3 text-gray-200 hover:text-white hover:bg-gray-700/50 transition-colors duration-200"
              >
                <div className="font-medium">{compound.name}</div>
                <div className="text-sm text-gray-400 mt-0.5">
                  {compound.category} • {compound.halfLife} half-life
                </div>
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SearchComponent;
