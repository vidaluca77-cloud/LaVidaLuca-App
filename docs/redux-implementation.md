# Redux State Management Documentation

## Overview

The LaVidaLuca app now implements a comprehensive Redux state management system using Redux Toolkit. This provides centralized state management with predictable updates, improved debugging capabilities, and better performance through optimized re-renders.

## Architecture

### Store Structure

```
src/store/
├── index.ts              # Main store configuration
├── types.ts              # TypeScript type definitions
├── hooks.ts              # Typed hooks and action exports
├── ReduxProvider.tsx     # Provider component
├── slices/               # Feature-based state slices
│   ├── appSlice.ts       # General app state
│   ├── uiSlice.ts        # UI state (modals, notifications)
│   ├── contactSlice.ts   # Contact form state
│   └── joinSlice.ts      # Join form state
├── thunks/               # Async action creators
│   ├── contactThunks.ts  # Contact form API calls
│   └── joinThunks.ts     # Join form API calls
└── selectors/            # Data access selectors
    ├── index.ts          # Re-exports all selectors
    ├── appSelectors.ts   # App state selectors
    ├── uiSelectors.ts    # UI state selectors
    ├── contactSelectors.ts # Contact state selectors
    └── joinSelectors.ts  # Join state selectors
```

## Features Implemented

### 1. Redux Store Configuration
- **File**: `src/store/index.ts`
- Configured with Redux Toolkit's `configureStore`
- Includes all feature slices
- DevTools enabled in development
- Middleware for async thunks and serialization checks

### 2. Feature Slices

#### App Slice (`appSlice.ts`)
Manages general application state:
- Loading states
- Error messages
- Theme (light/dark)
- Language (fr/en)

**Actions:**
- `setLoading(boolean)`
- `setError(string | null)`
- `clearError()`
- `setTheme('light' | 'dark')`
- `setLanguage('fr' | 'en')`
- `resetApp()`

#### UI Slice (`uiSlice.ts`)
Manages user interface state:
- Sidebar state
- Modal state
- Notification system

**Actions:**
- `toggleSidebar()`
- `setSidebarOpen(boolean)`
- `openModal()` / `closeModal()`
- `addNotification(notification)`
- `removeNotification(id)`
- `clearNotifications()`

#### Contact Slice (`contactSlice.ts`)
Manages contact form state:
- Form data (name, email, message)
- Loading and error states
- Submission status

**Actions:**
- `updateContactFormData(data)`
- `resetContactForm()`
- `clearContactError()`

#### Join Slice (`joinSlice.ts`)
Manages join form state:
- Form data (name, email, phone, motivation)
- Loading and error states
- Submission status

**Actions:**
- `updateJoinFormData(data)`
- `resetJoinForm()`
- `clearJoinError()`

### 3. Async Thunks

#### Contact Thunks (`contactThunks.ts`)
- `submitContactForm(formData)` - Handles contact form submission to API

#### Join Thunks (`joinThunks.ts`)
- `submitJoinForm(formData)` - Handles join form submission to API

### 4. Selectors

Optimized data access functions for each feature:

**App Selectors:**
- `selectAppState(state)`
- `selectIsLoading(state)`
- `selectError(state)`
- `selectTheme(state)`
- `selectLanguage(state)`

**UI Selectors:**
- `selectUIState(state)`
- `selectSidebarOpen(state)`
- `selectModalOpen(state)`
- `selectNotifications(state)`
- `selectHasNotifications(state)`

**Contact Selectors:**
- `selectContactState(state)`
- `selectContactFormData(state)`
- `selectContactIsLoading(state)`
- `selectContactError(state)`
- `selectContactSubmitted(state)`

**Join Selectors:**
- `selectJoinState(state)`
- `selectJoinFormData(state)`
- `selectJoinIsLoading(state)`
- `selectJoinError(state)`
- `selectJoinSubmitted(state)`

### 5. Type Safety

Complete TypeScript integration with:
- `RootState` interface for the entire store state
- `AppDispatch` type for dispatch function
- `AsyncThunkConfig` for thunk configurations
- Typed hooks: `useAppDispatch()` and `useAppSelector()`

