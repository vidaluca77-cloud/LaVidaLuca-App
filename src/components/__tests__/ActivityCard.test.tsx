import { render, screen, fireEvent } from '@testing-library/react';
import ActivityCard from '../ActivityCard';
import { Activity } from '@/types';

// Mock activity data
const mockActivity: Activity = {
  id: '1',
  slug: 'test-activity',
  title: 'Test Activity',
  category: 'agri',
  summary: 'This is a test activity summary',
  duration_min: 90,
  skill_tags: ['test', 'agriculture', 'example'],
  seasonality: ['spring'],
  safety_level: 1,
  materials: ['gloves', 'boots']
};

describe('ActivityCard Component', () => {
  it('renders activity information correctly', () => {
    render(<ActivityCard activity={mockActivity} />);
    
    expect(screen.getByText('Test Activity')).toBeInTheDocument();
    expect(screen.getByText('This is a test activity summary')).toBeInTheDocument();
    expect(screen.getByText('1h30')).toBeInTheDocument(); // duration
    expect(screen.getByText('Facile')).toBeInTheDocument(); // safety level
  });

  it('displays skill tags with limit', () => {
    render(<ActivityCard activity={mockActivity} />);
    
    expect(screen.getByText('test')).toBeInTheDocument();
    expect(screen.getByText('agriculture')).toBeInTheDocument();
    expect(screen.getByText('example')).toBeInTheDocument();
  });

  it('displays materials', () => {
    render(<ActivityCard activity={mockActivity} />);
    
    expect(screen.getByText('Matériel :')).toBeInTheDocument();
    expect(screen.getByText('gloves, boots')).toBeInTheDocument();
  });

  it('shows skill tag overflow indicator when more than 3 tags', () => {
    const activityWithManyTags: Activity = {
      ...mockActivity,
      skill_tags: ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    };
    
    render(<ActivityCard activity={activityWithManyTags} />);
    
    expect(screen.getByText('+2')).toBeInTheDocument();
  });

  it('calls onLearnMore when button is clicked', () => {
    const mockOnLearnMore = jest.fn();
    render(<ActivityCard activity={mockActivity} onLearnMore={mockOnLearnMore} />);
    
    const button = screen.getByText('En savoir plus');
    fireEvent.click(button);
    
    expect(mockOnLearnMore).toHaveBeenCalledWith(mockActivity);
  });

  it('does not show materials section when empty', () => {
    const activityWithoutMaterials: Activity = {
      ...mockActivity,
      materials: []
    };
    
    render(<ActivityCard activity={activityWithoutMaterials} />);
    
    expect(screen.queryByText('Matériel :')).not.toBeInTheDocument();
  });
});