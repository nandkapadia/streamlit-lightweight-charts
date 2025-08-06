# Frontend Test Suite Documentation

This document provides comprehensive information about the test suite for the streamlit-lightweight-charts-pro frontend.

## Overview

The frontend test suite is built using Jest and React Testing Library, providing comprehensive coverage for all components, utilities, and hooks. The test suite follows best practices for testing React applications and includes both unit and integration tests.

## Test Structure

```
frontend/
├── src/
│   ├── __tests__/                    # Main test files
│   │   ├── LightweightCharts.test.tsx
│   │   └── index.test.tsx
│   ├── components/
│   │   └── __tests__/
│   │       └── ErrorBoundary.test.tsx
│   ├── hooks/
│   │   └── __tests__/
│   │       └── useOptimizedChart.test.ts
│   ├── utils/
│   │   └── __tests__/
│   │       ├── chartDimensions.test.ts
│   │       └── performance.test.ts
│   └── setupTests.ts                 # Test setup and mocks
├── jest.config.js                    # Jest configuration
└── TESTING.md                        # This file
```

## Test Categories

### 1. Component Tests

#### LightweightCharts Component (`LightweightCharts.test.tsx`)
- **Component Rendering**: Tests basic rendering, custom dimensions, and callback handling
- **Chart Configuration**: Tests empty configs, multiple charts, and complex configurations
- **Error Handling**: Tests graceful handling of missing or invalid configurations
- **Performance**: Tests handling of large datasets and performance optimizations
- **Accessibility**: Tests ARIA attributes and keyboard accessibility
- **Responsive Design**: Tests window resize handling and container resizing

#### ErrorBoundary Component (`ErrorBoundary.test.tsx`)
- **Normal Rendering**: Tests rendering children without errors
- **Error Handling**: Tests catching and displaying various error types
- **Error Recovery**: Tests recovery when errors are resolved
- **Lifecycle**: Tests componentDidCatch and state management
- **Accessibility**: Tests ARIA attributes in error states
- **Performance**: Tests with large component trees and rapid error-recovery cycles
- **Edge Cases**: Tests null/undefined children and async errors

#### Index Component (`index.test.tsx`)
- **Component Rendering**: Tests main app rendering and configuration passing
- **Component Initialization**: Tests component ready state and error handling
- **Frame Height Management**: Tests frame height calculation and error handling
- **Resize Handling**: Tests window resize events and debouncing
- **Error Handling**: Tests missing configs and disabled states
- **Theme Integration**: Tests theme passing to chart components
- **Performance**: Tests large configurations efficiently
- **Cleanup**: Tests proper cleanup on unmount

### 2. Hook Tests

#### useOptimizedChart Hook (`useOptimizedChart.test.ts`)
- **Initialization**: Tests default values and custom options
- **Chart Management**: Tests adding, removing, and clearing charts
- **Series Management**: Tests adding, removing, and clearing series
- **Performance Optimization**: Tests debouncing and performance logging
- **Error Handling**: Tests chart creation and resize errors
- **State Management**: Tests initialization and disposal states
- **Cleanup**: Tests proper cleanup on unmount

### 3. Utility Tests

#### chartDimensions Utility (`chartDimensions.test.ts`)
- **Default Dimensions**: Tests fallback to default dimensions
- **Container Dimensions**: Tests using container dimensions when available
- **Edge Cases**: Tests zero, negative, and very large dimensions
- **Null/Undefined Handling**: Tests handling of null and undefined values

#### performance Utility (`performance.test.ts`)
- **Performance Logging**: Tests performance metrics logging
- **Error Handling**: Tests graceful error handling
- **Async Functions**: Tests async function performance logging
- **DOM Element Caching**: Tests cached DOM element retrieval
- **Style Optimization**: Tests optimized styles creation

## Test Configuration

