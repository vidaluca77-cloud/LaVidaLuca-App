import { render, screen } from '@testing-library/react';
import { formatDuration, getSafetyColor, getSafetyText } from '../activityHelpers';

describe('Activity Helpers', () => {
  describe('formatDuration', () => {
    it('formats minutes correctly', () => {
      expect(formatDuration(30)).toBe('30min');
      expect(formatDuration(45)).toBe('45min');
    });

    it('formats hours correctly', () => {
      expect(formatDuration(60)).toBe('1h');
      expect(formatDuration(120)).toBe('2h');
    });

    it('formats hours and minutes correctly', () => {
      expect(formatDuration(90)).toBe('1h30');
      expect(formatDuration(150)).toBe('2h30');
    });
  });

  describe('getSafetyColor', () => {
    it('returns correct colors for safety levels', () => {
      expect(getSafetyColor(1)).toBe('bg-green-100 text-green-800');
      expect(getSafetyColor(2)).toBe('bg-yellow-100 text-yellow-800');
      expect(getSafetyColor(3)).toBe('bg-red-100 text-red-800');
      expect(getSafetyColor(999)).toBe('bg-gray-100 text-gray-800');
    });
  });

  describe('getSafetyText', () => {
    it('returns correct text for safety levels', () => {
      expect(getSafetyText(1)).toBe('Facile');
      expect(getSafetyText(2)).toBe('Attention');
      expect(getSafetyText(3)).toBe('Expert');
      expect(getSafetyText(999)).toBe('Non défini');
    });
  });
});