## Usage Examples

### Basic Setup in Component

```tsx
'use client';
import { useAppSelector, useAppDispatch, addNotification } from '../store/hooks';
import { selectNotifications } from '../store/selectors';

export default function MyComponent() {
  const dispatch = useAppDispatch();
  const notifications = useAppSelector(selectNotifications);

  const handleClick = () => {
    dispatch(addNotification({
      type: 'success',
      message: 'Action completed successfully!'
    }));
  };

  return (
    <div>
      <button onClick={handleClick}>Show Notification</button>
      <p>Notifications: {notifications.length}</p>
    </div>
  );
}
```

### Form Management with Redux

```tsx
'use client';
import { useAppSelector, useAppDispatch, updateContactFormData, submitContactForm } from '../store/hooks';
import { selectContactFormData, selectContactIsLoading } from '../store/selectors';

export default function ContactForm() {
  const dispatch = useAppDispatch();
  const formData = useAppSelector(selectContactFormData);
  const isLoading = useAppSelector(selectContactIsLoading);

  const handleInputChange = (field: string, value: string) => {
    dispatch(updateContactFormData({ [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dispatch(submitContactForm(formData)).unwrap();
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.name}
        onChange={(e) => handleInputChange('name', e.target.value)}
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
```

### Async Operations

```tsx
'use client';
import { useAppDispatch, submitContactForm, addNotification } from '../store/hooks';

export default function AsyncExample() {
  const dispatch = useAppDispatch();

  const handleAsyncOperation = async () => {
    try {
      const result = await dispatch(submitContactForm({
        name: 'John',
        email: 'john@example.com',
        message: 'Hello!'
      })).unwrap();
      
      dispatch(addNotification({
        type: 'success',
        message: 'Form submitted successfully!'
      }));
    } catch (error) {
      dispatch(addNotification({
        type: 'error',
        message: 'Failed to submit form'
      }));
    }
  };

  return <button onClick={handleAsyncOperation}>Submit</button>;
}
```

## Integration Points

### Layout Integration
The Redux Provider is integrated in `src/app/layout.tsx`:

```tsx
import ReduxProvider from '../store/ReduxProvider';
import NotificationToast from '../components/NotificationToast';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ReduxProvider>
          {/* App content */}
          {children}
          
          {/* Redux-managed notification system */}
          <NotificationToast />
        </ReduxProvider>
      </body>
    </html>
  );
}
```

### Component Examples
- **Contact Page** (`src/app/contact/page.tsx`) - Demonstrates form state management
- **NotificationToast** (`src/components/NotificationToast.tsx`) - Shows UI state management

## Benefits Achieved

1. **Centralized State**: All application state is managed in a single, predictable location
2. **Type Safety**: Full TypeScript integration prevents runtime errors
3. **Developer Experience**: Redux DevTools support for debugging and time-travel debugging
4. **Performance**: Optimized re-renders through selective subscriptions
5. **Maintainability**: Clear separation of concerns with feature-based slices
6. **Testability**: Easy to test individual reducers and actions
7. **Scalability**: Structure supports adding new features without breaking existing code

## Testing

Redux functionality is covered by comprehensive tests in `tests/store/redux.test.ts` including:
- Individual slice reducers
- Action creators
- Store integration
- Async thunk behavior

Run tests with:
```bash
npm test tests/store/redux.test.ts
```

## Future Enhancements

Potential areas for expansion:
1. **Persistence**: Add redux-persist for local storage
2. **API Integration**: Expand thunks for more API endpoints
3. **Real-time Updates**: WebSocket integration for live data
4. **Optimistic Updates**: Implement optimistic UI patterns
5. **Caching**: Add RTK Query for advanced data fetching and caching
6. **Middleware**: Custom middleware for analytics or logging

## Performance Considerations

- Selectors are optimized to prevent unnecessary re-renders
- State is normalized where appropriate
- Async operations are handled efficiently with Redux Toolkit's built-in thunk middleware
- DevTools are disabled in production for optimal performance