---
name: test-generator
description: Generate comprehensive tests for code changes using multi-agent analysis
---

# /test-generator - Test Generation Engine

> Generate comprehensive tests for code changes with multi-agent analysis covering happy paths, boundaries, edge cases, and error handling.

---

## Usage

```
/test-generator                                     # Tests for uncommitted changes
/test-generator --scope <file|diff|commit>          # Specific scope
/test-generator --depth <quick|standard|thorough>   # Coverage depth
/test-generator --file <path>                       # Target specific file
```

---

## Examples

```
/test-generator
# Generates tests for all uncommitted changes

/test-generator --scope diff
# Tests for staged changes only

/test-generator --file src/utils/calculator.ts
# Tests for specific file

/test-generator --depth thorough
# Maximum coverage with all edge cases
```

---

## Depth Levels

| Level | Analysts | Scenarios | Description |
|-------|----------|-----------|-------------|
| `quick` | Happy Path only | 3-5 | Fast validation, core functionality |
| `standard` | Happy + Adversarial | 8-15 | Balanced coverage for most code (DEFAULT) |
| `thorough` | All 3 Analysts | 20-40 | Comprehensive testing, all categories |

---

## What Happens

### Phase 1: Code Discovery
- Identify target code from git diff, file, or commit
- Extract function signatures, parameters, return types
- Map dependencies and external calls

### Phase 2: Context Analysis
- Detect testing framework (Jest, Vitest, pytest, etc.)
- Read existing test patterns in codebase
- Identify mocking requirements

### Phase 3: Multi-Agent Analysis (Parallel)
Three analysts with different perspectives:
- **Happy Path Analyst**: Normal flows, typical inputs, expected outputs
- **Adversarial Analyst**: Boundaries, edge cases, null/empty, type errors
- **Integration Analyst**: Component interactions, data flow, API contracts

### Phase 4: Scenario Consolidation
- Merge scenarios from all analysts
- Remove duplicates
- Prioritize by risk and coverage value

### GATE 1: User Approval
- Present consolidated test scenarios
- Wait for user approval before generating tests
- Allow user to add/remove/modify scenarios

### Phase 5: Test Generation
- Generate tests following AAA pattern
- Apply detected framework conventions
- Use proper naming conventions

### Phase 6: Validation
- Verify test structure and assertions
- Check for anti-patterns
- Ensure test isolation

### GATE 2: User Approval
- Present generated tests
- Wait for user approval before writing files

---

## Test Categories Generated

| Category | Description | Example |
|----------|-------------|---------|
| Happy Path | Normal expected flow | Valid user login succeeds |
| Boundary Min | At minimum value | `age = 0` is valid |
| Boundary Max | At maximum value | `age = 150` is valid |
| Boundary Off-by-one | Just outside bounds | `age = -1` throws |
| Edge: Empty | Empty inputs | Empty string returns default |
| Edge: Null | Null/undefined | `null` throws ArgumentError |
| Edge: Single | Single element | Array with 1 item works |
| Error: Type | Wrong type | String instead of number |
| Error: Missing | Missing required | Omit required field |
| State: Invalid | Invalid transition | Start on completed task |

---

## Framework Auto-Detection

| Language | Detection | Frameworks |
|----------|-----------|------------|
| TypeScript/JS | package.json | Jest, Vitest, Mocha, Node Test Runner |
| Python | pyproject.toml, setup.py | pytest, unittest |
| Go | go.mod | testing, testify |
| Java | pom.xml, build.gradle | JUnit 5, TestNG |
| Rust | Cargo.toml | built-in `#[test]` |
| Ruby | Gemfile | RSpec, Minitest |
| C# | *.csproj | xUnit, NUnit, MSTest |

---

## Output Format

### Scenario Report (Gate 1)

```markdown
# Test Scenarios for: [function/file name]

## Summary
- Total scenarios: 15
- Happy path: 3
- Boundary: 4
- Edge cases: 5
- Error handling: 3

## Scenarios by Category

### Happy Path
1. `functionName_withValidInput_returnsExpectedResult`
   - Input: typical valid values
   - Expected: normal success response

### Boundary Values
2. `functionName_withMinValue_handlesMinimum`
   - Input: minimum valid value (0)
   - Expected: processes correctly

[...]

## Proceed with test generation? [Y/n]
```

### Generated Tests (Gate 2)

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

## Naming Convention

Tests follow: `MethodName_Scenario_ExpectedBehavior`

Examples:
- `login_withValidCredentials_returnsAuthToken`
- `calculateTotal_withEmptyCart_returnsZero`
- `processOrder_withInvalidPayment_throwsPaymentError`

---

## Begin

To start test generation, read `ai/toolkits/testing/CLAUDE.md` and follow the Test Generation Engine protocol.
