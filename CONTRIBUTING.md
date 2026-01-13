# Contributing to Strategic Futures AI 🤝

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

Follow the instructions in the main [README.md](README.md) to set up your development environment.

## Code Style

### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

### TypeScript/React (Frontend)
- Use TypeScript for type safety
- Follow React best practices and hooks conventions
- Use functional components
- Keep components small and focused

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

Please ensure all tests pass before submitting a pull request.

## Pull Request Process

1. **Update Documentation**: Update README.md or other docs if needed
2. **Add Tests**: Include tests for new features
3. **Follow Commit Conventions**: Use clear, descriptive commit messages
4. **Keep PRs Focused**: One feature or fix per PR
5. **Update CHANGELOG**: Add an entry describing your changes

### Commit Message Format

```
type: brief description

Longer description if needed

Fixes #issue_number
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Areas for Contribution

### High Priority
- [ ] Additional test coverage
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] UI/UX enhancements

### Feature Ideas
- [ ] Export analysis results to PDF/Word
- [ ] Comparison view for multiple analyses
- [ ] Custom scenario parameters
- [ ] Integration with additional LLM providers
- [ ] Collaborative features (share analyses)
- [ ] Data visualization improvements

### Documentation
- [ ] Video tutorials
- [ ] More code examples
- [ ] Architecture diagrams
- [ ] API usage examples

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- General discussions

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
