[ENHANCEMENT] Add Type Hints to Utility Functions

## Feature Description
Add Python type hints to utility functions to improve code readability and enable better IDE support and static type checking.

## Problem Statement
Several utility functions in the project lack type hints, making it harder for new contributors to understand expected inputs and outputs. Adding type hints will improve code documentation and catch potential type-related bugs early.

## Proposed Solution
Add appropriate type hints to functions in the utils directory, focusing on:
1. Function parameters
2. Return types
3. Complex data structures
4. Generic types where appropriate

## Technical Details
Example of adding type hints:

Before:
```python
def get_cached_data(key, default=None):
    if key in cache:
        return cache[key]
    return default

def calculate_success_rate(solved, total):
    if total == 0:
        return 0
    return (solved / total) * 100
```

After:
```python
from typing import TypeVar, Optional, Dict, Any

T = TypeVar('T')

def get_cached_data(key: str, default: Optional[T] = None) -> Optional[T]:
    if key in cache:
        return cache[key]
    return default

def calculate_success_rate(solved: int, total: int) -> float:
    if total == 0:
        return 0.0
    return (solved / total) * 100.0
```

### Target Files
Start with:
- `core/utils/cache.py`
- `api/core/utils/cache.py`

### Required Skills
- [x] Python
- [x] Basic Type Hints Knowledge
- [ ] Other: _____

### Difficulty Level
- [x] Beginner Friendly
- [ ] Intermediate
- [ ] Advanced

### Estimated Time
- [x] Small (< 2 hours)
- [ ] Medium (2-4 hours)
- [ ] Large (4-8 hours)
- [ ] Extra Large (> 8 hours)

## Implementation Checklist
- [ ] Review current utility functions
- [ ] Add type hints to function parameters
- [ ] Add return type hints
- [ ] Add type hints for complex data structures
- [ ] Add docstrings explaining types
- [ ] Run mypy for type checking
- [ ] Update documentation

## Getting Started
1. Install mypy:
```bash
pip install mypy
```

2. Common type hints to use:
```python
from typing import (
    List, Dict, Set, Tuple,
    Optional, Union, Any,
    TypeVar, Generic
)
```

3. Run type checking:
```bash
mypy core/utils/cache.py
```

## Resources for Learning Type Hints
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)

## Tips
- Use Optional[T] for values that could be None
- Use Union[Type1, Type2] for values that could be multiple types
- Use TypeVar for generic type hints
- Add clear docstrings explaining complex types

This is a great first issue for:
- Learning Python type hints
- Understanding code documentation
- Using static type checkers
- Improving code maintainability

Labels: good first issue, enhancement, documentation, python
