# Testing Standards

> The quality principles and standards that govern all Test Generation Engine activities.

---

## Core Principles

### 1. AAA Pattern is Mandatory

Every test MUST follow Arrange-Act-Assert:

```typescript
it('functionName_scenario_expectedBehavior', () => {
  // Arrange - Setup test data and dependencies
  const input = createTestInput();
  const mockService = createMock();

  // Act - Execute the function under test
  const result = functionUnderTest(input);

  // Assert - Verify the outcome
  expect(result).toBe(expectedValue);
});
```

**Why**: Clear separation makes tests readable, maintainable, and debuggable.

---

### 2. Single Responsibility

Each test should verify ONE behavior and have ONE reason to fail.

**Good**:
```typescript
it('calculateDiscount_withValidPercent_appliesDiscount', () => {
  expect(calculateDiscount(100, 20)).toBe(80);
});

it('calculateDiscount_withZeroPercent_returnsOriginalPrice', () => {
  expect(calculateDiscount(100, 0)).toBe(100);
});
```

**Bad**:
```typescript
it('calculateDiscount_works', () => {
  expect(calculateDiscount(100, 20)).toBe(80);
  expect(calculateDiscount(100, 0)).toBe(100);  // Second assertion
  expect(calculateDiscount(100, 100)).toBe(0);  // Third assertion
});
```

---

### 3. Test Isolation

Tests must be independent:
- No shared mutable state between tests
- No test order dependencies
- Each test sets up its own fixtures
- Each test cleans up after itself

**Good**:
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockRepository;

  beforeEach(() => {
    mockRepo = createMockRepository();
    service = new UserService(mockRepo);
  });

  it('test1', () => { /* isolated */ });
  it('test2', () => { /* isolated */ });
});
```

**Bad**:
```typescript
let sharedUser: User; // Shared state!

it('creates user', () => {
  sharedUser = createUser();
  expect(sharedUser.id).toBeDefined();
});

it('updates user', () => {
  // Depends on previous test!
  updateUser(sharedUser);
});
```

---

### 4. Descriptive Naming

Test names should describe: **What** + **Condition** + **Expected Outcome**

Format: `methodName_scenario_expectedBehavior`

**Good**:
- `login_withValidCredentials_returnsAuthToken`
- `calculateTotal_withEmptyCart_returnsZero`
- `processPayment_whenCardDeclined_throwsPaymentError`

**Bad**:
- `test1`
- `loginTest`
- `it_works`
- `should_work_correctly`

---

### 5. Test Realistic Scenarios

Use realistic test data that reflects production usage:

**Good**:
```typescript
const validUser = {
  name: 'Jane Smith',
  email: 'jane.smith@company.com',
  age: 32
};
```

**Bad**:
```typescript
const testUser = {
  name: 'test',
  email: 'test@test.com',
  age: 123
};
```

---

## Quality Standards

### For Test Structure

| Aspect | Standard |
|--------|----------|
| Assertions per test | 1 (rarely 2-3 related) |
| Setup lines | < 10 (extract helpers if more) |
| Test file size | < 500 lines (split if larger) |
| Describe nesting | Max 3 levels |

### For Test Coverage

| Category | Required Coverage |
|----------|-------------------|
| Happy paths | 100% of main flows |
| Boundaries | All numeric limits |
| Error paths | All thrown exceptions |
| Edge cases | null, empty, single element |

### For Assertions

**Strong Assertions**:
```typescript
expect(result).toBe(42);                    // Exact equality
expect(result).toEqual({ id: 1, name: 'Test' }); // Deep equality
expect(() => fn()).toThrow(SpecificError);  // Specific error type
```

**Weak Assertions** (avoid):
```typescript
expect(result).toBeTruthy();    // Too vague
expect(result).toBeDefined();   // Doesn't verify value
expect(errors.length).toBeGreaterThan(0); // Doesn't verify content
```

---

## Anti-Patterns

### 1. The Giant Test

**Problem**: Tests that verify multiple unrelated behaviors.

```typescript
// BAD
it('user_flow', () => {
  const user = createUser();
  expect(user.id).toBeDefined();

  updateUser(user, { name: 'New Name' });
  expect(user.name).toBe('New Name');

  deleteUser(user);
  expect(getUser(user.id)).toBeNull();
});
```

**Solution**: Split into focused tests.

---

### 2. The Leaky Test

**Problem**: Tests that depend on external state or other tests.

```typescript
// BAD - depends on database state from other tests
it('gets_all_users', () => {
  const users = getAllUsers();
  expect(users.length).toBe(5); // Magic number from other tests
});
```

**Solution**: Each test creates its own test data.

---

### 3. The Mockery

**Problem**: Over-mocking that tests implementation, not behavior.

```typescript
// BAD - tests internal implementation
it('saves_user', () => {
  service.saveUser(user);
  expect(mockRepo.beginTransaction).toHaveBeenCalled();
  expect(mockRepo.insert).toHaveBeenCalledWith('users', user);
  expect(mockRepo.commit).toHaveBeenCalled();
});
```

**Solution**: Test observable behavior.

```typescript
// GOOD - tests behavior
it('saveUser_withValidData_userIsPersisted', () => {
  service.saveUser(user);
  expect(service.getUser(user.id)).toEqual(user);
});
```

---

### 4. The Time Bomb

**Problem**: Tests that use real time and become flaky.

```typescript
// BAD
it('expires_after_one_hour', async () => {
  const token = createToken();
  await sleep(3600000); // Wait 1 hour!
  expect(token.isExpired()).toBe(true);
});
```

**Solution**: Mock time or use dependency injection.

```typescript
// GOOD
it('isExpired_afterOneHour_returnsTrue', () => {
  const mockClock = createMockClock('2024-01-01T12:00:00Z');
  const token = createToken({ clock: mockClock });

  mockClock.advance({ hours: 1, seconds: 1 });

  expect(token.isExpired()).toBe(true);
});
```

---

### 5. The Flaky Test

**Problem**: Tests that sometimes pass, sometimes fail.

Common causes:
- Race conditions
- Reliance on real time
- Shared state
- Network calls
- Random data without seeding

**Solution**:
- Use deterministic inputs
- Mock external dependencies
- Avoid shared state
- Seed random generators

---

### 6. The Logic Duplicator

**Problem**: Duplicating production logic in tests.

```typescript
// BAD - reimplements the logic
it('calculates_total', () => {
  const items = [{ price: 10, qty: 2 }, { price: 5, qty: 3 }];
  const expected = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  expect(calculateTotal(items)).toBe(expected);
});
```

**Solution**: Use hard-coded expected values.

```typescript
// GOOD
it('calculateTotal_withMultipleItems_sumsCorrectly', () => {
  const items = [{ price: 10, qty: 2 }, { price: 5, qty: 3 }];
  expect(calculateTotal(items)).toBe(35);
});
```

---

### 7. The Comment Explainer

**Problem**: Tests that need comments to explain what they test.

```typescript
// BAD
it('test_case_1', () => {
  // This tests that when a user has no orders,
  // the loyalty points should be zero
  const user = createUser();
  expect(user.loyaltyPoints).toBe(0);
});
```

**Solution**: Self-documenting test names.

```typescript
// GOOD
it('newUser_withNoOrders_hasZeroLoyaltyPoints', () => {
  const user = createUser();
  expect(user.loyaltyPoints).toBe(0);
});
```

---

## Test Organization

### File Structure

```
src/
  services/
    user-service.ts
    order-service.ts
