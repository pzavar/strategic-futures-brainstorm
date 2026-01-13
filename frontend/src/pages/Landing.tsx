import { Link } from 'react-router-dom';

export const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Strategic Futures Analysis
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto mb-8">
            An AI-driven framework for generating scenario-based strategic analysis 
            through automated research and synthesis
          </p>
            <Link
              to="/app"
              className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl"
            >
            Access Tool
            </Link>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Methodology
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              A three-stage analytical pipeline for organizational strategic analysis
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mt-12">
            {/* Step 1: Research */}
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                1
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Research Phase
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Automated information gathering on organizational context, industry positioning, 
                competitive environment, and emerging trends through web-based research.
              </p>
            </div>

            {/* Step 2: Scenarios */}
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                2
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Scenario Generation
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Construction of multiple future scenarios based on varying assumptions about technological, 
                market, regulatory, and economic developments.
              </p>
            </div>

            {/* Step 3: Strategies */}
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                3
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Strategy Development
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Synthesis of strategic options for each scenario, with analysis of potential 
                impacts, risks, and implementation factors.
              </p>
            </div>
          </div>

          {/* Flow Arrow */}
          <div className="flex justify-center items-center mt-8 mb-8">
            <div className="hidden md:flex items-center space-x-4 text-primary-600">
              <div className="w-12 h-1 bg-primary-600"></div>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <div className="w-12 h-1 bg-primary-600"></div>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <div className="w-12 h-1 bg-primary-600"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gradient-to-br from-primary-50 to-primary-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Output Components
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Structured analytical outputs for strategic planning and decision support
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Research Synthesis</h3>
              <p className="text-gray-600">
                Compiled analysis of industry context, competitive dynamics, and relevant trend data
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Scenario Set</h3>
              <p className="text-gray-600">
                Multiple plausible future states based on different combinations of key uncertainties
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">💡</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Strategic Options</h3>
              <p className="text-gray-600">
                Scenario-specific strategic recommendations with impact and risk considerations
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Instructions Section */}
      <div className="bg-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Usage Instructions
            </h2>
            <p className="text-lg text-gray-600">
              Process overview for generating strategic analysis
            </p>
          </div>

          <div className="space-y-8">
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-full font-bold text-lg">
                  1
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Input Organization Name</h3>
                <p className="text-gray-600">
                  Enter the name of the organization to be analyzed. The system accepts any publicly-traded 
                  or well-documented organization.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-full font-bold text-lg">
                  2
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Monitor Processing</h3>
                <p className="text-gray-600">
                  Track the three-stage analysis pipeline as it executes. The complete process 
                  typically requires 2-5 minutes depending on data availability.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-full font-bold text-lg">
                  3
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-bold text-gray-900 mb-2">Review Results</h3>
                <p className="text-gray-600">
                  Examine the generated scenarios and strategic recommendations. Results are stored 
                  for reference and comparative analysis across multiple organizations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

