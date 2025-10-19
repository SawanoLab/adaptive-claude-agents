# 実例集

このドキュメントでは、Adaptive Claude Agentsがさまざまなプロジェクトタイプをどのように検出し、適切なサブエージェントを生成するかを、実際の例を通して示します。

## 目次

- [例1: Next.js + TypeScriptプロジェクト](#例1-nextjs--typescriptプロジェクト)
- [例2: Python FastAPIプロジェクト](#例2-python-fastapiプロジェクト)
- [例3: React + Viteプロジェクト](#例3-react--viteプロジェクト)
- [例4: フルスタックモノレポ](#例4-フルスタックモノレポ)
- [例5: レガシーJavaScript + Express](#例5-レガシーjavascript--express)

---

## 例1: Next.js + TypeScriptプロジェクト

### プロジェクト構造

```
my-nextjs-app/
├── package.json
├── next.config.js
├── tsconfig.json
├── .git/
│   └── logs/
│       ├── refs/heads/main (25+ commits)
│       └── HEAD
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   └── lib/
│       └── utils.ts
├── public/
│   └── images/
└── README.md
```

### package.json

```json
{
  "name": "my-nextjs-app",
  "version": "0.3.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
```

### 検出出力

```
Project Analyzer Results
========================

Detected Stack:
  - next.js (confidence: 0.95)
    Evidence:
      - package.json contains "next": "14.0.0"
      - Found next.config.js
      - Using app directory (Next.js 13+)

  - typescript (confidence: 0.90)
    Evidence:
      - Found tsconfig.json
      - .tsx files in src/

  - react (confidence: 0.95)
    Evidence:
      - package.json contains "react": "^18.2.0"
      - Component files found

Development Phase: MVP
  Indicators:
    - Version: 0.3.0 (pre-1.0)
    - Git commits: 27 (medium activity)
    - Has basic documentation (README.md)
    - No CI/CD detected
    - No test files found

Recommended Review Rigor: MEDIUM
  - Focus on architecture and patterns
  - Encourage testing setup
  - Validate type safety
  - Review component structure

Generated Subagents:
  1. Frontend Developer (Next.js specialist)
     - App Router expertise
     - TypeScript best practices
     - React component patterns

  2. Code Reviewer
     - Review rigor: MEDIUM
     - Focus areas:
       * Component architecture
       * Type safety
       * Performance considerations
       * Accessibility basics

  3. TypeScript Specialist
     - Type definitions
     - Generic usage
     - Type narrowing

Subagents saved to: /Users/you/.config/claude/subagents/my-nextjs-app/
```

### 生成されたサブエージェント

#### 1. Frontend Developer

```markdown
---
name: Frontend Developer
description: Next.js 14 (App Router) + TypeScript specialist
stack: [nextjs, typescript, react]
phase: mvp
---

# Role

You are an expert Next.js developer specializing in the App Router (Next.js 13+)
with TypeScript. Help build scalable, type-safe React applications.

# Expertise

- Next.js App Router architecture
- React Server Components
- TypeScript best practices
- Modern React patterns (hooks, context, suspense)
- CSS Modules / Tailwind CSS
- API Routes and Server Actions

# Current Project Context

This is an MVP-stage Next.js project using:
- Next.js 14 with App Router
- TypeScript
- React 18

The project is in active development (27 commits) but still pre-1.0.

# Development Guidelines

## Component Structure
- Use TypeScript for all components
- Prefer Server Components when possible
- Client Components only when necessary ('use client')
- Keep components focused and reusable

## Type Safety
- Define proper TypeScript interfaces
- Avoid `any` types
- Use strict mode settings

## File Organization
- Follow Next.js conventions (app/, components/, lib/)
- Colocate related files
- Use barrel exports for cleaner imports

# Code Review Focus (MEDIUM Rigor)

When reviewing code:
- Validate TypeScript usage and type safety
- Check component architecture
- Ensure proper Server/Client component usage
- Suggest performance optimizations
- Recommend testing for critical paths
- Verify accessibility basics (semantic HTML, ARIA when needed)

# Common Tasks

- Create new pages and layouts
- Build reusable components
- Implement API routes or Server Actions
- Add TypeScript types
- Optimize performance
- Debug rendering issues

# Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
```

#### 2. Code Reviewer

```markdown
---
name: Code Reviewer
description: Medium-rigor reviewer for MVP-stage Next.js project
phase: mvp
rigor: medium
---

# Role

You perform code reviews for this MVP-stage Next.js + TypeScript project,
balancing quality with development speed.

# Review Rigor: MEDIUM

## What to Focus On

### Architecture & Patterns
- Component structure and organization
- Proper use of Server vs Client Components
- State management approach
- API design

### Type Safety
- TypeScript usage (no `any` unless justified)
- Proper interface/type definitions
- Type narrowing and guards

### Best Practices
- React best practices (hooks rules, key props, etc.)
- Next.js conventions (metadata, routing, data fetching)
- Error handling
- Basic accessibility (semantic HTML, alt text)

### Testing Mindset
- Encourage adding tests for critical features
- Suggest testable code structure
- Recommend starting with integration tests

## What NOT to Nitpick (Yet)

- Perfect test coverage (encourage, but don't block)
- Advanced performance optimizations
- Complete documentation
- Minor style inconsistencies (use Prettier/ESLint instead)

## Review Checklist

- [ ] Code follows TypeScript strict mode
- [ ] Components are properly structured
- [ ] No obvious bugs or edge cases
- [ ] Error handling exists for user-facing features
- [ ] Code is reasonably readable
- [ ] Follows Next.js conventions
- [ ] No security issues (XSS, injection, etc.)

## Feedback Style

- Be constructive and educational
- Explain *why*, not just *what*
- Suggest improvements without blocking progress
- Celebrate good patterns when you see them

## Example Review Comments

**Good**:
> Consider extracting this logic into a custom hook for reusability.
> This would also make it easier to test. For example: `useUserData()`

**Too Strict for MVP**:
> This component needs unit tests, integration tests, and E2E tests
> before we can merge. Also add Storybook stories.

**Too Lenient**:
> LGTM 👍

(Always provide specific feedback, even if positive)
```

---

## 例2: Python FastAPIプロジェクト

### プロジェクト構造

```
fastapi-service/
├── pyproject.toml
├── requirements.txt
├── .git/
│   └── logs/
│       └── refs/heads/main (150+ commits)
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py
│   └── dependencies.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── conftest.py
├── alembic/
│   └── versions/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
└── docker-compose.yml
```

### pyproject.toml

```toml
[tool.poetry]
name = "fastapi-service"
version = "1.2.3"
description = "Production FastAPI service"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
sqlalchemy = "^2.0.0"
alembic = "^1.12.0"
pydantic = "^2.4.0"
pydantic-settings = "^2.0.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.25.0"
```

### 検出出力

```
Project Analyzer Results
========================

Detected Stack:
  - fastapi (confidence: 0.95)
    Evidence:
      - pyproject.toml contains "fastapi"
      - Found app/main.py with FastAPI app
      - Standard FastAPI structure (routers, models)

  - python (confidence: 1.0)
    Evidence:
      - Found pyproject.toml
      - Python files detected

  - sqlalchemy (confidence: 0.90)
    Evidence:
      - pyproject.toml contains "sqlalchemy"
      - Found alembic/ directory (migrations)
      - Database models in app/models/

  - postgresql (confidence: 0.70)
    Evidence:
      - docker-compose.yml has postgres service
      - Alembic configuration present

Development Phase: PRODUCTION
  Indicators:
    - Version: 1.2.3 (stable, post-1.0)
    - Git commits: 156 (high activity, mature)
    - Has comprehensive tests (tests/ directory)
    - CI/CD present (.github/workflows/)
    - Has database migrations (alembic/)
    - Dockerized

Recommended Review Rigor: STRICT
  - Enforce comprehensive testing
  - Validate security practices
  - Review performance implications
  - Check error handling and edge cases
  - Verify backward compatibility

Generated Subagents:
  1. Backend Developer (FastAPI specialist)
     - RESTful API design
     - Async Python patterns
     - Database integration

  2. Code Reviewer
     - Review rigor: STRICT
     - Focus areas:
       * Security (SQL injection, auth, etc.)
       * Performance and scalability
       * Test coverage
       * Error handling
       * API versioning
       * Breaking changes

  3. Database Specialist
     - SQLAlchemy ORM
     - Alembic migrations
     - Query optimization

  4. DevOps Consultant
     - Docker configuration
     - CI/CD optimization
     - Deployment strategies

Subagents saved to: /Users/you/.config/claude/subagents/fastapi-service/
```

### 主な違い（Next.jsの例と比較）

1. **開発フェーズ**: PRODUCTION（v1.2.3、テスト・CI/CDあり）
2. **レビュー厳格度**: STRICT（セキュリティ、パフォーマンス、テストが必須）
3. **サブエージェント**: DevOps Consultantが追加（本番環境のため）
4. **フォーカス**: アーキテクチャよりもセキュリティと安定性

---

## 例3: React + Viteプロジェクト

### プロジェクト構造

```
my-vite-app/
├── package.json
├── vite.config.ts
├── index.html
├── .git/
│   └── logs/
│       └── refs/heads/main (3 commits)
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   └── vite-env.d.ts
└── public/
```

### package.json

```json
{
  "name": "my-vite-app",
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

### 検出出力

```
Project Analyzer Results
========================

Detected Stack:
  - vite (confidence: 0.95)
    Evidence:
      - package.json contains "vite": "^5.0.0"
      - Found vite.config.ts
      - index.html in root (Vite convention)

  - react (confidence: 0.95)
    Evidence:
      - package.json contains "react"
      - Found @vitejs/plugin-react
      - .tsx files in src/

  - typescript (confidence: 0.90)
    Evidence:
      - Found vite.config.ts and .tsx files
      - @types/* packages in devDependencies

Development Phase: PROTOTYPE
  Indicators:
    - Version: 0.0.1 (very early)
    - Git commits: 3 (just started)
    - Minimal structure (only basic files)
    - No tests detected
    - No CI/CD
    - No documentation beyond basic setup

Recommended Review Rigor: LIGHT
  - Focus on core functionality
  - Encourage experimentation
  - Quick feedback on critical issues only
  - Don't block on testing/docs yet

Generated Subagents:
  1. Frontend Developer (React + Vite specialist)
     - Vite configuration
     - React development
     - TypeScript setup

  2. Code Reviewer
     - Review rigor: LIGHT
     - Focus areas:
       * Basic functionality works
       * No obvious security issues
       * Code is readable
       * Suggest architectural direction (not enforce)

Subagents saved to: /Users/you/.config/claude/subagents/my-vite-app/
```

### コードレビューサンプル（軽量版）

```markdown
# Code Reviewer (LIGHT Rigor - Prototype Phase)

## Review Philosophy

This is a prototype. The goal is to **move fast and explore ideas**.

## What to Check

- Does the code work?
- Are there any critical bugs or security issues?
- Is it readable enough to iterate on?

## What to Suggest (Not Require)

- Potential architectural directions
- Libraries that might help
- Patterns to consider as the project grows

## What to Ignore

- Test coverage (for now)
- Perfect TypeScript types
- Documentation
- Performance optimization
- Edge case handling

## Example Feedback

**Good**:
> This works! As you build out the feature, you might want to consider
> extracting the API logic into a separate hook. But for now, this is fine.

**Too Strict**:
> You need to add error boundaries, loading states, retry logic, and tests.

**Just Right**:
> Nice start! The component is clear. One quick note: you might want to
> add basic error handling for the fetch call to avoid crashes.
```

---

## 例4: フルスタックモノレポ

### プロジェクト構造

```
fullstack-monorepo/
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
├── .git/
│   └── logs/
│       └── refs/heads/main (80 commits)
├── apps/
│   ├── web/
│   │   ├── package.json (Next.js)
│   │   ├── next.config.js
│   │   └── src/
│   └── api/
│       ├── package.json (NestJS)
│       ├── nest-cli.json
│       └── src/
├── packages/
│   ├── ui/
│   │   ├── package.json (React components)
│   │   └── src/
│   ├── config/
│   │   └── package.json (shared config)
│   └── types/
│       └── package.json (shared TypeScript types)
└── README.md
```

### ルートpackage.json

```json
{
  "name": "fullstack-monorepo",
  "version": "0.8.0",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "typescript": "^5.0.0"
  }
}
```

### 検出出力

```
Project Analyzer Results
========================

Detected Stack:
  - monorepo (confidence: 0.95)
    Evidence:
      - Found pnpm-workspace.yaml
      - Found turbo.json
      - Multiple package.json files (workspaces)

  - nextjs (confidence: 0.90)
    Evidence:
      - apps/web/package.json contains "next"
      - Found apps/web/next.config.js

  - nestjs (confidence: 0.85)
    Evidence:
      - apps/api/package.json contains "@nestjs/core"
      - Found nest-cli.json

  - typescript (confidence: 0.95)
    Evidence:
      - TypeScript in all subprojects
      - Shared types package

Development Phase: MVP (transitioning to Production)
  Indicators:
    - Version: 0.8.0 (approaching 1.0)
    - Git commits: 80 (active development)
    - Well-structured (monorepo with shared packages)
    - Some testing (test scripts present)
    - No CI/CD detected yet
    - Comprehensive README

Recommended Review Rigor: MEDIUM-STRICT
  - Enforce consistency across workspaces
  - Validate shared types usage
  - Review monorepo-specific patterns
  - Check for code duplication
  - Ensure proper dependency management

Generated Subagents:
  1. Monorepo Architect
     - Turborepo optimization
     - Workspace management
     - Shared package design

  2. Frontend Developer (Next.js)
     - Next.js best practices
     - Shared UI component usage

  3. Backend Developer (NestJS)
     - NestJS patterns
     - API design
     - Shared types integration

  4. Code Reviewer
     - Review rigor: MEDIUM-STRICT
     - Focus areas:
       * Cross-workspace consistency
       * Shared type safety
       * No circular dependencies
       * Proper package boundaries
       * Build optimization

  5. TypeScript Specialist
     - Shared types package
     - Type consistency across apps

Subagents saved to: /Users/you/.config/claude/subagents/fullstack-monorepo/
```

### モノレポ特有の考慮事項

#### Monorepo Architect Subagent（抜粋）

```markdown
# Monorepo-Specific Guidance

## Workspace Management

- Keep packages focused and single-purpose
- Use proper dependency declarations (workspace:*)
- Avoid circular dependencies between packages

## Shared Packages

### packages/ui
- Reusable React components
- Should not depend on app-specific logic
- Export via barrel files (index.ts)

### packages/types
- Shared TypeScript interfaces/types
- Single source of truth for data models
- Used by both web and api

### packages/config
- Shared ESLint, TypeScript, Tailwind configs
- Enforces consistency across apps

## Build Optimization

- Use Turbo caching effectively
- Define proper task dependencies in turbo.json
- Avoid unnecessary rebuilds

## Common Issues

1. **Dependency Version Mismatches**
   - Use pnpm to enforce single versions
   - Check with `pnpm list <package>`

2. **Circular Dependencies**
   - packages/ui should NOT import from apps/*
   - apps/* CAN import from packages/*
   - packages/* can import from other packages/* (carefully)

3. **Build Order**
   - Shared packages must build before apps
   - Turbo handles this automatically
```

---

## 例5: レガシーJavaScript + Express

### プロジェクト構造

```
legacy-express-app/
├── package.json
├── .git/
│   └── logs/
│       └── refs/heads/master (450+ commits)
├── server.js
├── routes/
│   ├── users.js
│   ├── products.js
│   └── orders.js
├── views/
│   └── *.ejs
├── public/
│   ├── css/
│   └── js/
└── config/
    └── database.js
```

### package.json

```json
{
  "name": "legacy-express-app",
  "version": "2.3.1",
  "description": "Legacy e-commerce backend",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "ejs": "^3.1.6",
    "mysql": "^2.18.1",
    "body-parser": "^1.19.0",
    "express-session": "^1.17.1"
  }
}
```

### server.js

```javascript
const express = require('express');
const app = express();

// ... legacy code, no TypeScript, callbacks everywhere
```

### 検出出力

```
Project Analyzer Results
========================

Detected Stack:
  - express (confidence: 0.95)
    Evidence:
      - package.json contains "express": "^4.17.1"
      - Found server.js (common Express pattern)
      - Routes directory with .js files

  - javascript (confidence: 1.0)
    Evidence:
      - No TypeScript detected
      - .js files only
      - No type definitions

  - mysql (confidence: 0.85)
    Evidence:
      - package.json contains "mysql"
      - Found config/database.js

  - ejs (confidence: 0.80)
    Evidence:
      - package.json contains "ejs"
      - .ejs files in views/

Development Phase: PRODUCTION (Legacy)
  Indicators:
    - Version: 2.3.1 (stable, production)
    - Git commits: 458 (very mature project)
    - No modern tooling (no TypeScript, no tests, no CI/CD)
    - No recent major changes (legacy maintenance mode)

  ⚠️  Legacy Project Detected:
    - Consider modernization strategy
    - High risk for changes (no tests)
    - Use extra caution with refactoring

Recommended Review Rigor: STRICT (Legacy-Aware)
  - Extreme caution with changes
  - Require manual testing for all changes
  - No breaking changes without migration plan
  - Focus on backward compatibility
  - Document all changes thoroughly

Generated Subagents:
  1. Backend Developer (Express/Legacy specialist)
     - Express 4.x patterns
     - Callback-based async handling
     - EJS templating
     - MySQL integration

  2. Code Reviewer (Legacy-Aware)
     - Review rigor: STRICT
     - Focus areas:
       * Backward compatibility (critical!)
       * SQL injection prevention
       * Session security
       * No breaking changes
       * Manual testing checklist
       * Rollback plan

  3. Modernization Consultant
     - Suggest gradual improvements
     - TypeScript migration path
     - Testing strategy
     - Async/await refactoring
     - Security updates

  4. Database Specialist (MySQL)
     - Query optimization
     - Migration safety
     - Backup verification

Subagents saved to: /Users/you/.config/claude/subagents/legacy-express-app/
```

### レガシープロジェクト向けコードレビュー（抜粋）

```markdown
# Code Reviewer (STRICT - Legacy Production)

## ⚠️ Legacy Project - Special Considerations

This is a production system with NO automated tests. Every change carries risk.

## Review Checklist (All Required)

- [ ] Does this change maintain backward compatibility?
- [ ] Is there a rollback plan?
- [ ] Has this been manually tested in a staging environment?
- [ ] Are all SQL queries safe from injection?
- [ ] Does this affect session handling or authentication?
- [ ] Is there documentation for this change?
- [ ] Have stakeholders been notified of the change?

## Security Focus

Legacy code often has security issues. Check for:

- SQL injection (use parameterized queries)
- XSS vulnerabilities (escape user input in templates)
- Session fixation
- Insecure dependencies (check with `npm audit`)

## Modernization Suggestions

When reviewing, you may suggest gradual improvements:

**Good Incremental Suggestions**:
- Replace one callback with async/await
- Add JSDoc comments for better IDE support
- Introduce one test for critical path
- Update one insecure dependency

**Bad Suggestions**:
- "Rewrite everything in TypeScript"
- "Replace Express with NestJS"
- "Migrate from MySQL to PostgreSQL"

(Too risky for a legacy production system)

## Feedback Template

For each change, provide:

1. **Risk Assessment**: Low/Medium/High
2. **Testing Checklist**: Specific scenarios to test manually
3. **Rollback Steps**: How to undo this change
4. **Backward Compatibility**: What might break?
```

### Modernization Consultant Subagent（抜粋）

```markdown
# Modernization Consultant

## Role

Help gradually modernize this legacy Express application without breaking production.

## Modernization Strategy (Gradual)

### Phase 1: Foundation (Current - 3 months)
- Add basic testing (start with critical paths)
- Update insecure dependencies
- Add TypeScript (allow JS) with JSDoc comments
- Set up CI/CD for automated testing

### Phase 2: Incremental Improvement (3-6 months)
- Convert one route at a time to async/await
- Migrate one module to TypeScript
- Add integration tests
- Improve error handling

### Phase 3: Architecture (6-12 months)
- Consider microservices for new features
- Evaluate ORM (Sequelize, TypeORM) vs raw MySQL
- Modernize frontend (if needed)

## Quick Wins (Safe Improvements)

1. **Add `.editorconfig` and `.eslintrc`**
   - Enforce consistent style
   - Catch common errors

2. **Add `helmet` and security middleware**
   ```javascript
   const helmet = require('helmet');
   app.use(helmet());
   ```

3. **Environment variables (dotenv)**
   - Stop hardcoding credentials

4. **Add basic logging**
   - Use `winston` or `pino`
   - Track errors in production

5. **Dependency updates (careful!)**
   - Update one at a time
   - Test thoroughly

## What NOT to Do

- Don't rewrite everything at once
- Don't change database schema without migration plan
- Don't break existing APIs (users depend on them)
- Don't force latest tools if they don't fit
```

---

## まとめ

この5つの例は、Adaptive Claude Agentsがさまざまなプロジェクトタイプと開発段階にどのように適応するかを示しています：

| 例 | フェーズ | レビュー厳格度 | 主な特徴 |
|----|---------|--------------|----------|
| Next.js + TS | MVP | Medium | バランス型、テスト推奨 |
| FastAPI | Production | Strict | セキュリティ・パフォーマンス重視 |
| React + Vite | Prototype | Light | 実験を促進、スピード重視 |
| モノレポ | MVP→Production | Medium-Strict | 一貫性・境界線重視 |
| Legacy Express | Production (Legacy) | Strict (Legacy-Aware) | 後方互換性・リスク管理重視 |

各プロジェクトには、その技術スタック、開発段階、コンテキストに合わせた専門的なサブエージェントが生成されます。

---

**関連ドキュメント**:
- [実装計画](./IMPLEMENTATION.md) - 検出ロジックの詳細
- [ベストプラクティス](./BEST_PRACTICES.md) - サブエージェント設計ガイドライン
- [README](../README.md) - プロジェクト概要
