import type { Compound } from './types';
import { testosterone } from './compounds/testosterone';
import { nandrolone } from './compounds/nandrolone';
import { trenbolone } from './compounds/trenbolone';

export type { Compound };

export const compounds: Compound[] = [
  testosterone,
  nandrolone,
  trenbolone
];

// Export individual compounds for direct access
export {
  testosterone,
  nandrolone,
  trenbolone
};
