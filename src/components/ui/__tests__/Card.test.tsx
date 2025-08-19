import { render, screen } from '@testing-library/react';

import { Card, Badge } from '@/components/ui/Card';

describe('Card Component', () => {
  it('should render children correctly', () => {
    render(
      <Card>
        <p>Card content</p>
      </Card>
    );
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('should apply base card styles', () => {
    const { container } = render(<Card>Content</Card>);
    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass(
      'bg-white',
      'rounded-xl',
      'shadow-sm',
      'border',
      'border-gray-100',
      'p-6'
    );
  });

  it('should apply hover styles when hover prop is true', () => {
    const { container } = render(<Card hover>Content</Card>);
    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass('hover:shadow-md', 'transition-shadow');
  });

  it('should accept additional className', () => {
    const { container } = render(<Card className='custom-class'>Content</Card>);
    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass('custom-class');
  });
});

describe('Badge Component', () => {
  it('should render with correct text', () => {
    render(<Badge>Test Badge</Badge>);
    expect(screen.getByText('Test Badge')).toBeInTheDocument();
  });

  it('should apply gray variant styles by default', () => {
    render(<Badge>Default Badge</Badge>);
    const badge = screen.getByText('Default Badge');
    expect(badge).toHaveClass('bg-gray-100', 'text-gray-800');
  });

  it('should apply correct variant styles', () => {
    const variants = [
      {
        variant: 'green' as const,
        classes: ['bg-green-100', 'text-green-800'],
      },
      {
        variant: 'yellow' as const,
        classes: ['bg-yellow-100', 'text-yellow-800'],
      },
      { variant: 'red' as const, classes: ['bg-red-100', 'text-red-800'] },
      { variant: 'blue' as const, classes: ['bg-blue-100', 'text-blue-800'] },
    ];

    variants.forEach(({ variant, classes }) => {
      const { container } = render(
        <Badge variant={variant}>{variant} badge</Badge>
      );
      const badge = container.firstChild as HTMLElement;
      classes.forEach(className => {
        expect(badge).toHaveClass(className);
      });
    });
  });

  it('should apply size classes correctly', () => {
    const { rerender } = render(<Badge size='sm'>Small Badge</Badge>);
    expect(screen.getByText('Small Badge')).toHaveClass(
      'px-2',
      'py-1',
      'text-xs'
    );

    rerender(<Badge size='md'>Medium Badge</Badge>);
    expect(screen.getByText('Medium Badge')).toHaveClass(
      'px-3',
      'py-1',
      'text-sm'
    );
  });
});
