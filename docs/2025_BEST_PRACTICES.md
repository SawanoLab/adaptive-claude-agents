# 2025 Framework Best Practices & Recommendations

**Last Updated**: 2025-10-20
**Purpose**: Framework-specific best practices and recommended tools for 2025

This document provides up-to-date guidance on modern development patterns, tool selection, and architectural decisions for each supported framework.

---

## Table of Contents

- [Browser Automation](#browser-automation)
- [Next.js 15](#nextjs-15)
- [FastAPI](#fastapi)
- [Go Frameworks](#go-frameworks-gin-fiber-echo)
- [Flutter](#flutter-state-management)
- [Python ML/CV](#python-mlcv-pytorch-vs-tensorflow)
- [iOS Swift](#ios-swift-swiftui-vs-uikit)
- [React State Management](#react-state-management-vite)
- [Activation Triggers Guide](#activation-triggers-guide)

---

## Browser Automation

### Chrome DevTools MCP vs Playwright MCP

**Recommendation**: **Chrome DevTools MCP for 90% of web development**

| Aspect | Chrome DevTools MCP | Playwright MCP |
|--------|-------------------|----------------|
| **Use Case** | ✅ Default for most development | Cross-browser testing only |
| **Browsers** | Chrome, Edge | Chrome, Firefox, Safari |
| **Performance** | ✅ Excellent (CDP, Core Web Vitals) | Limited |
| **Debugging** | ✅ Deep integration | Basic |
| **Complexity** | ✅ Simple | 26 tools (proliferation) |
| **Best For** | 90% web dev, perf optimization | QA, cross-browser validation |

**When to use each**:
```
Chrome DevTools: Default choice
  ✓ Performance analysis (LCP, CLS, INP)
  ✓ Chrome/Edge debugging
  ✓ UI testing
  ✓ Network monitoring

Playwright: Only when necessary
  ✓ Cross-browser required (Firefox, Safari)
  ✓ CI/CD automation pipelines
  ✓ Visual regression across browsers
```

**Community Consensus (2025)**: "Use Chrome DevTools for normal development, Playwright only when cross-browser testing is necessary."

---

## Next.js 15

### Key Updates in 2025

- ✅ **Turbopack** is now the default bundler (stable, not experimental)
- ✅ **React 19** fully integrated (UI streaming, Server Components)
- ✅ **App Router** is the standard (Pages Router deprecated for new projects)
- ✅ **ISR** (Incremental Static Regeneration) for dynamic content

### Architectural Best Practices

```typescript
// ✅ App Router structure (2025 standard)
app/
├── layout.tsx          // Server Component (default)
├── page.tsx            // Server Component
├── loading.tsx         // Streaming UI
├── error.tsx           // Error boundaries
└── components/
    ├── ClientButton.tsx // 'use client' directive
    └── ServerData.tsx   // Server Component

// ✅ ISR pattern for dynamic content
export const revalidate = 3600; // Revalidate every hour

export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.id);
  return <ProductView product={product} />;
}

// ✅ State management: Keep close to usage
"use client";

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0); // Local state
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Anti-Patterns to Avoid

```typescript
// ❌ Giant utils.ts (>2000 lines)
// utils.ts - TOO BIG!
export const formatDate = ...
export const validateEmail = ...
// ... 2000 more lines

// ✅ Organized by domain
lib/
├── date-utils.ts
├── validation.ts
└── api-helpers.ts

// ❌ Deep nesting (>7 levels)
app/features/auth/components/forms/inputs/text/

// ✅ Flat structure
app/features/auth/
├── LoginForm.tsx
└── RegisterForm.tsx
```

### Performance Optimization

- ✅ **Dynamic imports** for code splitting
- ✅ **Image lazy loading** with Next.js `<Image>`
- ✅ **Automatic code splitting** (don't disable)
- ✅ **Use Server Components** by default

---

## FastAPI

### Core Principle: Async-First (2025)

**Performance**: FastAPI 17ms vs Flask 507ms (2025 benchmarks)

### Best Practices

```python
# ✅ Always use async for I/O operations
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()

# ✅ Async database connections
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("postgresql+asyncpg://...")

# ✅ Async dependencies (avoid thread pool overhead)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET_KEY)
    user = await db.get(User, payload["sub"])
    return user

# ✅ CPU-bound tasks → Celery workers
@app.post("/process")
async def process_data(data: dict):
    # Don't block event loop!
    task = process_heavy_computation.delay(data)
    return {"task_id": task.id}
```

### Anti-Patterns

```python
# ❌ Sync dependencies in async app (thread pool overhead)
def get_user_sync(db: Session = Depends(get_sync_db)):
    return db.query(User).all()

# ❌ Blocking calls in async endpoint
@app.get("/slow")
async def slow_endpoint():
    time.sleep(5)  # Blocks entire event loop!
    return {"status": "done"}

# ✅ Use async sleep or offload to worker
@app.get("/fast")
async def fast_endpoint():
    await asyncio.sleep(5)  # Non-blocking
    return {"status": "done"}
```

### Database Patterns

- ✅ **asyncpg** for PostgreSQL
- ✅ **databases** library for async query building
- ✅ **SQLAlchemy 2.0+** async mode
- ✅ **Alembic** for migrations

---

## Go Frameworks (Gin, Fiber, Echo)

### 2025 Recommendations

| Framework | Stars | RPS | Recommendation |
|-----------|-------|-----|----------------|
| **Gin** | 75K | 34K | ✅ **Default choice** (mature, ecosystem, learning curve) |
| **Fiber** | - | 36K | Fastest (Express.js-like), ⚠️ fasthttp incompatibility |
| **Echo** | 30K | 34K | Enterprise (type safety, structured) |

**Key Insight**: Real-world performance差は小さい (with DB + JSON processing)
→ Choose based on **ecosystem and team familiarity**, not raw benchmarks

### Gin Pattern (Recommended)

```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func main() {
    router := gin.Default()

    // Middleware
    router.Use(Logger(), Auth())

    // Routes
    router.GET("/users/:id", getUser)
    router.POST("/users", createUser)

    router.Run(":8080")
}

func getUser(c *gin.Context) {
    id := c.Param("id")
    user, err := db.GetUser(id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
        return
    }
    c.JSON(http.StatusOK, user)
}
```

### Framework Selection Guide

**Choose Gin if**:
- General web development
- Large ecosystem needed
- Team new to Go web frameworks

**Choose Fiber if**:
- Maximum performance critical
- Express.js familiarity preferred
- ⚠️ Aware of fasthttp incompatibility with standard net/http middleware

**Choose Echo if**:
- Enterprise environment
- Type safety priority
- Structured patterns preferred

---

## Flutter State Management

### 2025 Trend: Riverpod Dominates

| Solution | Adoption | Recommendation |
|----------|----------|----------------|
| **Riverpod** | 70% new apps | ✅ **Recommended** (compile-time safety, best performance) |
| **BLoC** | Enterprise | For large-scale, Clean Architecture projects |
| **Provider** | Legacy | Learning & small projects only |

### Riverpod Pattern (2025 Standard)

```dart
// ✅ Define provider
final userProvider = FutureProvider<User>((ref) async {
  final api = ref.watch(apiProvider);
  return await api.fetchUser();
});

// ✅ Use in widget
class UserWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider);

    return userAsync.when(
      data: (user) => Text(user.name),
      loading: () => CircularProgressIndicator(),
      error: (err, stack) => Text('Error: $err'),
    );
  }
}
```

### When to Use Each

**Riverpod**:
- ✅ New projects (default choice)
- ✅ Performance-critical apps
- ✅ Compile-time safety needed

**BLoC**:
- ✅ Large enterprise applications
- ✅ Clean Architecture patterns
- ✅ Structured event-driven approach

**Provider**:
- ✅ Small apps
- ✅ Learning Flutter
- ✅ Simple state needs

---

## Python ML/CV (PyTorch vs TensorFlow)

### 2025 Selection Guide

**No universal "better" framework** - choose based on use case

| Aspect | PyTorch | TensorFlow |
|--------|---------|------------|
| **Best For** | 🔬 Research, prototyping, NLP, Generative AI | 🏭 Production, scale, deployment |
| **Strengths** | Dynamic graph, Pythonic, Hugging Face | Static optimization, TF Serving/Lite/JS |
| **CV Research** | ✅ GANs, Vision Transformers | Production CV deployment |
| **Deployment** | Moderate | ✅ Excellent (cross-platform) |
| **Learning Curve** | Easier | Steeper |

### Use Case Examples

```python
# PyTorch: Research & Prototyping
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)

optimizer = torch.optim.Adam(model.parameters())

# TensorFlow: Production Deployment
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(10)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.save('model.h5')  # Easy deployment with TF Serving
```

### Recommendation

**PyTorch if**:
- Research project
- NLP / Generative AI focus
- Need fast experimentation
- Prefer Pythonic code

**TensorFlow if**:
- Production deployment critical
- Cross-platform (web, mobile, edge)
- Enterprise environment
- TensorBoard / TFX pipeline needed

**Ideal**: Learn both, choose per project

---

## iOS Swift (SwiftUI vs UIKit)

### 2025 Adoption Status

| Framework | New Apps | Existing Apps | Recommendation |
|-----------|----------|---------------|----------------|
| **SwiftUI** | 70% | 20% | ✅ Future standard |
| **UIKit** | 30% | 80% | Still essential knowledge |
| **Hybrid** | - | - | ✅ **Current best practice** |

### When to Use Each

**SwiftUI (Modern)**:
```swift
// ✅ New projects, multi-platform
struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

**UIKit (Legacy/Enterprise)**:
```swift
// ✅ iOS <13 support, complex customization
class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }
}
```

**Hybrid Approach (2025 Standard)**:
```swift
// ✅ Interoperability
import SwiftUI
import UIKit

// SwiftUI in UIKit
let swiftUIView = ContentView()
let hostingController = UIHostingController(rootView: swiftUIView)

// UIKit in SwiftUI
struct LegacyViewWrapper: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> LegacyViewController {
        return LegacyViewController()
    }
}
```

### Career Strategy (2025)

- ✅ **Learn both** - SwiftUI for future, UIKit still required
- ✅ Start new projects with SwiftUI
- ✅ Maintain UIKit skills for 80% of enterprise apps
- ✅ Use hybrid approach for migration

---

## React State Management (Vite)

### 2025 Trend: Zustand Rising

| Library | Recommendation | Use Case |
|---------|---------------|----------|
| **Zustand** | ✅ **Default choice** | Small to large apps, minimal boilerplate |
| **Redux** | Enterprise only | Complex middleware, time-travel debugging |
| **Context API** | Small apps | Simple state, no external lib |

### Zustand Pattern (2025 Standard)

```typescript
// ✅ Create store (no providers needed!)
import create from 'zustand'

const useStore = create((set) => ({
  count: 0,
  user: null,
  increment: () => set((state) => ({ count: state.count + 1 })),
  setUser: (user) => set({ user }),
}))

// ✅ Use in component (no wrapper!)
function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>{count}</button>
}

// ✅ Async actions
const useStore = create((set) => ({
  users: [],
  fetchUsers: async () => {
    const response = await fetch('/api/users')
    const users = await response.json()
    set({ users })
  },
}))
```

### Redux (When Needed)

```typescript
// Only use Redux for:
// - Large enterprise apps
// - Complex middleware (Redux Saga)
// - Time-travel debugging required
// - Team already experienced with Redux

import { configureStore, createSlice } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1 },
  },
})
```

### Progressive Adoption

```
Small app → Context API
Medium app → Zustand ← Default choice
Large enterprise → Redux (if needed)
```

**Key Advantage of Zustand**:
- ✅ No providers
- ✅ Minimal boilerplate
- ✅ Better performance (fine-grained updates)
- ✅ TypeScript support
- ✅ Smaller bundle size

---

## Activation Triggers Guide

### How to Make Subagents Activate Automatically

Each template should include an "Activation Triggers" section for proactive delegation.

**Template Pattern**:
```markdown
## Activation Triggers

**Auto-activate when user mentions:**
- Keywords: "keyword1", "keyword2", "キーワード"
- Tasks: "specific task type"
- Context: "framework-specific indicators"

**Proactive activation phrases:**
- "Task detected - using specialized expertise..."
- "Delegating to specialist for optimal results..."
```

### Framework-Specific Triggers

**Next.js**:
```
Keywords: "Next.js", "App Router", "Server Components", "ISR"
Tasks: "React server", "SSR", "static generation"
```

**FastAPI**:
```
Keywords: "FastAPI", "async", "Pydantic", "endpoint"
Tasks: "API development", "async programming", "REST API"
```

**Browser Testing**:
```
Chrome DevTools: "performance", "Core Web Vitals", "debug", "Chrome"
Playwright: "cross-browser", "Firefox", "Safari", "CI/CD"
```

---

## Summary: Key Takeaways

1. **Browser**: Chrome DevTools default, Playwright for cross-browser
2. **Next.js**: App Router + Turbopack + ISR standard
3. **FastAPI**: Async-first, use asyncpg/databases
4. **Go**: Gin recommended (ecosystem), Fiber if performance critical
5. **Flutter**: Riverpod standard, BLoC for enterprise
6. **Python ML**: PyTorch (research), TensorFlow (production)
7. **iOS**: Hybrid SwiftUI + UIKit approach
8. **React State**: Zustand default, Redux only if needed

---

**Last Updated**: 2025-10-20
**Next Review**: When major framework updates released or new patterns emerge
