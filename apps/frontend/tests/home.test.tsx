/**
 * @jest-environment jsdom
 */
import { render, screen } from '@testing-library/react'
import Home from '../src/app/page'

// Mock next/font/google since it won't work in test environment
jest.mock('next/font/google', () => ({
  Inter: () => ({ className: 'inter-mock' })
}))

describe('Home page', () => {
  it('renders the main heading', () => {
    render(<Home />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeInTheDocument()
  })
})