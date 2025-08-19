import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

export const supabase = supabaseUrl && supabaseAnonKey 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

// Auth helper functions
export const signUp = async (email: string, password: string, metadata: any = {}) => {
  if (!supabase) throw new Error('Supabase not configured')
  return await supabase.auth.signUp({
    email,
    password,
    options: {
      data: metadata
    }
  })
}

export const signIn = async (email: string, password: string) => {
  if (!supabase) throw new Error('Supabase not configured')
  return await supabase.auth.signInWithPassword({
    email,
    password
  })
}

export const signOut = async () => {
  if (!supabase) throw new Error('Supabase not configured')
  return await supabase.auth.signOut()
}

export const getCurrentUser = async () => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

export const getUserProfile = async (userId: string) => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single()
  
  return { data, error }
}

export const updateUserProfile = async (userId: string, updates: any) => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data, error } = await supabase
    .from('users')
    .update(updates)
    .eq('id', userId)
    .select()
  
  return { data, error }
}

// Activities helper functions
export const getActivities = async () => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data, error } = await supabase
    .from('activities')
    .select('*')
    .order('title')
  
  return { data, error }
}

export const getActivity = async (id: string) => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data, error } = await supabase
    .from('activities')
    .select('*')
    .eq('id', id)
    .single()
  
  return { data, error }
}

// Contact helper function
export const submitContactMessage = async (message: any) => {
  if (!supabase) throw new Error('Supabase not configured')
  const { data, error } = await supabase
    .from('contact_messages')
    .insert([message])
    .select()
  
  return { data, error }
}