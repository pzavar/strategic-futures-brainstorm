import { useState, useMemo } from 'react';
import { Combobox } from '@headlessui/react';
import { searchCompanies, normalizeCompanyName, type Company } from '../utils/companySearch';

interface CompanyInputProps {
  onSubmit: (companyName: string) => void;
  loading?: boolean;
}

export const CompanyInput = ({ onSubmit, loading = false }: CompanyInputProps) => {
  const [query, setQuery] = useState('');
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);

  // Perform fuzzy search as user types
  const filteredCompanies = useMemo(() => {
    if (!query.trim()) {
      return [];
    }
    return searchCompanies(query, 10);
  }, [query]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    let companyNameToSubmit: string | null = null;
    
    // If a company is selected, use it
    if (selectedCompany) {
      companyNameToSubmit = selectedCompany.name;
    } else if (query.trim()) {
      // Otherwise, try to normalize the query
      companyNameToSubmit = normalizeCompanyName(query);
    }
    
    if (companyNameToSubmit) {
      onSubmit(companyNameToSubmit);
      setQuery('');
      setSelectedCompany(null);
    }
  };

  const handleSelect = (company: Company | null) => {
    if (company) {
      setSelectedCompany(company);
      setQuery(company.name);
    } else {
      setSelectedCompany(null);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="flex gap-4">
        <Combobox
          value={selectedCompany}
          onChange={handleSelect}
          disabled={loading}
        >
          <div className="relative flex-1">
            <Combobox.Input
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="Enter company name or ticker (e.g., Apple, AAPL, Aple)"
              displayValue={(company: Company | null) => {
                if (company) {
                  return company.name;
                }
                return query;
              }}
              onChange={(e) => {
                setQuery(e.target.value);
                setSelectedCompany(null);
              }}
              {...(loading && { readOnly: true, tabIndex: -1 })}
            />
            {query && filteredCompanies.length > 0 && (
              <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                {filteredCompanies.map((result, idx) => (
                  <Combobox.Option
                    key={`${result.company.ticker}-${idx}`}
                    value={result.company}
                    className={({ active }) =>
                      `relative cursor-pointer select-none py-2 pl-4 pr-4 ${
                        active ? 'bg-primary-600 text-white' : 'text-gray-900'
                      }`
                    }
                  >
                    {({ selected, active }) => (
                      <div className="flex items-center justify-between">
                        <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                          {result.company.name}
                        </span>
                        <span className={`text-sm ${active ? 'text-primary-100' : 'text-gray-500'}`}>
                          {result.company.ticker}
                        </span>
                      </div>
                    )}
                  </Combobox.Option>
                ))}
              </Combobox.Options>
            )}
            {query && filteredCompanies.length === 0 && query.trim().length > 0 && (
              <div className="absolute z-10 mt-1 w-full rounded-md bg-white py-2 px-4 text-sm text-gray-500 shadow-lg ring-1 ring-black ring-opacity-5">
                No companies found. Try a different search term.
              </div>
            )}
          </div>
        </Combobox>
        <button
          type="submit"
          disabled={loading || (!selectedCompany && !normalizeCompanyName(query))}
          className="px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </form>
  );
};

