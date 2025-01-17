import type { FC } from 'react';
import type { Compound } from '../../data/compounds/types';
import { SteroidProfile } from '../../components/compounds/SteroidProfile';
import { Header, Footer } from '../shared';

interface CompoundTemplateProps {
  compound: Compound;
}

export const CompoundTemplate: FC<CompoundTemplateProps> = ({ compound }) => {
  const breadcrumbs = [
    { label: 'Home', href: '/' },
    { label: 'Compounds', href: '/compounds' },
    { label: compound.name },
  ];

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <Header
          breadcrumbs={breadcrumbs}
          title={compound.name}
          subtitle={compound.category}
        />

        <SteroidProfile compound={compound} />

        <Footer showDisclaimer={true} />
      </div>
    </main>
  );
};
