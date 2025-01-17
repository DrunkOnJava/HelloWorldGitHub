import type { FC } from 'react';
import type { Compound } from '../../../data/compounds/types';
import { ProfileSection } from './ProfileSection';
import { Rating, DosageTable, SideEffectsList } from '../shared';
import styles from './styles.module.css';

interface SteroidProfileProps {
  compound: Compound;
}

export const SteroidProfile: FC<SteroidProfileProps> = ({ compound }) => {
  return (
    <div className={styles.profile}>
      <header className={styles.header}>
        <h1 className={styles.title}>{compound.name}</h1>
        <div className={styles.category}>{compound.category}</div>
        <p className={styles.description}>{compound.description}</p>
      </header>

      <ProfileSection title="Ratings">
        <div className={styles.ratings}>
          <Rating
            label="Anabolic Rating"
            value={compound.anabolicRating}
            colorClass="bg-green-500"
            className="mb-4"
          />
          <Rating
            label="Androgenic Rating"
            value={compound.androgenicRating}
            colorClass="bg-red-500"
          />
        </div>
      </ProfileSection>

      <ProfileSection title="Dosage Information">
        <div className={styles.grid}>
          <DosageTable dosageRanges={compound.dosageRanges} />
          <div>
            <p><strong>Half Life:</strong> {compound.halfLife}</p>
            <p><strong>Detection Time:</strong> {compound.detectionTime}</p>
          </div>
        </div>
      </ProfileSection>

      <ProfileSection title="Side Effects">
        <SideEffectsList sideEffects={compound.sideEffects} />
      </ProfileSection>

      <ProfileSection title="PCT Requirements">
        <div className={styles.pctSection}>
          <div className={styles.pctRequired}>
            {compound.pctRequirements.required ? "PCT Required" : "PCT Optional"}
          </div>
          <div className={styles.pctDetails}>
            <p><strong>Protocol:</strong> {compound.pctRequirements.protocol}</p>
            <p><strong>Duration:</strong> {compound.pctRequirements.duration}</p>
          </div>
        </div>
      </ProfileSection>

      <ProfileSection title="Interactions">
        <ul className={styles.interactions}>
          {compound.interactions.map((interaction, index) => (
            <li key={index} className={styles.interactionItem}>{interaction}</li>
          ))}
        </ul>
      </ProfileSection>

      <ProfileSection title="References">
        <div className={styles.references}>
          {compound.references.map((reference, index) => (
            <p key={index}>{reference}</p>
          ))}
        </div>
      </ProfileSection>
    </div>
  );
};
