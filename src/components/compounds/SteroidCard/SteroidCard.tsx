import type { FC } from 'react';
import type { Compound } from '../../../data/compounds/types';
import { SteroidCardHeader } from './SteroidCardHeader';
import { SteroidCardBody } from './SteroidCardBody';
import styles from './styles.module.css';

interface SteroidCardProps {
  compound: Compound;
  onClick?: () => void;
}

export const SteroidCard: FC<SteroidCardProps> = ({ compound, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  return (
    <div
      className={styles.card}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          handleClick();
        }
      }}
    >
      <SteroidCardHeader
        name={compound.name}
        category={compound.category}
      />
      <SteroidCardBody
        description={compound.description}
        anabolicRating={compound.anabolicRating}
        androgenicRating={compound.androgenicRating}
        halfLife={compound.halfLife}
        detectionTime={compound.detectionTime}
      />
    </div>
  );
};
