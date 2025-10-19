# Examples Gallery

Real-world examples of Adaptive Claude Agents in action.

---

## Table of Contents

1. [Example 1: Next.js E-Commerce App](#example-1-nextjs-e-commerce-app)
2. [Example 2: FastAPI Microservice](#example-2-fastapi-microservice)
3. [Example 3: Vanilla PHP CMS](#example-3-vanilla-php-cms)
4. [Example 4: Python ML Pipeline](#example-4-python-ml-pipeline)
5. [Example 5: iOS SwiftUI App](#example-5-ios-swiftui-app)

---

## Example 1: Next.js E-Commerce App

### Project Overview

**Type**: E-commerce web application
**Framework**: Next.js 14 with TypeScript
**Phase**: MVP (v0.5.0)
**Team Size**: 3 developers

### Project Structure

```
ecommerce-app/
├── package.json          # Next.js 14, TypeScript
├── src/
│   ├── app/             # App Router
│   ├── components/      # React components
│   └── lib/             # Utilities
├── __tests__/           # 45 test files
└── .github/
    └── workflows/       # CI/CD with GitHub Actions
```

### Detection Output

```bash
$ python3 skills/project-analyzer/detect_stack.py ~/projects/ecommerce-app

🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     Next.js
Version:       14.2.0
Language:      TypeScript
Styling:       Tailwind CSS
Testing:       Vitest + Testing Library
State:         Zustand
API Client:    fetch (native)
Confidence:    98%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Subagents:
  • nextjs-tester

Generate these subagents? (y/n): y

📝 Generating subagents...
  ✓ Generated: .claude/agents/nextjs-tester.md

✅ Successfully generated 1 subagent!
```

### Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py ~/projects/ecommerce-app

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: MVP
Confidence: 72%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 0.5.0 (0.x.x) → MVP
  • 127 commits → MVP stage
  • 45 test files → basic testing (56% coverage)
  • CI/CD: GitHub Actions ✓
  • README + CONTRIBUTING + 3 doc files

Review Standards (Moderate):
  - Type safety: Enabled (moderate)
  - Test coverage: 50%+ recommended
  - Security: Basic checks (XSS, CSRF)
  - Code style: Lenient
```

### Usage Example

**User**: "Use the nextjs-tester agent to write tests for the ProductCard component"

**Claude (with nextjs-tester)**:

```typescript
// __tests__/components/ProductCard.test.tsx
import { render, screen } from '@testing-library/react'
import { ProductCard } from '@/components/ProductCard'

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    name: 'Laptop',
    price: 999.99,
    imageUrl: '/laptop.jpg'
  }

  it('renders product information correctly', () => {
    render(<ProductCard product={mockProduct} />)

    expect(screen.getByText('Laptop')).toBeInTheDocument()
    expect(screen.getByText('$999.99')).toBeInTheDocument()
    expect(screen.getByRole('img')).toHaveAttribute('src', '/laptop.jpg')
  })

  it('calls onAddToCart when button is clicked', async () => {
    const onAddToCart = vi.fn()
    render(<ProductCard product={mockProduct} onAddToCart={onAddToCart} />)

    await userEvent.click(screen.getByRole('button', { name: /add to cart/i }))

    expect(onAddToCart).toHaveBeenCalledWith(mockProduct.id)
  })
})
```

**Review Behavior (MVP Phase)**:
- ✅ Tests cover main functionality
- ✅ Uses Testing Library best practices
- ⚠️ Suggests 50%+ coverage but doesn't enforce 80%
- ✅ Allows some edge cases to be deferred

---

## Example 2: FastAPI Microservice

### Project Overview

**Type**: User authentication microservice
**Framework**: FastAPI 0.104.1
**Phase**: Production (v1.2.0)
**Team Size**: 5 developers

### Project Structure

```
auth-service/
├── pyproject.toml       # FastAPI, SQLAlchemy, pydantic
├── app/
│   ├── api/            # Endpoints
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic
├── tests/              # 187 test files (85% coverage)
├── alembic/            # Database migrations
└── .github/
    └── workflows/      # CI/CD + security scanning
```

### Detection Output

```bash
$ python3 skills/project-analyzer/detect_stack.py ~/projects/auth-service

🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     FastAPI
Version:       0.104.1
Language:      Python 3.11
Testing:       pytest + pytest-asyncio
ORM:           SQLAlchemy 2.0
Database:      PostgreSQL (asyncpg)
Server:        uvicorn
Migration:     Alembic
Confidence:    96%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Subagents:
  • api-developer
  • api-tester
  • sqlalchemy-specialist

Generate these subagents? (y/n): y

📝 Generating subagents...
  ✓ Generated: .claude/agents/api-developer.md
  ✓ Generated: .claude/agents/api-tester.md
  ✓ Generated: .claude/agents/sqlalchemy-specialist.md

✅ Successfully generated 3 subagents!
```

### Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py ~/projects/auth-service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: Production
Confidence: 92%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 1.2.0 (1.x.x) → Production ✓
  • 487 commits, 12 tags → Production
  • 187 test files → 85% coverage ✓
  • CI/CD: GitHub Actions with security scanning ✓
  • Comprehensive docs (README, API, SECURITY, CHANGELOG)

Review Standards (Strict):
  - Type safety: Strict (pydantic, mypy)
  - Test coverage: 80%+ required ✓
  - Security: Comprehensive (OWASP Top 10, dependency audit)
  - Performance: Required benchmarks
  - Code style: Black + ruff (strict)
```

### Usage Example

**User**: "Use the api-developer agent to add a password reset endpoint"

**Claude (with api-developer)**:

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import PasswordResetRequest, PasswordResetConfirm
from app.services.auth import AuthService
from app.services.email import send_password_reset_email
from app.core.deps import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/password-reset/request")
async def request_password_reset(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Request a password reset email.

    Security:
    - Rate limited (5 requests per hour per IP)
    - No user enumeration (same response for existing/non-existing users)
    - Reset tokens expire in 1 hour
    - Tokens are single-use
    """
    auth_service = AuthService(db)

    # Generate reset token (even if user doesn't exist to prevent enumeration)
    reset_token = await auth_service.generate_reset_token(data.email)

    if reset_token:
        # Send email in background
        background_tasks.add_task(
            send_password_reset_email,
            email=data.email,
            token=reset_token
        )

    # Always return success to prevent user enumeration
    return {
        "message": "If the email exists, a password reset link has been sent."
    }

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Confirm password reset with token.

    Security:
    - Token validation (expiry, single-use)
    - Password strength validation (pydantic schema)
    - Invalidates all existing sessions
    - Logs security event
    """
    auth_service = AuthService(db)

    try:
        await auth_service.reset_password(
            token=data.token,
            new_password=data.new_password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Password reset successful"}
```

**Review Behavior (Production Phase)**:
- ✅ Security-first design (no user enumeration, rate limiting)
- ✅ Comprehensive docstrings
- ✅ Error handling with proper status codes
- ✅ Background tasks for email (non-blocking)
- ✅ Requires tests with 80%+ coverage
- ✅ No `# TODO` comments allowed

---

## Example 3: Vanilla PHP CMS

### Project Overview

**Type**: Custom content management system
**Framework**: Vanilla PHP (no Laravel/Symfony)
**Phase**: MVP (v0.7.0)
**Team Size**: 2 developers

### Project Structure

```
custom-cms/
├── composer.json        # PDO, PHPUnit, Codeception
├── public/
│   └── index.php       # Entry point
├── src/
│   ├── Controllers/    # MVC controllers
│   ├── Models/         # Database models
│   └── Views/          # Templates
├── tests/              # 38 test files
└── playwright/         # E2E tests
```

### Detection Output

```bash
$ python3 skills/project-analyzer/detect_stack.py ~/projects/custom-cms

🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     Vanilla PHP/Web
Version:       PHP 8.2
Language:      PHP
Frontend:      Vanilla JavaScript (ES6+)
Styling:       Custom CSS
Testing:       PHPUnit + Codeception + Playwright
Database:      MySQL (PDO)
Confidence:    100%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Subagents:
  • php-developer
  • playwright-tester
  • vanilla-js-developer
  • mysql-specialist

Generate these subagents? (y/n): y

📝 Generating subagents...
  ✓ Generated: .claude/agents/php-developer.md
  ✓ Generated: .claude/agents/playwright-tester.md
  ✓ Generated: .claude/agents/vanilla-js-developer.md
  ✓ Generated: .claude/agents/mysql-specialist.md

✅ Successfully generated 4 subagents!
```

### Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py ~/projects/custom-cms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: MVP
Confidence: 65%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 0.7.0 (0.x.x) → MVP
  • 89 commits → MVP stage
  • 38 test files → basic testing
  • No CI/CD (manual testing)
  • README + basic documentation

Review Standards (Moderate):
  - Type safety: PHP 8+ type hints recommended
  - Test coverage: 50%+ recommended
  - Security: Basic (SQL injection, XSS, CSRF)
  - Code style: PSR-12 recommended but not enforced
```

### Usage Example

**User**: "Use the php-developer agent to add user authentication"

**Claude (with php-developer)**:

```php
<?php
// src/Controllers/AuthController.php

declare(strict_types=1);

namespace App\Controllers;

use App\Models\User;
use App\Services\SessionManager;

class AuthController
{
    public function __construct(
        private readonly User $userModel,
        private readonly SessionManager $session
    ) {}

    public function login(): void
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            // CSRF protection
            if (!$this->validateCsrfToken($_POST['csrf_token'] ?? '')) {
                http_response_code(403);
                echo json_encode(['error' => 'Invalid CSRF token']);
                return;
            }

            $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
            $password = $_POST['password'] ?? '';

            // Input validation
            if (!$email || !$password) {
                http_response_code(400);
                echo json_encode(['error' => 'Email and password required']);
                return;
            }

            $user = $this->userModel->findByEmail($email);

            // Prevent timing attacks
            if (!$user || !password_verify($password, $user['password_hash'])) {
                // Same response for non-existent user and wrong password
                sleep(1); // Slow down brute force
                http_response_code(401);
                echo json_encode(['error' => 'Invalid credentials']);
                return;
            }

            // Regenerate session ID to prevent fixation
            $this->session->regenerate();
            $this->session->set('user_id', $user['id']);
            $this->session->set('user_email', $user['email']);

            echo json_encode([
                'success' => true,
                'redirect' => '/dashboard'
            ]);
        } else {
            require_once __DIR__ . '/../Views/auth/login.php';
        }
    }

    private function validateCsrfToken(string $token): bool
    {
        return hash_equals(
            $this->session->get('csrf_token') ?? '',
            $token
        );
    }
}
```

**Review Behavior (MVP Phase)**:
- ✅ Security basics covered (CSRF, SQL injection via PDO, XSS via htmlspecialchars)
- ✅ Type hints used (PHP 8+)
- ⚠️ Suggests adding rate limiting but doesn't enforce
- ⚠️ Allows some TODO comments for future improvements

---

## Example 4: Python ML Pipeline

### Project Overview

**Type**: Image classification pipeline
**Framework**: Python ML/CV
**Phase**: Prototype (v0.1.0)
**Team Size**: 1 researcher

### Project Structure

```
ml-pipeline/
├── pyproject.toml       # PyTorch, OpenCV, scikit-learn
├── data/
│   ├── raw/            # Original images
│   └── processed/      # Preprocessed data
├── models/             # Saved models
├── notebooks/          # Jupyter notebooks (12 files)
└── src/
    ├── train.py        # Training script
    └── preprocess.py   # Data preprocessing
```

### Detection Output

```bash
$ python3 skills/project-analyzer/detect_stack.py ~/projects/ml-pipeline

🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     Python ML/CV
Version:       Python 3.10
ML Type:       Computer Vision
Libraries:     PyTorch, OpenCV, scikit-learn, pandas
Notebooks:     12 Jupyter notebooks
Confidence:    88%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Subagents:
  • python-ml-developer
  • cv-specialist

Generate these subagents? (y/n): y

📝 Generating subagents...
  ✓ Generated: .claude/agents/python-ml-developer.md
  ✓ Generated: .claude/agents/cv-specialist.md

✅ Successfully generated 2 subagents!
```

### Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py ~/projects/ml-pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: Prototype
Confidence: 82%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 0.1.0 (0.0.x) → Prototype
  • 18 commits → Early stage
  • 0 test files → Rapid experimentation
  • 12 Jupyter notebooks → Research phase
  • Minimal documentation (README only)

Review Standards (Light):
  - Type safety: Optional (focus on functionality)
  - Testing: Not required (experimentation phase)
  - Security: Deferred
  - Code style: Lenient (allow exploratory code)
  - Documentation: Inline comments sufficient
```

### Usage Example

**User**: "Use the cv-specialist agent to add data augmentation"

**Claude (with cv-specialist)**:

```python
# src/augmentation.py
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

def get_training_transforms(image_size: int = 224):
    """
    Data augmentation pipeline for training.

    Quick implementation for rapid prototyping.
    """
    return A.Compose([
        # Geometric transforms
        A.RandomRotate90(p=0.5),
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(
            shift_limit=0.1,
            scale_limit=0.2,
            rotate_limit=15,
            p=0.5
        ),

        # Color transforms
        A.RandomBrightnessContrast(p=0.3),
        A.HueSaturationValue(p=0.3),

        # Normalize and convert to tensor
        A.Resize(image_size, image_size),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
        ToTensorV2()
    ])

# Quick usage example
if __name__ == "__main__":
    transform = get_training_transforms()
    image = cv2.imread("data/raw/sample.jpg")
    augmented = transform(image=image)["image"]
    print(f"Augmented shape: {augmented.shape}")
```

**Review Behavior (Prototype Phase)**:
- ✅ Focus on functionality (does it work?)
- ✅ Allows TODO comments liberally
- ✅ No test requirements
- ✅ Minimal documentation OK
- ✅ Encourages rapid iteration

---

## Example 5: iOS SwiftUI App

### Project Overview

**Type**: Task management iOS app
**Framework**: SwiftUI + Core Data
**Phase**: MVP (v0.8.0)
**Team Size**: 2 developers

### Project Structure

```
TaskApp/
├── TaskApp.xcodeproj
├── TaskApp/
│   ├── Views/          # SwiftUI views
│   ├── ViewModels/     # MVVM view models
│   ├── Models/         # Data models
│   └── Services/       # API and Core Data
└── TaskAppTests/       # 32 XCTest files
```

### Detection Output

```bash
$ python3 skills/project-analyzer/detect_stack.py ~/projects/TaskApp

🔍 Analyzing project structure...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:     iOS Swift
Version:       Swift 5.9
UI Framework:  SwiftUI
Architecture:  MVVM
Data:          Core Data
Dependencies:  Swift Package Manager
Testing:       XCTest
Confidence:    94%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Subagents:
  • swift-developer

Generate these subagents? (y/n): y

📝 Generating subagents...
  ✓ Generated: .claude/agents/swift-developer.md

✅ Successfully generated 1 subagent!
```

### Phase Detection

```bash
$ python3 skills/adaptive-review/detect_phase.py ~/projects/TaskApp

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Development Phase: MVP
Confidence: 70%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Indicators:
  • Version 0.8.0 (0.x.x) → MVP
  • 95 commits → MVP stage
  • 32 test files → moderate testing
  • TestFlight beta testing
  • README + basic documentation

Review Standards (Moderate):
  - Type safety: Swift enforces at compile time ✓
  - Test coverage: 50%+ recommended
  - Security: Basic (Keychain for sensitive data)
  - Memory management: Check for retain cycles
  - UI/UX: Basic accessibility
```

### Usage Example

**User**: "Use the swift-developer agent to add offline sync"

**Claude (with swift-developer)**:

```swift
// TaskApp/Services/SyncManager.swift
import Foundation
import CoreData
import Combine

@MainActor
class SyncManager: ObservableObject {
    @Published var isSyncing = false
    @Published var lastSyncDate: Date?

    private let apiService: APIService
    private let viewContext: NSManagedObjectContext
    private var cancellables = Set<AnyCancellable>()

    init(
        apiService: APIService = .shared,
        viewContext: NSManagedObjectContext
    ) {
        self.apiService = apiService
        self.viewContext = viewContext
    }

    func sync() async throws {
        isSyncing = true
        defer { isSyncing = false }

        // 1. Push local changes to server
        try await pushLocalChanges()

        // 2. Fetch server changes
        try await pullServerChanges()

        lastSyncDate = Date()
    }

    private func pushLocalChanges() async throws {
        let fetchRequest: NSFetchRequest<Task> = Task.fetchRequest()
        fetchRequest.predicate = NSPredicate(
            format: "needsSync == YES"
        )

        let tasksToSync = try viewContext.fetch(fetchRequest)

        for task in tasksToSync {
            // Create/update on server
            if task.serverId == nil {
                let createdTask = try await apiService.createTask(task)
                task.serverId = createdTask.id
            } else {
                try await apiService.updateTask(task)
            }

            task.needsSync = false
        }

        try viewContext.save()
    }

    private func pullServerChanges() async throws {
        let serverTasks = try await apiService.fetchTasks(
            since: lastSyncDate
        )

        for serverTask in serverTasks {
            // Update or create local task
            let fetchRequest: NSFetchRequest<Task> = Task.fetchRequest()
            fetchRequest.predicate = NSPredicate(
                format: "serverId == %@",
                serverTask.id as CVarArg
            )

            let existingTasks = try viewContext.fetch(fetchRequest)

            if let existingTask = existingTasks.first {
                // Update existing
                existingTask.update(from: serverTask)
            } else {
                // Create new
                let newTask = Task(context: viewContext)
                newTask.update(from: serverTask)
            }
        }

        try viewContext.save()
    }
}

// Extension for updating from server model
extension Task {
    func update(from serverTask: ServerTask) {
        self.serverId = serverTask.id
        self.title = serverTask.title
        self.isCompleted = serverTask.isCompleted
        self.updatedAt = serverTask.updatedAt
        self.needsSync = false
    }
}
```

**Review Behavior (MVP Phase)**:
- ✅ Uses async/await (modern Swift)
- ✅ Proper error handling
- ✅ @MainActor for UI updates
- ⚠️ Suggests adding conflict resolution but doesn't enforce
- ⚠️ Basic error handling OK (comprehensive error UI can wait)

---

## Common Patterns Across Examples

### 1. Progressive Disclosure

All examples follow Anthropic's Progressive Disclosure pattern:
1. **Detect** tech stack automatically
2. **Ask** user for confirmation
3. **Generate** appropriate subagents
4. **Validate** installation

### 2. Phase-Aware Review

Review rigor adapts to development phase:

| Phase | Type Safety | Testing | Security | Code Style |
|-------|-------------|---------|----------|------------|
| **Prototype** | Optional | None | Defer | Lenient |
| **MVP** | Moderate | 50%+ | Basic | Recommended |
| **Production** | Strict | 80%+ | Comprehensive | Enforced |

### 3. Framework-Specific Expertise

Each generated subagent has deep knowledge of:
- Framework best practices
- Testing patterns
- Security considerations
- Common patterns and anti-patterns

### 4. Real-World Complexity

Examples demonstrate:
- Multi-file projects
- Database integration
- API design
- Testing strategies
- Security patterns
- Performance considerations

---

## Try It Yourself!

### Quick Test

```bash
# 1. Install
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash

# 2. Analyze your project
cd your-project
# In Claude Code:
> "Analyze my project and generate appropriate subagents"

# 3. Check your phase
> "What development phase am I in?"

# 4. Use generated subagents
> "Use the [subagent-name] to [task]"
```

### Share Your Example!

Found Adaptive Claude Agents useful? Share your experience:

- 📝 [Submit your example](https://github.com/SawanoLab/adaptive-claude-agents/issues/new?template=example_submission.md)
- 💬 [Discuss use cases](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- ⭐ [Star the repo](https://github.com/SawanoLab/adaptive-claude-agents)

---

**Happy Coding!** 🚀

For more help, see:
- [Quick Start Guide](./QUICKSTART.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [Full Documentation](../README.md)
