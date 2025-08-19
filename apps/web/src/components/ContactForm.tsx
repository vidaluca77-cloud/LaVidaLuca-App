'use client'

import React, { useState } from 'react'
import { useSubmitContactMutation } from '../lib/api/contactsApi'

interface ContactFormData {
  name: string
  email: string
  phone: string
  organization: string
  subject: string
  message: string
  contact_type: string
  consent_privacy: boolean
  consent_marketing: boolean
}

export default function ContactForm() {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    phone: '',
    organization: '',
    subject: '',
    message: '',
    contact_type: 'general',
    consent_privacy: false,
    consent_marketing: false
  })

  const [submitContact, { isLoading, error, isSuccess }] = useSubmitContactMutation()

  const contactTypes = [
    { value: 'general', label: 'Question générale', icon: '💬' },
    { value: 'partnership', label: 'Partenariat', icon: '🤝' },
    { value: 'support', label: 'Support technique', icon: '🔧' },
    { value: 'formation', label: 'Information formation', icon: '📚' },
    { value: 'press', label: 'Presse & Médias', icon: '📰' },
    { value: 'recruitment', label: 'Recrutement', icon: '👥' }
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked
      setFormData(prev => ({
        ...prev,
        [name]: checked
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.consent_privacy) {
      alert('Vous devez accepter la politique de confidentialité pour continuer.')
      return
    }

    try {
      await submitContact({
        name: formData.name,
        email: formData.email,
        phone: formData.phone || undefined,
        organization: formData.organization || undefined,
        subject: formData.subject,
        message: formData.message,
        contact_type: formData.contact_type,
        consent_privacy: formData.consent_privacy,
        consent_marketing: formData.consent_marketing
      }).unwrap()
      
      // Reset form on success
      setFormData({
        name: '',
        email: '',
        phone: '',
        organization: '',
        subject: '',
        message: '',
        contact_type: 'general',
        consent_privacy: false,
        consent_marketing: false
      })
    } catch (err) {
      console.error('Erreur lors de l\'envoi:', err)
    }
  }

  if (isSuccess) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Message envoyé avec succès !
          </h2>
          <p className="text-gray-600 mb-6">
            Nous avons bien reçu votre message et vous répondrons dans les plus brefs délais.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Envoyer un autre message
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="p-8 border-b border-gray-200">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Contactez-nous
          </h1>
          <p className="text-gray-600">
            Vous avez des questions sur nos formations ou souhaitez établir un partenariat ? 
            N'hésitez pas à nous contacter !
          </p>
        </div>

        {/* Contact Info */}
        <div className="p-8 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl mb-2">📧</div>
              <h3 className="font-semibold text-gray-900">Email</h3>
              <p className="text-gray-600">contact@lavidaluca.fr</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">📞</div>
              <h3 className="font-semibold text-gray-900">Téléphone</h3>
              <p className="text-gray-600">+33 1 23 45 67 89</p>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-2">⏰</div>
              <h3 className="font-semibold text-gray-900">Horaires</h3>
              <p className="text-gray-600">Lun-Ven: 9h-18h</p>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-8">
          <div className="space-y-6">
            {/* Contact Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Type de demande *
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {contactTypes.map((type) => (
                  <label
                    key={type.value}
                    className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                      formData.contact_type === type.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <input
                      type="radio"
                      name="contact_type"
                      value={type.value}
                      checked={formData.contact_type === type.value}
                      onChange={handleChange}
                      className="sr-only"
                    />
                    <span className="text-lg mr-3">{type.icon}</span>
                    <span className="text-sm font-medium">{type.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Personal Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom complet *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Votre nom et prénom"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="votre@email.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Téléphone
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="+33 1 23 45 67 89"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Organisation
                </label>
                <input
                  type="text"
                  name="organization"
                  value={formData.organization}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="MFR, lycée, entreprise..."
                />
              </div>
            </div>

            {/* Subject */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sujet *
              </label>
              <input
                type="text"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Résumé de votre demande"
              />
            </div>

            {/* Message */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message *
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                placeholder="Décrivez votre demande en détail..."
              />
            </div>

            {/* Consent */}
            <div className="space-y-3">
              <label className="flex items-start gap-3">
                <input
                  type="checkbox"
                  name="consent_privacy"
                  checked={formData.consent_privacy}
                  onChange={handleChange}
                  className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">
                  J'accepte la{' '}
                  <a href="/privacy" className="text-blue-600 hover:underline">
                    politique de confidentialité
                  </a>{' '}
                  et consens au traitement de mes données personnelles pour traiter ma demande. *
                </span>
              </label>

              <label className="flex items-start gap-3">
                <input
                  type="checkbox"
                  name="consent_marketing"
                  checked={formData.consent_marketing}
                  onChange={handleChange}
                  className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">
                  J'accepte de recevoir des informations sur les activités et nouveautés de La Vida Luca.
                </span>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex items-center gap-2">
                  <span className="text-red-600">⚠️</span>
                  <span className="text-red-800">
                    Erreur lors de l'envoi du message. Veuillez réessayer.
                  </span>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading || !formData.consent_privacy}
                className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Envoi en cours...
                  </div>
                ) : (
                  'Envoyer le message'
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}