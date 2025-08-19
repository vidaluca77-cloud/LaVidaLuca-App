// src/lib/supabase.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  if (!url || !key) {
    // Return a mock client for development/build time
    return {
      auth: {
        signInWithPassword: async () => ({ error: new Error('Supabase not configured') }),
        signOut: async () => ({ error: null }),
        getUser: async () => ({ data: { user: null }, error: null }),
      }
    } as any;
  }
  
  return createBrowserClient(url, key);
}

export const supabase = createClient();