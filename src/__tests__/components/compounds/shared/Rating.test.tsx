import { render, screen } from '@testing-library/react';
import { Rating } from '@components/compounds/shared/Rating';

describe('Rating Component', () => {
  const defaultProps = {
    label: 'Test Rating',
    value: 250,
    colorClass: 'bg-blue-500',
  };

  it('renders with required props', () => {
    render(<Rating {...defaultProps} />);
    expect(screen.getByText('Test Rating')).toBeInTheDocument();
    expect(screen.getByText('250')).toBeInTheDocument();
  });

  it('calculates percentage width correctly', () => {
    render(<Rating {...defaultProps} />);
    // With default maxValue of 500, value of 250 should be 50%
    const progressBar = screen.getByRole('generic').querySelector(`.${defaultProps.colorClass}`);
    expect(progressBar).toHaveStyle({ width: '50%' });
  });

  it('handles custom maxValue', () => {
    render(<Rating {...defaultProps} maxValue={1000} />);
    // With maxValue of 1000, value of 250 should be 25%
    const progressBar = screen.getByRole('generic').querySelector(`.${defaultProps.colorClass}`);
    expect(progressBar).toHaveStyle({ width: '25%' });
  });

  it('caps percentage at 100%', () => {
    render(<Rating {...defaultProps} value={1000} />);
    const progressBar = screen.getByRole('generic').querySelector(`.${defaultProps.colorClass}`);
    expect(progressBar).toHaveStyle({ width: '100%' });
  });

  it('applies custom className', () => {
    const customClass = 'custom-test-class';
    render(<Rating {...defaultProps} className={customClass} />);
    const container = screen.getByRole('generic');
    expect(container).toHaveClass(customClass);
  });

  it('applies color class to progress bar', () => {
    const customColorClass = 'bg-red-500';
    render(<Rating {...defaultProps} colorClass={customColorClass} />);
    const progressBar = screen.getByRole('generic').querySelector(`.${customColorClass}`);
    expect(progressBar).toBeInTheDocument();
  });
});
