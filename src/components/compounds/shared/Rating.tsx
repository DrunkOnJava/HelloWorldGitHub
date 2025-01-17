import type { FC } from 'react';

interface RatingProps {
  label: string;
  value: number;
  maxValue?: number;
  colorClass: string;
  className?: string;
}

export const Rating: FC<RatingProps> = ({
  label,
  value,
  maxValue = 500,
  colorClass,
  className = '',
}) => {
  const percentage = Math.min(100, (value / maxValue) * 100);

  return (
    <div className={`flex flex-col ${className}`}>
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
        </span>
        <span className="text-sm font-bold text-gray-900 dark:text-white">
          {value}
        </span>
      </div>
      <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-300 ${colorClass}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
