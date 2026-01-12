import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CompanyInput } from '../CompanyInput'

describe('CompanyInput', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders input and submit button', () => {
    const onSubmit = vi.fn()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    expect(screen.getByPlaceholderText(/enter company name or ticker/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument()
  })

  it('calls onSubmit with normalized company name when exact match is submitted', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const input = screen.getByPlaceholderText(/enter company name or ticker/i)
    const button = screen.getByRole('button', { name: /analyze/i })
    
    await user.type(input, 'Apple')
    await user.click(button)
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith('Apple Inc.')
    })
  })

  it('calls onSubmit with normalized company name when ticker is submitted', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const input = screen.getByPlaceholderText(/enter company name or ticker/i)
    const button = screen.getByRole('button', { name: /analyze/i })
    
    await user.type(input, 'AAPL')
    await user.click(button)
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith('Apple Inc.')
    })
  })

  it('calls onSubmit with normalized company name when typo is submitted', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const input = screen.getByPlaceholderText(/enter company name or ticker/i)
    const button = screen.getByRole('button', { name: /analyze/i })
    
    await user.type(input, 'Aple')
    await user.click(button)
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith('Apple Inc.')
    })
  })

  it('disables button when loading', () => {
    const onSubmit = vi.fn()
    render(<CompanyInput onSubmit={onSubmit} loading={true} />)
    
    const button = screen.getByRole('button', { name: /analyzing/i })
    expect(button).toBeDisabled()
  })

  it('disables button when input is empty', () => {
    const onSubmit = vi.fn()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const button = screen.getByRole('button', { name: /analyze/i })
    expect(button).toBeDisabled()
  })

  it('shows dropdown options when typing', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const input = screen.getByPlaceholderText(/enter company name or ticker/i)
    await user.type(input, 'App')
    
    await waitFor(() => {
      expect(screen.getByText(/Apple Inc./i)).toBeInTheDocument()
    })
  })

  it('handles case-insensitive matching', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()
    render(<CompanyInput onSubmit={onSubmit} />)
    
    const input = screen.getByPlaceholderText(/enter company name or ticker/i)
    const button = screen.getByRole('button', { name: /analyze/i })
    
    await user.type(input, 'APPLE')
    await user.click(button)
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith('Apple Inc.')
    })
  })
})

