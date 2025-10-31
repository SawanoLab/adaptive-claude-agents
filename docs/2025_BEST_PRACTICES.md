# 2025 Framework Best Practices & Recommendations

**Last Updated**: 2025-10-20
**Purpose**: Framework-specific best practices and recommended tools for 2025

This document provides up-to-date guidance on modern development patterns, tool selection, and architectural decisions for each supported framework.

---

## Table of Contents

- [Token Optimization for Subagents](#token-optimization-for-subagents-2025)
- [Model Selection (Haiku 4.5 vs Sonnet 4.5)](#model-selection-haiku-45-vs-sonnet-45)
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

## Token Optimization for Subagents (2025)

**Last Updated**: 2025-10-31
**Source**: [Anthropic Best Practices](https://docs.claude.com/en/docs/claude-code), Community Research (2025)

### 🎯 Core Strategies

| Strategy | Token Reduction | Implementation Difficulty | Priority |
|----------|-----------------|---------------------------|----------|
| **Markdown Shared Memory** | 50-60% | Easy | 🔴 High |
| **Context Compression** | 60-80% | Medium | 🔴 High |
| **Just-in-Time Loading** | 40-50% | Medium | 🟡 Medium |
| **Token-Efficient Tools Beta** | 10-20% | Easy (API header) | 🟢 Low |
| **Parallel Processing Limits** | Variable | Easy (guidelines) | 🔴 High |

### Expected Overall Savings

**Baseline (no optimization)**: 100,000 tokens/session
**After full optimization**: 30,000-50,000 tokens/session
**Total savings**: **50-70% reduction**

### 1. Markdown Shared Memory Pattern

**Principle**: Subagents save detailed reports to `.claude/reports/`, returning only summaries to the main agent.

**Before** (wasteful):
```text
Subagent returns 10,000 token detailed report
→ Main agent context grows by 10,000 tokens
→ Every subsequent message costs more
```

**After** (efficient):
```text
Subagent saves report to .claude/reports/analysis-20251031.md
Subagent returns 200 token summary
→ Main agent context grows by only 200 tokens
→ 98% token reduction on report transmission
```

**Implementation**:

```markdown
## Subagent Output Format (REQUIRED)

### Summary (3-5 lines)
- Key finding 1
- Key finding 2
- Key finding 3

### Details
Saved to: `.claude/reports/[task-name]-YYYYMMDD-HHMMSS.md`

### Recommendations
1. [Action item 1]
2. [Action item 2]
```

### 2. Context Compression

**Principle**: Only pass essential context to subagents. Use file paths and identifiers instead of full file contents.

**Bad Example**:
```python
# Passing 50,000 tokens of context
context = {
    "files": [
        {"path": "api/users.py", "content": "... 5000 lines ..."},
        {"path": "api/auth.py", "content": "... 3000 lines ..."},
        # ... 10 more files
    ]
}
subagent.execute(context)  # 50,000 tokens
```

**Good Example**:
```python
# Passing only 500 tokens of context
context = {
    "task": "Review authentication logic",
    "files": ["api/users.py", "api/auth.py"],  # Paths only
    "focus_areas": ["login", "token_refresh"]
}
subagent.execute(context)  # 500 tokens
# Subagent reads files internally as needed
```

**Savings**: 99% reduction in context transfer

### 3. Just-in-Time Context Loading

**Principle**: Load context progressively, not upfront.

**Three-Tier Loading Strategy**:

```text
Tier 1: Overview (500 tokens)
  - Use mcp__serena__get_symbols_overview
  - Get file structure without content

Tier 2: Targeted (2,000 tokens)
  - Use mcp__serena__find_symbol
  - Load specific functions/classes

Tier 3: Full Read (5,000+ tokens)
  - Use Read tool as last resort
  - Only for small files (<200 lines)
```

**Example Workflow**:

```python
# Step 1: Get overview (500 tokens)
overview = mcp__serena__get_symbols_overview("large_file.py")

# Step 2: Identify target (based on overview)
if "process_payment" in [s.name for s in overview.symbols]:
    # Step 3: Load only target (1,500 tokens)
    symbol = mcp__serena__find_symbol(
        "process_payment",
        "large_file.py",
        include_body=True
    )

# Avoided reading 10,000 token file
# Savings: 8,000 tokens (80%)
```

### 4. Token-Efficient Tools Beta

**New Feature** (February 2025): Anthropic's official token reduction API

**Usage**:
```python
headers = {
    "anthropic-beta": "token-efficient-tools-2025-02-19"
}

response = anthropic.messages.create(
    model="claude-sonnet-4-5",
    headers=headers,  # Enable token efficiency
    messages=[...]
)
```

**Effect**: Automatic 10-20% reduction in tool use tokens

### 5. Parallel Processing Cost Management

**Warning**: Claude Code can automatically spawn 5+ parallel subagents, rapidly consuming tokens.

**Guidelines**:

```yaml
✅ Approved Parallel Processing:
  - 2-3 independent tasks
  - Total estimated tokens: <60,000
  - Time savings: >30 minutes
  - Example: "Run tests" + "Generate docs"

❌ Prohibited Parallel Processing:
  - 5+ simultaneous subagents
  - No token budget estimate
  - Simple tasks with excessive parallelization
  - Example: "Check 10 files" → 10 parallel subagents (wasteful)
```

**Monitoring**:

```bash
# Log token estimates before spawning subagents
echo "Spawning 3 subagents, estimated total: 45,000 tokens"
# Proceed only if within budget
```

### 6. Dynamic Context Allocation

**Principle**: Allocate context size based on task complexity

**Examples**:

```text
Simple task: "Fix typo in README.md"
→ Allocate 5,000 tokens
→ Use Haiku 4.5

Medium task: "Review API authentication"
→ Allocate 20,000 tokens
→ Use Sonnet 4.5

Complex task: "Refactor entire auth system"
→ Allocate 100,000 tokens
→ Use Sonnet 4.5 + multiple subagents
```

### Implementation Priority

#### Phase 1: Immediate (Easy + High Impact)

1. **Markdown Shared Memory** → 50-60% savings
2. **Parallel Processing Limits** → Prevent token spikes
3. **Token-Efficient Tools Beta** → 10-20% savings (API header only)

**Expected Phase 1 savings**: 20-30% reduction

#### Phase 2: Short-term (Medium Difficulty + High Impact)

1. **Context Compression** → 60-80% savings per delegation
2. **Just-in-Time Loading** → 40-50% savings
3. **Dynamic Context Allocation** → 20-30% savings

**Expected Phase 2 savings**: Additional 30-40% reduction

#### Phase 3: Ongoing (Monitoring & Refinement)

1. Token usage analytics
2. Adjust thresholds based on metrics
3. Template optimization based on data

**Expected Phase 3 savings**: Additional 10-20% reduction

### Real-World Example

**Before Optimization**:
```text
User: "Review all API endpoints and generate test coverage report"

Main Agent:
  - Reads 15 API files (30,000 tokens)
  - Spawns 5 parallel review subagents
  - Each subagent receives full context (30,000 tokens)
  - Each returns 5,000 token report

Total: 30,000 + (5 × 30,000) + (5 × 5,000) = 205,000 tokens
Cost: ~$0.80 (Sonnet 4.5)
```

**After Optimization**:
```text
User: "Review all API endpoints and generate test coverage report"

Main Agent:
  - Passes file paths only (500 tokens)
  - Spawns 1 review subagent (sequential processing)
  - Subagent loads files progressively (10,000 tokens)
  - Subagent saves report to .claude/reports/api-review.md
  - Returns 200 token summary

Total: 500 + 10,000 + 200 = 10,700 tokens
Cost: ~$0.05 (Sonnet 4.5)
Savings: 95% ($0.75 saved)
```

### Monitoring & Metrics

**Key Metrics to Track**:

```yaml
Token Usage:
  - Tokens per session
  - Tokens per subagent spawn
  - Context size growth rate

Efficiency:
  - Tasks completed per 10k tokens
  - Average subagent report size
  - Parallel spawn frequency

Cost:
  - Daily/weekly token spend
  - Cost per task type
  - Savings vs baseline
```

**Target Metrics** (after full optimization):

```yaml
Tokens per session: <50,000 (down from 100,000)
Subagent reports: <500 tokens (down from 5,000)
Parallel spawns: <3 simultaneous (down from 5+)
Monthly cost reduction: 50-70%
```

### Resources

- [Anthropic Token-Efficient Tool Use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/token-efficient-tool-use)
- [Claude Code Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Community: Token Optimization Patterns (2025)](https://medium.com/@sampan090611/experiences-on-claude-codes-subagent-and-little-tips-for-using-claude-code-c4759cd375a7)

---

## Model Selection (Haiku 4.5 vs Sonnet 4.5)

**Since**: Claude Code v2.0.17 (October 2025)
**Recommendation**: Use **Haiku 4.5** for simple tasks to reduce costs by 60-80%

### Model Comparison

| Aspect | Haiku 4.5 | Sonnet 4.5 |
|--------|-----------|------------|
| **Cost** | ✅ 3-5x cheaper | 💰 Higher cost |
| **Speed** | ✅ 2-3x faster | Moderate |
| **Best For** | Simple edits, tests, verification | Complex reasoning, planning |
| **Context** | 200K tokens | 200K tokens |
| **Quality** | High for straightforward tasks | Highest for all tasks |

### When to Use Each Model

#### ✅ Use Haiku 4.5 (60-80% cost savings)

**1. Single File Simple Edits**
```
User: "file1.jsのtypoを修正して"
→ Haiku 4.5: 定型作業、コスト最小
```

**2. Test Execution & Validation**
```
User: "テストを実行して結果を報告"
→ Haiku 4.5: 検証作業、推論不要
```

**3. Code Formatting & Linting**
```
User: "このファイルをPrettierでフォーマット"
→ Haiku 4.5: 機械的な作業
```

**4. Documentation Updates (Simple)**
```
User: "README.mdのバージョン番号を1.2.0に更新"
→ Haiku 4.5: 単純な置換作業
```

**5. Git Operations**
```
User: "変更をコミットして"
→ Haiku 4.5: 定型コマンド実行
```

#### 🎯 Use Sonnet 4.5 (高精度が必要)

**1. Architecture Design & Planning**
```
User: "認証システムの設計を考えて"
→ Sonnet 4.5: 複雑な推論が必要
```

**2. Debugging Complex Issues**
```
User: "このメモリリークの原因を調査"
→ Sonnet 4.5: 深い分析が必要
```

**3. Multi-File Refactoring**
```
User: "5つのファイルでAPI仕様を変更"
→ Sonnet 4.5: 依存関係の理解が必要
```

**4. Code Review**
```
User: "このPRをレビューして"
→ Sonnet 4.5: セキュリティ・パフォーマンスの判断
```

**5. Codebase Exploration**
```
User: "この関数がどこで使われているか調査"
→ Sonnet 4.5: コンテキスト理解が重要
```

### Cost-Benefit Analysis

| Task Type | Haiku Cost | Sonnet Cost | Savings | Quality Trade-off |
|-----------|-----------|-------------|---------|-------------------|
| Typo fix (1 file) | $0.001 | $0.005 | **80%** | ✅ None |
| Test execution | $0.002 | $0.010 | **80%** | ✅ None |
| Git commit | $0.001 | $0.003 | **67%** | ✅ None |
| Simple docs update | $0.001 | $0.004 | **75%** | ✅ None |
| Code review | $0.015 | $0.020 | 25% | ⚠️ Lower thoroughness |
| Architecture design | $0.030 | $0.040 | 25% | ❌ Significant |

**推奨コスト配分**:
- Haiku 4.5: 単純タスクの60-70% → **コスト削減60-80%**
- Sonnet 4.5: 複雑タスクの30-40% → **品質維持**

### How to Select Model in Claude Code

**Auto Mode (推奨)**:
```bash
# SonnetPlanモードを使用（デフォルト）
# Plan時はSonnet、実行時は自動でHaikuに切り替わる
claude --model sonnet-plan
```

**Manual Selection**:
```bash
# Haikuを明示的に指定（単純タスク向け）
claude --model haiku

# Sonnetを明示的に指定（複雑タスク向け）
claude --model sonnet
```

**Interactive Mode**:
```
> /model haiku    # Switch to Haiku 4.5
> /model sonnet   # Switch to Sonnet 4.5
```

### Practical Guidelines

**Rule of Thumb**:
1. **タスクが5分未満で説明できる** → Haiku 4.5
2. **複数の判断が必要** → Sonnet 4.5
3. **不確実な場合** → Sonnet 4.5から開始（安全側）

**Team Policy Example**:
```yaml
# .claude/settings.json
{
  "defaultModel": "sonnet-plan",  # Auto-switching enabled
  "simpleTasksModel": "haiku",
  "complexTasksModel": "sonnet",
  "costOptimization": true
}
```

**Expected Monthly Savings** (for typical developer):
- **Before**: $150/month (Sonnet only)
- **After**: $60-80/month (60% Haiku, 40% Sonnet)
- **Savings**: **$70-90/month** (47-60%)

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
