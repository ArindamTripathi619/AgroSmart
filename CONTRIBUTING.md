# 🤝 Contributing to AgroSmart

Thank you for your interest in contributing to AgroSmart! This document provides guidelines for contributing to this educational project.

## 📋 Project Purpose

AgroSmart is an educational demonstration project showcasing:
- React + TypeScript frontend development
- Python FastAPI backend development
- Machine Learning integration in web applications
- Agricultural technology applications

## 🎯 Areas for Contribution

### 1. Code Improvements
- Bug fixes
- Performance optimizations
- Code refactoring
- Type safety improvements

### 2. Features
- Additional prediction models
- New visualization types
- UI/UX enhancements
- Accessibility improvements

### 3. Documentation
- README improvements
- Code comments
- API documentation
- Tutorial creation

### 4. Testing
- Unit tests
- Integration tests
- E2E tests
- Performance testing

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" button on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AgroSmart.git
cd AgroSmart
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- Follow existing code style
- Add comments where necessary
- Update documentation if needed

### 4. Test Your Changes
```bash
# Frontend
npm run lint
npm run typecheck
npm run dev

# Backend (when implemented)
pytest
python -m mypy .
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug"
```

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

## 📝 Commit Message Convention

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add weather data integration
fix: resolve yield calculation error
docs: update setup guide
style: format code with prettier
refactor: optimize crop prediction logic
test: add unit tests for fertilizer API
chore: update dependencies
```

## 🎨 Code Style Guidelines

### TypeScript/React
- Use functional components
- Prefer `const` over `let`
- Use TypeScript interfaces
- Follow existing naming conventions
- Add JSDoc comments for complex functions

### Python
- Follow PEP 8 style guide
- Use type hints
- Add docstrings for functions
- Keep functions small and focused

## 🧪 Testing Guidelines

### Frontend Tests
- Test user interactions
- Test component rendering
- Test API integration
- Test edge cases

### Backend Tests
- Test API endpoints
- Test model predictions
- Test data validation
- Test error handling

## 📚 Documentation Standards

- Keep README up to date
- Document all API endpoints
- Add inline comments for complex logic
- Update CHANGELOG for significant changes

## 🐛 Bug Reports

When reporting bugs, include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details

## 💡 Feature Requests

When suggesting features:
- Describe the feature
- Explain the use case
- Provide examples
- Consider implementation complexity

## ⚖️ Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the project goals

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's license.

## 🙏 Thank You!

Every contribution, no matter how small, is valuable to this project!
