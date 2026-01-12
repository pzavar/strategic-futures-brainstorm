import { http, HttpResponse } from 'msw'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const handlers = [
  // Auth endpoints
  http.post(`${API_URL}/api/auth/register`, () => {
    return HttpResponse.json({
      access_token: 'mock_token',
      token_type: 'bearer',
    }, { status: 201 })
  }),

  http.post(`${API_URL}/api/auth/login`, () => {
    return HttpResponse.json({
      access_token: 'mock_token',
      token_type: 'bearer',
    })
  }),

  // Analysis endpoints
  http.post(`${API_URL}/api/analyses`, () => {
    return HttpResponse.json({
      id: 1,
      company_name: 'Test Company',
      status: 'pending',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }, { status: 201 })
  }),

  http.get(`${API_URL}/api/analyses`, () => {
    return HttpResponse.json([
      {
        id: 1,
        company_name: 'Test Company',
        status: 'completed',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ])
  }),

  http.get(`${API_URL}/api/analyses/:id`, () => {
    return HttpResponse.json({
      id: 1,
      company_name: 'Test Company',
      status: 'completed',
      company_context: 'Test context',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      scenarios: [],
      strategies: {},
    })
  }),
]

