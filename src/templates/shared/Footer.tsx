import type { FC } from 'react';

interface FooterProps {
  lastUpdated?: Date;
  showDisclaimer?: boolean;
  className?: string;
}

export const Footer: FC<FooterProps> = ({
  lastUpdated = new Date(),
  showDisclaimer = true,
  className = '',
}) => {
  return (
    <footer className={`mt-12 text-center text-sm text-gray-600 dark:text-gray-400 ${className}`}>
      <div className="max-w-3xl mx-auto px-4">
        {lastUpdated && (
          <p>Last updated: {lastUpdated.toLocaleDateString()}</p>
        )}

        {showDisclaimer && (
          <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
            <p className="font-medium text-yellow-800 dark:text-yellow-200 mb-2">
              Important Disclaimer
            </p>
            <p className="text-sm text-yellow-700 dark:text-yellow-300">
              This information is for educational and harm reduction purposes only.
              The use of anabolic steroids without proper medical supervision can be dangerous.
              Always consult with qualified healthcare professionals before making any decisions
              about your health.
            </p>
          </div>
        )}

        <div className="mt-6 border-t border-gray-200 dark:border-gray-700 pt-6">
          <nav className="flex justify-center space-x-4">
            <a
              href="/legal/terms"
              className="hover:text-blue-600 dark:hover:text-blue-400"
            >
              Terms of Use
            </a>
            <a
              href="/legal/disclaimer"
              className="hover:text-blue-600 dark:hover:text-blue-400"
            >
              Full Disclaimer
            </a>
            <a
              href="/safety"
              className="hover:text-blue-600 dark:hover:text-blue-400"
            >
              Safety Information
            </a>
          </nav>
        </div>
      </div>
    </footer>
  );
};
