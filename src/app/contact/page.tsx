"use client";
import { useState } from "react";
import { useAppSelector, useAppDispatch, updateContactFormData, resetContactForm, submitContactForm, addNotification } from "../../store/hooks";
import { selectContactFormData, selectContactIsLoading, selectContactError, selectContactSubmitted } from "../../store/selectors";

export default function Contact() {
  const dispatch = useAppDispatch();
  const formData = useAppSelector(selectContactFormData);
  const isLoading = useAppSelector(selectContactIsLoading);
  const error = useAppSelector(selectContactError);
  const submitted = useAppSelector(selectContactSubmitted);

  const handleInputChange = (field: string, value: string) => {
    dispatch(updateContactFormData({ [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    try {
      await dispatch(submitContactForm(formData)).unwrap();
      
      // Show success notification
      dispatch(addNotification({
        type: 'success',
        message: 'Votre message a été envoyé avec succès !'
      }));
      
    } catch (error) {
      // Show error notification
      dispatch(addNotification({
        type: 'error',
        message: error as string || 'Une erreur est survenue'
      }));
    }
  };

  const handleReset = () => {
    dispatch(resetContactForm());
  };

  return (
    <div className="max-w-xl">
      <h1 className="text-3xl font-bold mb-4">Contact</h1>
      
      {submitted ? (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-green-800">
            Merci ! Votre message a été envoyé. On vous répond vite.
          </p>
          <button 
            onClick={handleReset}
            className="mt-3 text-green-600 hover:text-green-800 underline"
          >
            Envoyer un autre message
          </button>
        </div>
      ) : (
        <>
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-800">{error}</p>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-3">
            <input 
              name="name" 
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              placeholder="Nom" 
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500" 
              required 
              disabled={isLoading}
            />
            <input 
              name="email" 
              type="email" 
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              placeholder="Email" 
              className="w-full border px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500" 
              required 
              disabled={isLoading}
            />
            <textarea 
              name="message" 
              value={formData.message}
              onChange={(e) => handleInputChange('message', e.target.value)}
              placeholder="Ton message" 
              className="w-full border px-3 py-2 rounded h-28 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500" 
              required 
              disabled={isLoading}
            />
            <div className="flex gap-3">
              <button 
                type="submit"
                disabled={isLoading}
                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Envoi...' : 'Envoyer'}
              </button>
              
              <button 
                type="button"
                onClick={handleReset}
                disabled={isLoading}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400 disabled:bg-gray-200 disabled:cursor-not-allowed transition-colors"
              >
                Réinitialiser
              </button>
            </div>
          </form>
          
          {/* Redux state demo section */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">État Redux (démo) :</h3>
            <pre className="text-xs text-gray-600 overflow-auto">
              {JSON.stringify({ 
                formData, 
                isLoading, 
                error: error ? error.substring(0, 50) + '...' : null,
                submitted 
              }, null, 2)}
            </pre>
          </div>
        </>
      )}
    </div>
  );
}
