import type { FC } from 'react';

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface HeaderProps {
  breadcrumbs: BreadcrumbItem[];
  title?: string;
  subtitle?: string;
}

export const Header: FC<HeaderProps> = ({
  breadcrumbs,
  title,
  subtitle,
}) => {
  return (
    <header className="mb-8">
      <nav className="mb-4">
        <ol className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
          {breadcrumbs.map((item, index) => (
            <li key={index}>
              {index > 0 && <span className="mx-2">/</span>}
              {item.href ? (
                <a
                  href={item.href}
                  className="hover:text-blue-600 dark:hover:text-blue-400"
                >
                  {item.label}
                </a>
              ) : (
                <span className="text-gray-900 dark:text-white font-medium">
                  {item.label}
                </span>
              )}
            </li>
          ))}
        </ol>
      </nav>

      {title && (
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-2 text-lg text-gray-600 dark:text-gray-400">
              {subtitle}
            </p>
          )}
        </div>
      )}
    </header>
  );
};
