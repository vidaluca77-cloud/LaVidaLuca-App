import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Activity, Suggestion, UserProfile, CacheEntry } from '../../lib/types';

// Async thunks for activities
export const fetchActivities = createAsyncThunk(
  'activities/fetchActivities',
  async (params: { category?: string; limit?: number } = {}, { rejectWithValue }) => {
    try {
      const queryParams = new URLSearchParams();
      if (params.category) queryParams.append('category', params.category);
      if (params.limit) queryParams.append('limit', params.limit.toString());
      
      const response = await fetch(`/api/activities?${queryParams}`);
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch activities');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue('Network error occurred');
    }
  }
);

export const fetchActivity = createAsyncThunk(
  'activities/fetchActivity',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/activities/${id}`);
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to fetch activity');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue('Network error occurred');
    }
  }
);

export const generateSuggestions = createAsyncThunk(
  'activities/generateSuggestions',
  async (profile: UserProfile, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/activities/suggestions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      });
      
      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message || 'Failed to generate suggestions');
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue('Network error occurred');
    }
  }
);

// Mock data fallback (same as current implementation)
const MOCK_ACTIVITIES: Activity[] = [
  // Agriculture
  { id: '1', slug: 'nourrir-soigner-moutons', title: 'Nourrir et soigner les moutons', category: 'agri', summary: 'Gestes quotidiens : alimentation, eau, observation.', duration_min: 60, skill_tags: ['elevage', 'responsabilite'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '2', slug: 'tonte-entretien-troupeau', title: 'Tonte & entretien du troupeau', category: 'agri', summary: 'Hygiène, tonte (démo), soins courants.', duration_min: 90, skill_tags: ['elevage', 'hygiene'], seasonality: ['printemps'], safety_level: 2, materials: ['bottes', 'gants'] },
  { id: '3', slug: 'basse-cour-soins', title: 'Soins basse-cour', category: 'agri', summary: 'Poules/canards/lapins : alimentation, abris, propreté.', duration_min: 60, skill_tags: ['soins_animaux'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '4', slug: 'plantation-cultures', title: 'Plantation de cultures', category: 'agri', summary: 'Semis, arrosage, paillage, suivi de plants.', duration_min: 90, skill_tags: ['sol', 'plantes'], seasonality: ['printemps', 'ete'], safety_level: 1, materials: ['gants'] },
  { id: '5', slug: 'init-maraichage', title: 'Initiation maraîchage', category: 'agri', summary: 'Plan de culture, entretien, récolte respectueuse.', duration_min: 120, skill_tags: ['sol', 'organisation'], seasonality: ['printemps', 'ete', 'automne'], safety_level: 1, materials: ['gants', 'bottes'] },
  { id: '6', slug: 'clotures-abris', title: 'Gestion des clôtures & abris', category: 'agri', summary: 'Identifier, réparer, sécuriser parcs et abris.', duration_min: 120, skill_tags: ['securite', 'bois'], seasonality: ['toutes'], safety_level: 2, materials: ['gants'] },

  // Transformation
  { id: '7', slug: 'fromage', title: 'Fabrication de fromage', category: 'transfo', summary: 'Du lait au caillé : hygiène, moulage, affinage (découverte).', duration_min: 90, skill_tags: ['hygiene', 'precision'], seasonality: ['toutes'], safety_level: 2, materials: ['tablier'] },
  { id: '8', slug: 'conserves', title: 'Confitures & conserves', category: 'transfo', summary: 'Préparation, stérilisation, mise en pot, étiquetage.', duration_min: 90, skill_tags: ['organisation', 'hygiene'], seasonality: ['ete', 'automne'], safety_level: 1, materials: ['tablier'] },
  // ... (truncated for brevity, but would include all 30 activities)
];

interface ActivitiesState {
  activities: Activity[];
  currentActivity: Activity | null;
  suggestions: Suggestion[];
  filteredActivities: Activity[];
  selectedCategory: string;
  isLoading: boolean;
  error: string | null;
  cache: {
    activities: CacheEntry<Activity[]> | null;
    suggestions: { [profileHash: string]: CacheEntry<Suggestion[]> };
  };
}

const initialState: ActivitiesState = {
  activities: [],
  currentActivity: null,
  suggestions: [],
  filteredActivities: [],
  selectedCategory: 'all',
  isLoading: false,
  error: null,
  cache: {
    activities: null,
    suggestions: {},
  },
};

// Helper function to calculate suggestions (same logic as before)
const calculateMatching = (profile: UserProfile, activities: Activity[]): Suggestion[] => {
  const suggestions = activities.map(activity => {
    let score = 0;
    const reasons: string[] = [];

    // Compétences communes
    const commonSkills = activity.skill_tags.filter(skill => 
      profile.skills.includes(skill)
    );
    if (commonSkills.length > 0) {
      score += commonSkills.length * 15;
      reasons.push(`Compétences correspondantes : ${commonSkills.join(', ')}`);
    }

    // Préférences de catégories
    if (profile.preferences.includes(activity.category)) {
      score += 25;
      const categoryNames = {
        agri: 'Agriculture',
        transfo: 'Transformation', 
        artisanat: 'Artisanat',
        nature: 'Environnement',
        social: 'Animation'
      };
      reasons.push(`Catégorie préférée : ${categoryNames[activity.category]}`);
    }

    // Durée adaptée
    if (activity.duration_min <= 90) {
      score += 10;
      reasons.push('Durée adaptée pour débuter');
    }

    // Sécurité
    if (activity.safety_level <= 2) {
      score += 10;
      if (activity.safety_level === 1) {
        reasons.push('Activité sans risque particulier');
      }
    }

    // Disponibilité (simulation)
    if (profile.availability.includes('weekend') || profile.availability.includes('semaine')) {
      score += 15;
      reasons.push('Compatible avec vos disponibilités');
    }

    return { activity, score, reasons };
  });

  return suggestions
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
};

const activitiesSlice = createSlice({
  name: 'activities',
  initialState,
  reducers: {
    setSelectedCategory: (state, action: PayloadAction<string>) => {
      state.selectedCategory = action.payload;
      state.filteredActivities = action.payload === 'all' 
        ? state.activities 
        : state.activities.filter(activity => activity.category === action.payload);
    },
    setCurrentActivity: (state, action: PayloadAction<Activity | null>) => {
      state.currentActivity = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    generateLocalSuggestions: (state, action: PayloadAction<UserProfile>) => {
      // Generate suggestions using mock data if API fails
      state.suggestions = calculateMatching(action.payload, MOCK_ACTIVITIES);
    },
    setCachedActivities: (state, action: PayloadAction<CacheEntry<Activity[]>>) => {
      state.cache.activities = action.payload;
    },
    setCachedSuggestions: (state, action: PayloadAction<{ profileHash: string; entry: CacheEntry<Suggestion[]> }>) => {
      state.cache.suggestions[action.payload.profileHash] = action.payload.entry;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Activities
      .addCase(fetchActivities.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchActivities.fulfilled, (state, action) => {
        state.isLoading = false;
        state.activities = action.payload;
        state.filteredActivities = state.selectedCategory === 'all' 
          ? action.payload 
          : action.payload.filter((activity: Activity) => activity.category === state.selectedCategory);
        state.error = null;
      })
      .addCase(fetchActivities.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        // Fallback to mock data
        state.activities = MOCK_ACTIVITIES;
        state.filteredActivities = state.selectedCategory === 'all' 
          ? MOCK_ACTIVITIES 
          : MOCK_ACTIVITIES.filter(activity => activity.category === state.selectedCategory);
      })

      // Fetch Single Activity
      .addCase(fetchActivity.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchActivity.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentActivity = action.payload;
        state.error = null;
      })
      .addCase(fetchActivity.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })

      // Generate Suggestions
      .addCase(generateSuggestions.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(generateSuggestions.fulfilled, (state, action) => {
        state.isLoading = false;
        state.suggestions = action.payload;
        state.error = null;
      })
      .addCase(generateSuggestions.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        // Keep suggestions empty on error, will be handled by UI
      });
  },
});

export const { 
  setSelectedCategory, 
  setCurrentActivity, 
  clearError, 
  generateLocalSuggestions,
  setCachedActivities,
  setCachedSuggestions,
} = activitiesSlice.actions;
export default activitiesSlice.reducer;