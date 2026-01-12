import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider, useAuth } from '../useAuth'
import api from '../../services/api'

vi.mock('../../services/api')
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => vi.fn(),
  }
})

describe('useAuth', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('provides auth context', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <BrowserRouter>
        <AuthProvider>{children}</AuthProvider>
      </BrowserRouter>
    )

    const { result } = renderHook(() => useAuth(), { wrapper })

    expect(result.current).toHaveProperty('user')
    expect(result.current).toHaveProperty('login')
    expect(result.current).toHaveProperty('register')
    expect(result.current).toHaveProperty('logout')
  })

  it('login sets token and user', async () => {
    const mockPost = vi.fn().mockResolvedValue({
      data: { access_token: 'test_token', token_type: 'bearer' },
    })
    ;(api.post as any) = mockPost

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <BrowserRouter>
        <AuthProvider>{children}</AuthProvider>
      </BrowserRouter>
    )

    const { result } = renderHook(() => useAuth(), { wrapper })

    await act(async () => {
      await result.current.login('test@example.com', 'password123')
    })

    expect(localStorage.getItem('strategic_futures_token')).toBe('test_token')
    expect(result.current.user).toBeTruthy()
  })
})

