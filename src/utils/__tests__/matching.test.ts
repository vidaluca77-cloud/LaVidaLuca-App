// src/utils/__tests__/matching.test.ts
import { calculateMatching } from "../matching";
import { UserProfile } from "@/types";

describe("calculateMatching", () => {
  it("calculates matching scores correctly", () => {
    const profile: UserProfile = {
      skills: ["elevage", "hygiene"],
      availability: ["weekend"],
      location: "Test Location",
      preferences: ["agri"],
    };

    const suggestions = calculateMatching(profile);

    expect(suggestions).toHaveLength(3);
    expect(suggestions[0].score).toBeGreaterThan(0);
    expect(suggestions[0].reasons).toBeInstanceOf(Array);
    expect(suggestions[0].activity).toBeDefined();
  });

  it("returns suggestions sorted by score descending", () => {
    const profile: UserProfile = {
      skills: ["elevage"],
      availability: ["weekend"],
      location: "Test Location",
      preferences: ["agri"],
    };

    const suggestions = calculateMatching(profile);

    for (let i = 0; i < suggestions.length - 1; i++) {
      expect(suggestions[i].score).toBeGreaterThanOrEqual(
        suggestions[i + 1].score
      );
    }
  });
});
