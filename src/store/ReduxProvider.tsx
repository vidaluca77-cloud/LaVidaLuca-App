// src/store/ReduxProvider.tsx
'use client';

import { Provider } from 'react-redux';
import { store } from './index';

interface ReduxProviderProps {
  children: React.ReactNode;
}

export default function ReduxProvider({ children }: ReduxProviderProps) {
  return <Provider store={store}>{children}</Provider>;
}