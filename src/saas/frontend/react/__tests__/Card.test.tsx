/**
 * Card Component Tests
 * 
 * Unit tests for the Card UI component.
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from '../components/ui/Card';

// ============================================================================
// TESTS
// ============================================================================

describe('Card Component', () => {
  it('renders with children', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('renders with different variants', () => {
    const { rerender } = render(<Card variant="default">Default</Card>);
    expect(screen.getByText('Default')).toHaveClass('card');

    rerender(<Card variant="elevated">Elevated</Card>);
    expect(screen.getByText('Elevated')).toHaveClass('card--elevated');

    rerender(<Card variant="outlined">Outlined</Card>);
    expect(screen.getByText('Outlined')).toHaveClass('card--outlined');
  });

  it('renders with different padding sizes', () => {
    const { rerender } = render(<Card padding="none">No padding</Card>);
    expect(screen.getByText('No padding')).toHaveClass('card--padding-none');

    rerender(<Card padding="small">Small padding</Card>);
    expect(screen.getByText('Small padding')).toHaveClass('card--padding-small');

    rerender(<Card padding="medium">Medium padding</Card>);
    expect(screen.getByText('Medium padding')).toHaveClass('card--padding-medium');

    rerender(<Card padding="large">Large padding</Card>);
    expect(screen.getByText('Large padding')).toHaveClass('card--padding-large');
  });

  it('applies custom className', () => {
    render(<Card className="custom-card">Custom</Card>);
    expect(screen.getByText('Custom')).toHaveClass('custom-card');
  });

  it('renders with multiple children', () => {
    render(
      <Card>
        <div>First child</div>
        <div>Second child</div>
      </Card>
    );
    expect(screen.getByText('First child')).toBeInTheDocument();
    expect(screen.getByText('Second child')).toBeInTheDocument();
  });
});

describe('CardHeader Component', () => {
  it('renders with children', () => {
    render(<CardHeader>Header content</CardHeader>);
    expect(screen.getByText('Header content')).toBeInTheDocument();
    expect(screen.getByText('Header content')).toHaveClass('card__header');
  });

  it('applies custom className', () => {
    render(<CardHeader className="custom-header">Header</CardHeader>);
    expect(screen.getByText('Header')).toHaveClass('custom-header');
  });
});

describe('CardContent Component', () => {
  it('renders with children', () => {
    render(<CardContent>Content</CardContent>);
    expect(screen.getByText('Content')).toBeInTheDocument();
    expect(screen.getByText('Content')).toHaveClass('card__content');
  });

  it('applies custom className', () => {
    render(<CardContent className="custom-content">Content</CardContent>);
    expect(screen.getByText('Content')).toHaveClass('custom-content');
  });
});

describe('CardFooter Component', () => {
  it('renders with children', () => {
    render(<CardFooter>Footer content</CardFooter>);
    expect(screen.getByText('Footer content')).toBeInTheDocument();
    expect(screen.getByText('Footer content')).toHaveClass('card__footer');
  });

  it('applies custom className', () => {
    render(<CardFooter className="custom-footer">Footer</CardFooter>);
    expect(screen.getByText('Footer')).toHaveClass('custom-footer');
  });
});

describe('CardTitle Component', () => {
  it('renders with children', () => {
    render(<CardTitle>Title</CardTitle>);
    expect(screen.getByText('Title')).toBeInTheDocument();
    expect(screen.getByText('Title')).toHaveClass('card__title');
  });

  it('renders with different heading levels', () => {
    const { rerender } = render(<CardTitle level={1}>H1 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    expect(screen.getByText('H1 Title')).toHaveClass('card__title--h1');

    rerender(<CardTitle level={2}>H2 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 2 })).toBeInTheDocument();
    expect(screen.getByText('H2 Title')).toHaveClass('card__title--h2');

    rerender(<CardTitle level={3}>H3 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 3 })).toBeInTheDocument();
    expect(screen.getByText('H3 Title')).toHaveClass('card__title--h3');

    rerender(<CardTitle level={4}>H4 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 4 })).toBeInTheDocument();
    expect(screen.getByText('H4 Title')).toHaveClass('card__title--h4');

    rerender(<CardTitle level={5}>H5 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 5 })).toBeInTheDocument();
    expect(screen.getByText('H5 Title')).toHaveClass('card__title--h5');

    rerender(<CardTitle level={6}>H6 Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 6 })).toBeInTheDocument();
    expect(screen.getByText('H6 Title')).toHaveClass('card__title--h6');
  });

  it('defaults to h3 when no level is specified', () => {
    render(<CardTitle>Default Title</CardTitle>);
    expect(screen.getByRole('heading', { level: 3 })).toBeInTheDocument();
    expect(screen.getByText('Default Title')).toHaveClass('card__title--h3');
  });

  it('applies custom className', () => {
    render(<CardTitle className="custom-title">Title</CardTitle>);
    expect(screen.getByText('Title')).toHaveClass('custom-title');
  });
});

describe('Card Composition', () => {
  it('renders complete card with all sections', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Card content goes here</p>
        </CardContent>
        <CardFooter>
          <button>Action</button>
        </CardFooter>
      </Card>
    );

    expect(screen.getByText('Card Title')).toBeInTheDocument();
    expect(screen.getByText('Card content goes here')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
  });

  it('renders card with only header and content', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Simple Card</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Simple content</p>
        </CardContent>
      </Card>
    );

    expect(screen.getByText('Simple Card')).toBeInTheDocument();
    expect(screen.getByText('Simple content')).toBeInTheDocument();
  });
});
