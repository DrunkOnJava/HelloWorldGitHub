import type { FC } from 'react';

interface DosageRange {
  min: number;
  max: number;
  unit: string;
}

interface DosageRanges {
  beginner: DosageRange;
  intermediate: DosageRange;
  advanced: DosageRange;
}

interface DosageTableProps {
  dosageRanges: DosageRanges;
  className?: string;
}

export const DosageTable: FC<DosageTableProps> = ({
  dosageRanges,
  className = '',
}) => {
  return (
    <table className={`w-full border-collapse ${className}`}>
      <thead>
        <tr>
          <th className="px-4 py-2 text-left text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900">
            Experience Level
          </th>
          <th className="px-4 py-2 text-left text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900">
            Dosage Range
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            Beginner
          </td>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            {`${dosageRanges.beginner.min}-${dosageRanges.beginner.max} ${dosageRanges.beginner.unit}`}
          </td>
        </tr>
        <tr>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            Intermediate
          </td>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            {`${dosageRanges.intermediate.min}-${dosageRanges.intermediate.max} ${dosageRanges.intermediate.unit}`}
          </td>
        </tr>
        <tr>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            Advanced
          </td>
          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white border-t border-gray-200 dark:border-gray-700">
            {`${dosageRanges.advanced.min}-${dosageRanges.advanced.max} ${dosageRanges.advanced.unit}`}
          </td>
        </tr>
      </tbody>
    </table>
  );
};
