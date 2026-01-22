# Git Diff Code Refiner

Reviews all changed files in a git diff range and applies refinement principles.

## Usage

```
Review commits: git diff main...HEAD
Review last commit: git diff HEAD~1
Review specific range: git diff abc123..def456
```

## Process

1. Run the specified `git diff` command
2. For each changed file in the diff, read and review it
3. Apply all principles below
4. Report issues found with file:line references

## Principles

### 1. No Redundant Comments

Remove comments that repeat what code already says.

**Bad:**
```python
# Mark all tests as security tests
pytestmark = pytest.mark.security

# Initialize the counter to zero
counter = 0

# Loop through all items
for item in items:
```

**Good:**
```python
pytestmark = pytest.mark.security

counter = 0

for item in items:
```