tests/
  services/
    user-service.test.ts
    order-service.test.ts
  integration/
    user-order-flow.test.ts
  fixtures/
    users.ts
    orders.ts
```

### Describe Block Structure

```typescript
describe('ClassName/ModuleName', () => {
  // Shared setup
  beforeEach(() => { /* setup */ });
  afterEach(() => { /* cleanup */ });

  describe('methodName', () => {
    describe('when condition', () => {
      it('methodName_condition_expectedResult', () => {
        // test
      });
    });

    describe('edge cases', () => {
      it('methodName_withNull_throwsError', () => {
        // test
      });
    });
  });
});
```

---

## Quality Gates

### Before Marking Tests Complete

- [ ] All tests follow AAA pattern
- [ ] Each test has single responsibility
- [ ] Test names are descriptive (method_scenario_expected)
- [ ] No shared mutable state
- [ ] No test order dependencies
- [ ] Realistic test data
- [ ] Strong assertions (not just truthy/defined)
- [ ] Edge cases covered (null, empty, boundaries)

### Before Generating Tests

- [ ] Framework correctly detected
- [ ] Existing test patterns analyzed
- [ ] Mock requirements identified
- [ ] Test scenarios approved by user

---

## Framework-Specific Patterns

### Jest/Vitest (JavaScript/TypeScript)
```typescript
describe('Module', () => {
  it('method_scenario_expected', () => {
    expect(result).toBe(expected);
  });
});
```

### pytest (Python)
```python
def test_method_scenario_expected():
    # Arrange
    input = create_input()

    # Act
    result = function_under_test(input)

    # Assert
    assert result == expected
```

### Go testing
```go
func TestMethodName_Scenario_Expected(t *testing.T) {
    // Arrange
    input := createInput()

    // Act
    result := FunctionUnderTest(input)

    // Assert
    if result != expected {
        t.Errorf("got %v, want %v", result, expected)
    }
}
```

### JUnit 5 (Java)
```java
@Test
@DisplayName("methodName with scenario returns expected")
void methodName_scenario_expected() {
    // Arrange
    var input = createInput();

    // Act
    var result = functionUnderTest(input);

    // Assert
    assertEquals(expected, result);
}
```

---

## Test Pyramid Guidance

```
         /\
        /  \     E2E Tests (10%)
       /----\    - Critical user flows only
      /      \   - Expensive to run
     /--------\  Integration Tests (20%)
    /          \ - Component boundaries
   /------------\- API contracts
  /              \Unit Tests (70%)
 /----------------\- Fast, isolated
/                  \- Cover all paths
```

### When to Use Each

| Test Type | Use When |
|-----------|----------|
| Unit | Pure functions, calculations, transformations |
| Integration | Component interactions, database ops, API calls |
| E2E | Critical user journeys, smoke tests |

---

## Metrics

### Healthy Test Suite

| Metric | Target |
|--------|--------|
| Test execution time | < 30s for unit tests |
| Flaky test rate | < 1% |
| Code coverage | > 80% (not a goal in itself) |
| Mutation score | > 70% |
| Tests per function | 3-10 depending on complexity |
