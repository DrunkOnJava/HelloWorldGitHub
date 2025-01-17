import type { FC } from 'react';
import { Rating } from '../shared';
import styles from './styles.module.css';

interface SteroidCardBodyProps {
  description: string;
  anabolicRating: number;
  androgenicRating: number;
  halfLife: string;
  detectionTime: string;
}

export const SteroidCardBody: FC<SteroidCardBodyProps> = ({
  description,
  anabolicRating,
  androgenicRating,
  halfLife,
  detectionTime,
}) => {
  return (
    <>
      <div className={styles.body}>
        <p className={styles.description}>{description}</p>
        <div className={styles.stats}>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Half Life</span>
            <span className={styles.statValue}>{halfLife}</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Detection Time</span>
            <span className={styles.statValue}>{detectionTime}</span>
          </div>
        </div>
      </div>

      <div className={styles.ratings}>
        <Rating
          label="Anabolic"
          value={anabolicRating}
          colorClass="bg-green-500"
          className="mb-2"
        />
        <Rating
          label="Androgenic"
          value={androgenicRating}
          colorClass="bg-red-500"
        />
      </div>
    </>
  );
};
