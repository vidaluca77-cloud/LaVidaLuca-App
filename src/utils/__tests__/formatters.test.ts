// src/utils/__tests__/formatters.test.ts
import { formatDuration, getSafetyColor, getSafetyText } from "../formatters";

describe("formatters", () => {
  describe("formatDuration", () => {
    it("formats minutes correctly", () => {
      expect(formatDuration(30)).toBe("30min");
      expect(formatDuration(60)).toBe("1h");
      expect(formatDuration(90)).toBe("1h30");
      expect(formatDuration(120)).toBe("2h");
    });
  });

  describe("getSafetyColor", () => {
    it("returns correct color classes", () => {
      expect(getSafetyColor(1)).toBe("bg-green-100 text-green-800");
      expect(getSafetyColor(2)).toBe("bg-yellow-100 text-yellow-800");
      expect(getSafetyColor(3)).toBe("bg-red-100 text-red-800");
      expect(getSafetyColor(0)).toBe("bg-gray-100 text-gray-800");
    });
  });

  describe("getSafetyText", () => {
    it("returns correct safety text", () => {
      expect(getSafetyText(1)).toBe("Facile");
      expect(getSafetyText(2)).toBe("Attention");
      expect(getSafetyText(3)).toBe("Expert");
      expect(getSafetyText(0)).toBe("Non défini");
    });
  });
});
