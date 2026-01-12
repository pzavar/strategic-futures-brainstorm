import Fuse from 'fuse.js';
import { SP500_COMPANIES, Company } from '../data/sp500-companies';

// Re-export Company type for convenience
export type { Company };

// Prepare search data with all searchable fields
const searchData = SP500_COMPANIES.map(company => ({
  ...company,
  // Create a searchable string that includes name, ticker, and aliases
  searchText: [
    company.name,
    company.ticker,
    ...(company.aliases || [])
  ].join(' ').toLowerCase()
}));

// Configure Fuse.js for fuzzy search
const fuse = new Fuse(searchData, {
  keys: [
    { name: 'name', weight: 0.5 },
    { name: 'ticker', weight: 0.3 },
    { name: 'aliases', weight: 0.2 },
    { name: 'searchText', weight: 0.1 }
  ],
  threshold: 0.4, // Lower = more strict, higher = more lenient (0.0-1.0)
  includeScore: true,
  minMatchCharLength: 1,
  ignoreLocation: true,
  // Normalize to handle case-insensitive matching
  getFn: (obj, path) => {
    const value = Fuse.config.getFn(obj, path);
    return typeof value === 'string' ? value.toLowerCase() : value;
  }
});

export interface SearchResult {
  company: Company;
  score: number;
}

/**
 * Search for companies using fuzzy matching
 * @param query - The search query (company name, ticker, or alias)
 * @param limit - Maximum number of results to return (default: 10)
 * @returns Array of matching companies with scores
 */
export function searchCompanies(query: string, limit: number = 10): SearchResult[] {
  if (!query || query.trim().length === 0) {
    return [];
  }

  const results = fuse.search(query.trim(), { limit });
  
  return results.map(result => ({
    company: {
      name: result.item.name,
      ticker: result.item.ticker,
      aliases: result.item.aliases
    },
    score: result.score || 1
  }));
}

/**
 * Find the best matching company for a given query
 * Returns the canonical company name if a match is found, otherwise returns null
 * @param query - The search query (company name, ticker, or alias)
 * @returns The canonical company name or null if no match found
 */
export function normalizeCompanyName(query: string): string | null {
  if (!query || query.trim().length === 0) {
    return null;
  }

  const trimmedQuery = query.trim();
  
  // First, try exact ticker match (case-insensitive)
  const exactTickerMatch = SP500_COMPANIES.find(
    company => company.ticker.toLowerCase() === trimmedQuery.toUpperCase()
  );
  if (exactTickerMatch) {
    return exactTickerMatch.name;
  }

  // Try exact name match (case-insensitive)
  const exactNameMatch = SP500_COMPANIES.find(
    company => company.name.toLowerCase() === trimmedQuery.toLowerCase()
  );
  if (exactNameMatch) {
    return exactNameMatch.name;
  }

  // Try exact alias match (case-insensitive)
  const exactAliasMatch = SP500_COMPANIES.find(
    company => company.aliases?.some(
      alias => alias.toLowerCase() === trimmedQuery.toLowerCase()
    )
  );
  if (exactAliasMatch) {
    return exactAliasMatch.name;
  }

  // Use fuzzy search for typos and variations
  const results = searchCompanies(trimmedQuery, 1);
  if (results.length > 0 && results[0].score < 0.5) {
    return results[0].company.name;
  }

  return null;
}

/**
 * Get all companies (for dropdown display)
 * @returns Array of all companies
 */
export function getAllCompanies(): Company[] {
  return SP500_COMPANIES;
}

