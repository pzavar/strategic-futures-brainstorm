import { Link } from 'react-router-dom';

export const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Strategic Futures AI
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto mb-8">
            Generate diverse future scenarios and strategic recommendations for any company
            using advanced AI research and analysis
          </p>
            <Link
              to="/app"
              className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-primary-700 transition-colors shadow-lg hover:shadow-xl"
            >
            Get Started
            </Link>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered 3-agent pipeline analyzes companies and generates comprehensive strategic insights
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mt-12">
            {/* Step 1: Research */}
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                1
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Research Agent
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Conducts comprehensive research on your company, including industry analysis, 
                competitive landscape, emerging trends, and market dynamics using real-time web search.
              </p>
            </div>

            {/* Step 2: Scenarios */}
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                2
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Scenario Agent
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Generates 4 diverse future scenarios exploring different combinations of technology evolution, 
                market dynamics, regulatory environments, and economic conditions.
              </p>
            </div>

            {/* Step 3: Strategies */}
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-8 shadow-lg">
              <div className="flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6 mx-auto">
                3
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Strategy Agent
              </h3>
              <p className="text-gray-700 text-center leading-relaxed">
                Develops 2-3 actionable strategic recommendations for each scenario, including 
                expected impact, key risks, and implementation considerations.
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
              What You Can Expect
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Comprehensive strategic analysis powered by advanced AI
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Comprehensive Research</h3>
              <p className="text-gray-600">
                Industry analysis, competitive landscape, and emerging trends gathered from real-time web sources
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Diverse Scenarios</h3>
              <p className="text-gray-600">
                4 distinct future scenarios exploring different strategic possibilities and market conditions
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
              <div className="text-4xl mb-4">💡</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Actionable Strategies</h3>
              <p className="text-gray-600">
                2-3 concrete strategic recommendations per scenario with impact analysis and risk assessment
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
              Getting Started
            </h2>
            <p className="text-lg text-gray-600">
              Follow these simple steps to generate your strategic analysis
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
                <h3 className="text-xl font-bold text-gray-900 mb-2">Enter a Company Name</h3>
                <p className="text-gray-600">
                  Simply enter the name of any company you want to analyze. Our AI will handle the rest.
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
                <h3 className="text-xl font-bold text-gray-900 mb-2">Watch the Magic Happen</h3>
                <p className="text-gray-600">
                  Follow along in real-time as our 3-agent pipeline researches, generates scenarios, 
                  and develops strategic recommendations. The process typically takes 2-5 minutes.
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
                <h3 className="text-xl font-bold text-gray-900 mb-2">Review Your Analysis</h3>
                <p className="text-gray-600">
                  Explore the generated scenarios and strategies. Save your analysis history and 
                  compare insights across different companies.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Explore Strategic Futures?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Start generating comprehensive strategic analysis for any company today
          </p>
            <Link
              to="/app"
              className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
            >
            Get Started
            </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm">
              © {new Date().getFullYear()} Strategic Futures AI. All rights reserved.
            </p>
            <div className="flex gap-6">
              <Link
                to="/terms"
                className="text-sm hover:text-white transition-colors"
              >
                Terms of Use
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

