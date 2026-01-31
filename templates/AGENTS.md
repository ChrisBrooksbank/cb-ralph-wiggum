# AGENTS.md - Operational Guide

Keep this file under 60 lines. It's loaded every iteration.

## Build Commands

```bash
npm run build          # Production build
npm run dev            # Development server
```

## Test Commands

```bash
npm test               # Run tests (watch mode)
npm run test:run       # Run tests once
npm run test:coverage  # Coverage report
```

## Validation (run before committing)

```bash
npm run check          # Run ALL checks (typecheck, lint, format, tests)
```

## Project Structure

```
src/
├── lib/           # Shared utilities
├── components/    # UI components
├── core/          # Business logic
└── types/         # TypeScript types
```

## Code Patterns

- Use TypeScript strict mode
- Follow existing naming conventions
- Write tests for new functionality
- Keep functions small and focused

## Notes

<!-- Add learnings from iterations here -->
