'use client'

import React, { useState } from 'react'
import { useLoginMutation } from '../lib/api/authApi'
import { useDispatch } from 'react-redux'
import { setCredentials } from '../lib/features/authSlice'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [login, { isLoading, error }] = useLoginMutation()
  const dispatch = useDispatch()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const result = await login({ username: email, password }).unwrap()
      dispatch(setCredentials({
        user: result.user,
        token: result.access_token
      }))
    } catch (err) {
      console.error('Login failed:', err)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Se connecter</h2>
      
      <div className="mb-4">
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
          Email
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div className="mb-6">
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
          Mot de passe
        </label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      {error && (
        <div className="mb-4 text-red-600 text-sm">
          Erreur de connexion. Vérifiez vos identifiants.
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {isLoading ? 'Connexion...' : 'Se connecter'}
      </button>
    </form>
  )
}