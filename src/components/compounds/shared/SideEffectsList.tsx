import type { FC } from 'react';

interface SideEffects {
  common: string[];
  uncommon: string[];
  rare: string[];
}

interface SideEffectsListProps {
  sideEffects: SideEffects;
  className?: string;
}

export const SideEffectsList: FC<SideEffectsListProps> = ({
  sideEffects,
  className = '',
}) => {
  return (
    <div className={`space-y-4 ${className}`}>
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Common
        </h3>
        <ul className="list-disc list-inside space-y-1">
          {sideEffects.common.map((effect, index) => (
            <li
              key={index}
              className="text-sm text-gray-600 dark:text-gray-400"
            >
              {effect}
            </li>
          ))}
        </ul>
      </div>

      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Uncommon
        </h3>
        <ul className="list-disc list-inside space-y-1">
          {sideEffects.uncommon.map((effect, index) => (
            <li
              key={index}
              className="text-sm text-gray-600 dark:text-gray-400"
            >
              {effect}
            </li>
          ))}
        </ul>
      </div>

      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Rare
        </h3>
        <ul className="list-disc list-inside space-y-1">
          {sideEffects.rare.map((effect, index) => (
            <li
              key={index}
              className="text-sm text-gray-600 dark:text-gray-400"
            >
              {effect}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