### Jest Configuration (`jest.config.js`)
- **Environment**: Uses jsdom for DOM simulation
- **Coverage**: Enforces 80% coverage thresholds
- **Transform**: Handles TypeScript and JSX transformation
- **Mocking**: Mocks CSS and asset files
- **Timeout**: 10-second timeout for tests

### Test Setup (`setupTests.ts`)
- **DOM Mocks**: Mocks ResizeObserver, IntersectionObserver, and performance API
- **Library Mocks**: Mocks lightweight-charts and streamlit-component-lib
- **Console Mocks**: Reduces console noise during tests
- **Global Mocks**: Mocks requestAnimationFrame and DOM methods

## Running Tests

### Basic Commands
```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in CI mode
npm run test:ci

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- LightweightCharts.test.tsx

# Run tests matching pattern
npm test -- --testNamePattern="should render"
```

### Coverage Reports
```bash
# Generate coverage report
npm run test:coverage

# View coverage in browser
npm run test:coverage -- --coverageReporters=html
```

## Test Best Practices

### 1. Test Organization
- Group related tests using `describe` blocks
- Use descriptive test names that explain the expected behavior
- Follow the Arrange-Act-Assert pattern

### 2. Mocking Strategy
- Mock external dependencies (libraries, APIs)
- Use realistic mock data that represents actual usage
- Avoid over-mocking internal implementation details

### 3. Error Testing
- Test both success and error scenarios
- Verify error messages and error handling behavior
- Test edge cases and boundary conditions

### 4. Performance Testing
- Test with large datasets to ensure performance
- Verify debouncing and optimization features
- Test memory usage and cleanup

### 5. Accessibility Testing
- Test ARIA attributes and keyboard navigation
- Verify screen reader compatibility
- Test with different themes and color schemes

## Adding New Tests

### 1. Component Tests
```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import YourComponent from '../YourComponent';

describe('YourComponent', () => {
  it('should render correctly', () => {
    render(<YourComponent />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

### 2. Hook Tests
```typescript
import { renderHook, act } from '@testing-library/react';
import { useYourHook } from '../useYourHook';

describe('useYourHook', () => {
  it('should initialize correctly', () => {
    const { result } = renderHook(() => useYourHook());
    expect(result.current.value).toBe(expectedValue);
  });
});
```

### 3. Utility Tests
```typescript
import { yourUtility } from '../yourUtility';

describe('yourUtility', () => {
  it('should handle normal input', () => {
    const result = yourUtility(input);
    expect(result).toBe(expectedOutput);
  });
});
```

## Continuous Integration

The test suite is configured to run in CI environments with:
- Coverage reporting
- Fail-fast on errors
- Parallel test execution
- Artifact collection for coverage reports

## Troubleshooting

### Common Issues

1. **Mock Not Working**: Ensure mocks are defined before imports
2. **Async Test Failures**: Use `waitFor` for async operations
3. **Coverage Issues**: Check that files are included in coverage configuration
4. **Performance Issues**: Use `jest.useFakeTimers()` for timer-based tests

### Debugging Tests
```bash
# Run tests with verbose output
npm test -- --verbose

# Run single test with debugging
npm test -- --testNamePattern="specific test" --verbose

# Run tests with console output
npm test -- --silent=false
```

## Performance Considerations

- Tests should run quickly (< 10 seconds for full suite)
- Use appropriate mocks to avoid slow operations
- Implement proper cleanup to prevent memory leaks
- Use `jest.useFakeTimers()` for timer-based functionality

## Future Enhancements

1. **E2E Tests**: Add end-to-end tests using Playwright or Cypress
2. **Visual Regression Tests**: Add visual testing for chart rendering
3. **Performance Benchmarks**: Add performance benchmarking tests
4. **Accessibility Audits**: Add automated accessibility testing
5. **Integration Tests**: Add tests for component interactions

## Contributing

When adding new features or fixing bugs:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve coverage thresholds
4. Update this documentation if needed
5. Follow existing test patterns and conventions 