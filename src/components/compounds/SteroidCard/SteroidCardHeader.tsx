import type { FC } from 'react';
import styles from './styles.module.css';

interface SteroidCardHeaderProps {
  name: string;
  category: string;
}

export const SteroidCardHeader: FC<SteroidCardHeaderProps> = ({ name, category }) => {
  return (
    <div className={styles.header}>
      <h3 className={styles.title}>{name}</h3>
      <div className={styles.category}>{category}</div>
    </div>
  );
};
