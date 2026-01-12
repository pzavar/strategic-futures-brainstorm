export const TermsOfUse = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Terms of Use</h1>
          <p className="text-gray-600 mb-8">Last updated: {new Date().toLocaleDateString()}</p>

          <div className="prose prose-lg max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-700 mb-4">
                By accessing and using Strategic Futures AI ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Prohibited Activities</h2>
              <p className="text-gray-700 mb-4">You agree NOT to:</p>
              <ul className="list-disc pl-6 space-y-2 text-gray-700 mb-4">
                <li>Use any automated systems, bots, scripts, or software to access, scrape, or interact with the Service without explicit written permission</li>
                <li>Attempt to reverse engineer, decompile, or disassemble any part of the Service</li>
                <li>Use the Service to generate content that is illegal, harmful, threatening, abusive, or violates any laws or regulations</li>
                <li>Impersonate any person or entity or falsely state or misrepresent your affiliation with any person or entity</li>
                <li>Interfere with or disrupt the Service or servers or networks connected to the Service</li>
                <li>Attempt to gain unauthorized access to any portion of the Service, other accounts, computer systems, or networks</li>
                <li>Use the Service for any commercial purpose without our express written consent</li>
                <li>Share your account credentials with others or allow unauthorized access to your account</li>
                <li>Use the Service to transmit any viruses, worms, or malicious code</li>
                <li>Collect or harvest any information from the Service using automated means</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Account Responsibilities</h2>
              <p className="text-gray-700 mb-4">
                You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to:
              </p>
              <ul className="list-disc pl-6 space-y-2 text-gray-700 mb-4">
                <li>Provide accurate, current, and complete information during registration</li>
                <li>Maintain and promptly update your account information</li>
                <li>Notify us immediately of any unauthorized use of your account</li>
                <li>Accept responsibility for all activities that occur under your account</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Acceptable Use</h2>
              <p className="text-gray-700 mb-4">
                The Service is provided for legitimate research and strategic analysis purposes. You may use the Service to:
              </p>
              <ul className="list-disc pl-6 space-y-2 text-gray-700 mb-4">
                <li>Generate strategic analysis and scenarios for companies</li>
                <li>Access and review your analysis history</li>
                <li>Use the generated content for your own research and decision-making purposes</li>
              </ul>
              <p className="text-gray-700 mb-4">
                All use must comply with applicable laws and regulations, and you must respect the intellectual property rights of others.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Intellectual Property</h2>
              <p className="text-gray-700 mb-4">
                The Service, including its original content, features, and functionality, is owned by Strategic Futures AI and is protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.
              </p>
              <p className="text-gray-700 mb-4">
                While you retain ownership of the analyses and content you generate using the Service, you grant us a license to use, store, and process such content as necessary to provide and improve the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Service Availability and Disclaimers</h2>
              <p className="text-gray-700 mb-4">
                We strive to provide reliable service, but we do not guarantee that the Service will be available at all times or that it will be error-free. The Service is provided "as is" and "as available" without warranties of any kind, either express or implied.
              </p>
              <p className="text-gray-700 mb-4">
                The AI-generated content provided by the Service is for informational purposes only and should not be considered as professional advice, financial guidance, or legal counsel. You should consult with qualified professionals before making any decisions based on the Service's output.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Limitation of Liability</h2>
              <p className="text-gray-700 mb-4">
                To the fullest extent permitted by law, Strategic Futures AI shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses resulting from your use of the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Data and Privacy</h2>
              <p className="text-gray-700 mb-4">
                Your use of the Service is also governed by our Privacy Policy. We collect and process your data as described in our Privacy Policy. By using the Service, you consent to such processing.
              </p>
              <p className="text-gray-700 mb-4">
                We reserve the right to monitor usage patterns and may take action if we detect suspicious or prohibited activity, including but not limited to automated access attempts.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Account Termination</h2>
              <p className="text-gray-700 mb-4">
                We reserve the right to suspend or terminate your account at any time, with or without notice, for any violation of these Terms of Use or for any other reason we deem necessary to protect the integrity of the Service or other users.
              </p>
              <p className="text-gray-700 mb-4">
                You may terminate your account at any time by contacting us or using the account deletion features in the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Changes to Terms</h2>
              <p className="text-gray-700 mb-4">
                We reserve the right to modify these Terms of Use at any time. We will notify users of any material changes by posting the new Terms of Use on this page and updating the "Last updated" date. Your continued use of the Service after such modifications constitutes acceptance of the updated terms.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Rate Limiting and Fair Use</h2>
              <p className="text-gray-700 mb-4">
                To ensure fair access for all users and maintain service quality, we may implement rate limiting on API requests and analysis generation. Excessive use that impacts service availability for other users may result in temporary or permanent restrictions on your account.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. Contact Information</h2>
              <p className="text-gray-700 mb-4">
                If you have any questions about these Terms of Use, please contact us through the appropriate channels provided in the Service.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

