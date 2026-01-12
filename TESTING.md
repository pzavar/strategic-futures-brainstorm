# Testing Strategy and Report

## Testing Approach

We follow a **Hybrid Testing Strategy** combining:
1. **Test Pyramid**: 70% unit tests, 25% integration tests, 5% E2E tests
2. **Mock-First**: External services (Groq, Tavily) are mocked to avoid rate limits
3. **Incremental Coverage**: Test each component as it's built

## Test Structure

### Backend Tests (`backend/tests/`)
```
tests/
  unit/              # Unit tests for services, utilities
    test_security.py
    test_groq_service.py
    test_tavily_service.py
  integration/       # Integration tests for API endpoints
    test_auth.py
    test_analyses.py
  fixtures/          # Test fixtures and mock data
  conftest.py        # Pytest configuration and fixtures
```

### Frontend Tests (`frontend/src/`)
```
src/
  components/
    __tests__/       # Component tests
  hooks/
    __tests__/       # Hook tests
  test/
    setup.ts         # Test setup
    mocks/           # MSW handlers and server
```

## Running Tests

### Backend
```bash
cd backend
pip install -r requirements-test.txt
pytest                    # Run all tests
pytest tests/unit/        # Run only unit tests
pytest tests/integration/ # Run only integration tests
pytest --cov=app          # Run with coverage
```

### Frontend
```bash
cd frontend
npm install
npm test                  # Run tests in watch mode
npm run test:ui           # Run with UI
npm run test:coverage     # Run with coverage
```

## Test Scenarios

### Backend Unit Tests

#### Security (`test_security.py`)
- ✅ Password hashing and verification
- ✅ JWT token creation and decoding
- ✅ Token expiration handling
- ✅ Invalid token handling

#### Groq Service (`test_groq_service.py`)
- ✅ Successful text generation
- ✅ Generation with system prompt
- ✅ Rate limit retry logic
- ✅ Error handling

#### Tavily Service (`test_tavily_service.py`)
- ✅ Successful search
- ✅ Search with custom max_results
- ✅ Empty results handling

### Backend Integration Tests

#### Auth (`test_auth.py`)
- ✅ User registration
- ✅ Duplicate email handling
- ✅ Successful login
- ✅ Invalid credentials

#### Analyses (`test_analyses.py`)
- ✅ Create analysis
- ✅ List analyses
- ✅ Get analysis details
- ✅ Unauthorized access

### Frontend Tests

#### Components
- ✅ CompanyInput: Form submission, loading states
- ✅ (More component tests to be added)

#### Hooks
- ✅ useAuth: Login, register, logout
- ✅ (More hook tests to be added)

## Coverage Goals

- **Phase 1 (Current)**: Core services → 80%+ coverage
- **Phase 2**: Agents → 70%+ coverage
- **Phase 3**: API endpoints → 60%+ coverage
- **Phase 4**: Frontend components → 50%+ coverage

## Test Data and Fixtures

- Use `faker` for generating test data
- Mock external APIs (Groq, Tavily) to avoid rate limits
- Use in-memory SQLite for database tests
- Use MSW (Mock Service Worker) for frontend API mocking

## Next Steps

1. Add tests for agent functions (research, scenario, strategy)
2. Add tests for pipeline orchestration
3. Add tests for SSE streaming
4. Add E2E tests for critical user flows
5. Increase frontend component test coverage

