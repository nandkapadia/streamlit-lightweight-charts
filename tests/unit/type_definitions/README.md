# Type Definitions Unit Tests

This directory contains unit tests for the `type_definitions` module.

## Test Coverage

### colors.py - 100% Coverage ✅

The `colors.py` module has comprehensive test coverage with **57 test cases** covering:

#### `_is_valid_color` Function Tests
- **Hex Colors**: 3-digit and 6-digit hex colors (valid and invalid)
- **RGB Colors**: Standard RGB format with various spacing patterns
- **RGBA Colors**: RGBA format with alpha values (including edge cases)
- **Named Colors**: All supported CSS named colors with case insensitivity
- **Invalid Inputs**: Non-string types, empty strings, whitespace, special characters
- **Edge Cases**: Mixed case hex, extra spaces, malformed color strings

#### `BackgroundSolid` Class Tests
- **Construction**: Default and custom construction
- **Color Validation**: All color format types (hex, rgb, rgba, named)
- **Error Handling**: Invalid colors, empty strings, None values
- **Serialization**: `to_dict()` method with camelCase conversion
- **Style Behavior**: Style attribute mutability

#### `BackgroundGradient` Class Tests
- **Construction**: Default and custom construction with two colors
- **Color Validation**: Both top and bottom color validation
- **Error Handling**: Invalid colors for both top and bottom
- **Serialization**: `to_dict()` method with proper key conversion
- **Style Behavior**: Style attribute mutability

#### `Background` Union Type Tests
- **Type Compatibility**: Both BackgroundSolid and BackgroundGradient
- **Collection Usage**: Lists and dictionaries containing background objects

#### Integration Tests
- **Serialization Chains**: Complete serialization workflows
- **Object Collections**: Background objects in lists and dictionaries
- **Error Messages**: Detailed error message validation

#### Edge Case Tests
- **Color Format Variations**: Different spacing, case sensitivity
- **Special Characters**: Invalid characters in color strings
- **Boundary Conditions**: Empty strings, None values, whitespace

## Test Statistics

- **Total Tests**: 57
- **Code Coverage**: 100%
- **Lines Covered**: 39/39
- **Functions Covered**: 3/3
- **Classes Covered**: 2/2

## Test Organization

Tests are organized into logical test classes:

1. **TestIsValidColor**: Tests for the color validation function
2. **TestBackgroundSolid**: Tests for solid background class
3. **TestBackgroundGradient**: Tests for gradient background class
4. **TestBackgroundUnion**: Tests for union type compatibility
5. **TestColorValidationEdgeCases**: Edge case validation tests
6. **TestBackgroundIntegration**: Integration and serialization tests
7. **TestBackgroundErrorMessages**: Error message validation tests

## Running Tests

```bash
# Run all type_definitions tests
python -m pytest tests/unit/type_definitions/ -v

# Run only colors tests
python -m pytest tests/unit/type_definitions/test_colors.py -v

# Run with coverage
python -m pytest tests/unit/type_definitions/test_colors.py --cov=streamlit_lightweight_charts_pro.type_definitions.colors --cov-report=term-missing
```

## Key Testing Insights

1. **Regex Behavior**: The RGBA regex pattern `[\d.]+` accepts alpha values > 1, which is reflected in the tests
2. **Style Mutability**: Background style attributes can be changed after initialization (dataclass fields are not frozen)
3. **Color Flexibility**: The validation accepts various color formats with different spacing patterns
4. **Error Handling**: Comprehensive error messages for invalid color formats
5. **Serialization**: Proper camelCase conversion for frontend compatibility

## Future Enhancements

- Consider adding tests for additional color formats if supported
- Add performance tests for color validation with large datasets
- Consider adding property-based testing for more comprehensive edge case coverage 