# Test Generation Engine

> A comprehensive test generation toolkit for Claude Code that uses multi-agent analysis to produce high-quality tests covering happy paths, boundaries, edge cases, and error handling.

---

## What Makes This Different

| Traditional Test Generation | Test Generation Engine |
|-----------------------------|------------------------|
| Single perspective | 3 specialized analysts with different focuses |
| Happy paths only | Comprehensive: happy, boundary, edge, error, integration |
| Generate immediately | User approval gates before generation |
| Generic patterns | Detects and matches existing project conventions |
| No quality checks | Built-in validation against anti-patterns |

---

## Quick Start

### Basic Usage
```
/test-generator
```
Generates tests for all uncommitted changes.

### With Options
```
/test-generator --file src/utils/calculator.ts
/test-generator --depth thorough
/test-generator --scope diff
```

### Depth Levels

| Level | Analysts | Scenarios | Use Case |
|-------|----------|-----------|----------|
| `quick` | Happy Path only | 3-5 | Fast validation |
| `standard` | Happy + Adversarial | 8-15 | Most code (DEFAULT) |
| `thorough` | All 3 | 20-40 | Critical code, comprehensive |

---

## The Multi-Agent Architecture

```
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    │ (You - Claude)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  HAPPY PATH   │   │  ADVERSARIAL  │   │  INTEGRATION  │
│   ANALYST     │   │    ANALYST    │   │    ANALYST    │
└───────────────┘   └───────────────┘   └───────────────┘
     Normal             Boundaries           Component
     flows              Edge cases           interactions
     Success            Errors               Mocking
```

### Agent Roles

- **Orchestrator (You)**: Coordinates phases, consolidates findings, manages gates
- **Happy Path Analyst**: Normal flows, typical inputs, expected outputs
- **Adversarial Analyst**: Boundaries, null/empty, type errors, failure paths
- **Integration Analyst**: Component boundaries, mocks, API contracts

---

## The 6-Phase Process

1. **Code Discovery** - Identify target code from git/files
2. **Context Analysis** - Detect framework, read existing patterns
3. **Multi-Agent Analysis** - Parallel analysis from 3 perspectives
4. **Scenario Consolidation** - Merge, dedupe, prioritize

**GATE 1: User approval of scenarios**

5. **Test Generation** - Generate tests following AAA pattern
6. **Validation** - Verify quality, check for anti-patterns

**GATE 2: User approval of generated tests**

---

## Test Categories Generated

| Category | Description | Example |
|----------|-------------|---------|
| Happy Path | Normal expected flow | Valid login succeeds |
| Boundary Min | At minimum value | `age = 0` valid |
| Boundary Max | At maximum value | `age = 150` valid |
| Boundary Off-by-one | Just outside bounds | `age = -1` throws |
| Edge: Empty | Empty inputs | `[]` returns default |
| Edge: Null | Null/undefined | `null` throws |
| Edge: Single | Single element | Array of 1 works |
| Error: Type | Wrong type | String for number |
| Error: Missing | Missing required | Omit field |
| State: Invalid | Bad transition | Skip state |
| Integration: Success | Dep succeeds | Mock returns value |
| Integration: Failure | Dep fails | Mock throws |

---

## Framework Detection

| Language | Config File | Frameworks Supported |
|----------|-------------|---------------------|
| TypeScript/JS | package.json | Jest, Vitest, Mocha, Node Test |
| Python | pyproject.toml | pytest, unittest |
| Go | go.mod | testing, testify |
| Java | pom.xml | JUnit 5, TestNG |
| Rust | Cargo.toml | built-in `#[test]` |
| Ruby | Gemfile | RSpec, Minitest |
| C# | *.csproj | xUnit, NUnit |

---

## Sample Output

```typescript
describe('calculateDiscount', () => {
  // HAPPY PATH
  describe('when called with valid inputs', () => {
    it('calculateDiscount_withValidPercentage_appliesDiscount', () => {
      // Arrange
      const price = 100;
      const discount = 20;

      // Act
      const result = calculateDiscount(price, discount);

      // Assert
      expect(result).toBe(80);
    });
  });

  // BOUNDARY VALUES
  describe('boundary conditions', () => {
    it('calculateDiscount_withZeroDiscount_returnsOriginalPrice', () => {
      // Arrange
      const price = 100;
      const discount = 0;

      // Act
      const result = calculateDiscount(price, discount);

      // Assert
      expect(result).toBe(100);
    });

    it('calculateDiscount_withNegativeDiscount_throwsRangeError', () => {
      // Arrange & Act & Assert
      expect(() => calculateDiscount(100, -1)).toThrow(RangeError);
    });
  });

  // EDGE CASES
  describe('edge cases', () => {
    it('calculateDiscount_withNullPrice_throwsArgumentError', () => {
      // Arrange & Act & Assert
      expect(() => calculateDiscount(null, 20)).toThrow(ArgumentError);
    });
  });
});
```

---

## Directory Structure

```
testing/
├── CLAUDE.md              # System instructions (read this first)
├── README.md              # This file
├── commands/
│   └── test-generator.md  # /test-generator command entry point
├── agents/
│   ├── happy-path-analyst.md    # Normal flow scenarios
│   ├── adversarial-analyst.md   # Edge cases, boundaries, errors
│   └── integration-analyst.md   # Component interactions
└── philosophy/
    └── testing-standards.md     # Quality mandates, anti-patterns
```

---

## Quality Standards

### Mandatory Patterns

- **AAA Pattern**: Arrange → Act → Assert in every test
- **Single Responsibility**: One test = one behavior
- **Isolation**: No shared state between tests
- **Descriptive Names**: `method_scenario_expectedBehavior`

### Anti-Patterns Avoided

- Giant tests (multiple assertions testing different things)
- Leaky tests (shared mutable state)
- Flaky tests (time-dependent, random)
- Logic duplication (reimplementing production code)
- Weak assertions (toBeTruthy, toBeDefined)

---

## Usage Tips

1. **Start with `standard` depth** - Good balance of coverage and test count
2. **Use `thorough` for critical code** - Payment processing, auth, data mutations
3. **Review scenarios at Gate 1** - Remove redundant, add missing
4. **Check generated mocks** - Ensure they match your service interfaces
5. **Run generated tests** - Verify they pass before committing

---

## Usage in Any Project

To use the Test Generation Engine in any repository:

1. Copy the `ai/toolkits/testing/` directory to your project
2. Ensure Claude Code can read the files
3. Invoke with `/test-generator`

Or reference directly:
```
Read ai/toolkits/testing/CLAUDE.md and follow those instructions to generate tests for: [target]
```

---

## Comparison

| Feature | GitHub Copilot | Traditional TDD | Test Generation Engine |
|---------|----------------|-----------------|----------------------|
| Multi-perspective | No | No | Yes (3 analysts) |
| Boundary analysis | Limited | Manual | Systematic |
| User approval gates | No | N/A | Yes (2 gates) |
| Anti-pattern checking | No | Manual | Automated |
| Framework detection | Basic | N/A | Comprehensive |
| Existing pattern matching | Limited | N/A | Yes |

---

## License

Part of the dev-toolbox AI collection. Use freely.
