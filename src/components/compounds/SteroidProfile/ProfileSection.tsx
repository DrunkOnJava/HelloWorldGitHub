import type { FC, ReactNode } from 'react';
import styles from './styles.module.css';

interface ProfileSectionProps {
  title: string;
  children: ReactNode;
  className?: string;
}

export const ProfileSection: FC<ProfileSectionProps> = ({
  title,
  children,
  className = '',
}) => {
  return (
    <section className={`${styles.section} ${className}`}>
      <h2 className={styles.sectionTitle}>{title}</h2>
      {children}
    </section>
  );
};
