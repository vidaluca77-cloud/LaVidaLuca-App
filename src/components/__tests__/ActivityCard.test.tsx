/**
 * Tests for ActivityCard component
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import ActivityCard from '../ActivityCard';
import { Activity } from '@/types';

const mockActivity: Activity = {
  id: '1',
  slug: 'test-activity',
  title: 'Test Activity',
  category: 'agri',
  summary: 'This is a test activity for unit testing',
  duration_min: 90,
  skill_tags: ['test', 'jest', 'react'],
  seasonality: ['printemps'],
  safety_level: 1,
  materials: ['laptop', 'test files'],
};

describe('ActivityCard Component', () => {
  it('renders activity information correctly', () => {
    render(<ActivityCard activity={mockActivity} />);

    expect(screen.getByText('Test Activity')).toBeInTheDocument();
    expect(
      screen.getByText('This is a test activity for unit testing')
    ).toBeInTheDocument();
    expect(screen.getByText('1h30')).toBeInTheDocument();
    expect(screen.getByText('Facile')).toBeInTheDocument();
  });

  it('renders skill tags', () => {
    render(<ActivityCard activity={mockActivity} />);

    expect(screen.getByText('test')).toBeInTheDocument();
    expect(screen.getByText('jest')).toBeInTheDocument();
    expect(screen.getByText('react')).toBeInTheDocument();
  });

  it('renders materials list', () => {
    render(<ActivityCard activity={mockActivity} />);

    expect(screen.getByText('Matériel :')).toBeInTheDocument();
    expect(screen.getByText('laptop, test files')).toBeInTheDocument();
  });

  it('formats duration correctly for hours and minutes', () => {
    const activityWithComplexDuration: Activity = {
      ...mockActivity,
      duration_min: 125, // 2h05
    };

    render(<ActivityCard activity={activityWithComplexDuration} />);
    expect(screen.getByText('2h05')).toBeInTheDocument();
  });

  it('formats duration correctly for minutes only', () => {
    const activityWithMinutes: Activity = {
      ...mockActivity,
      duration_min: 45,
    };

    render(<ActivityCard activity={activityWithMinutes} />);
    expect(screen.getByText('45min')).toBeInTheDocument();
  });

  it('shows safety levels correctly', () => {
    const activities = [
      { ...mockActivity, safety_level: 1 },
      { ...mockActivity, safety_level: 2 },
      { ...mockActivity, safety_level: 3 },
    ];

    activities.forEach((activity, index) => {
      const { unmount } = render(<ActivityCard activity={activity} />);

      if (index === 0) expect(screen.getByText('Facile')).toBeInTheDocument();
      if (index === 1)
        expect(screen.getByText('Attention')).toBeInTheDocument();
      if (index === 2) expect(screen.getByText('Expert')).toBeInTheDocument();

      unmount();
    });
  });

  it('handles activities with many skill tags', () => {
    const activityWithManyTags: Activity = {
      ...mockActivity,
      skill_tags: ['tag1', 'tag2', 'tag3', 'tag4', 'tag5'],
    };

    render(<ActivityCard activity={activityWithManyTags} />);

    expect(screen.getByText('tag1')).toBeInTheDocument();
    expect(screen.getByText('tag2')).toBeInTheDocument();
    expect(screen.getByText('tag3')).toBeInTheDocument();
    expect(screen.getByText('+2')).toBeInTheDocument(); // Shows +2 for remaining tags
  });
});
