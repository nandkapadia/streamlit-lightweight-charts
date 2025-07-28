#!/usr/bin/env python3
"""
Script to fix validation tests by converting them from construction-time validation
to chainable method validation.
"""

import re
import os
from pathlib import Path


def fix_validation_tests(file_path):
    """Fix validation tests in a file by converting them to use chainable methods."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match validation tests that expect exceptions during construction
    # This matches patterns like:
    # with pytest.raises(TypeError, match="field must be a type"):
    #     ClassName(field="invalid")
    pattern = r'(\s+)def test_validation_(\w+)\(self\):\s*\n\s+"""Test validation of \w+ field\."""\s*\n\s+with pytest\.raises\(([^,]+), match="([^"]+)"\):\s*\n\s+(\w+)\((\w+)="invalid"\)'
    
    def replace_validation_test(match):
        indent = match.group(1)
        field_name = match.group(2)
        exception_type = match.group(3)
        error_message = match.group(4)
        class_name = match.group(5)
        field_param = match.group(6)
        
        # Convert to chainable method validation
        new_content = f'''{indent}def test_validation_{field_name}(self):
{indent}    """Test validation of {field_name} field."""
{indent}    options = {class_name}()
{indent}    with pytest.raises({exception_type}, match="{error_message.replace("must be a", "must be of type")}"):
{indent}        options.set_{field_name}("invalid")'''
        
        return new_content
    
    # Apply the replacement
    new_content = re.sub(pattern, replace_validation_test, content)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    return content != new_content


def main():
    """Main function to fix all validation tests."""
    test_dir = Path("tests/unit/options")
    
    # Files that need to be fixed (excluding the ones we already fixed)
    files_to_fix = [
        "test_layout_options.py",
        "test_other_options.py", 
        "test_price_scale_options.py",
        "test_ui_options.py"
    ]
    
    for file_name in files_to_fix:
        file_path = test_dir / file_name
        if file_path.exists():
            print(f"Fixing {file_path}...")
            changed = fix_validation_tests(file_path)
            if changed:
                print(f"  ✅ Updated {file_path}")
            else:
                print(f"  ⚠️  No changes needed for {file_path}")
        else:
            print(f"  ❌ File not found: {file_path}")


if __name__ == "__main__":
    main() 