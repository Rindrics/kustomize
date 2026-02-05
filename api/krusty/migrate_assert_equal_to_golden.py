#!/usr/bin/env python3
"""
Migrate krusty tests from assert.Equal to AssertYAMLEqualsGolden.

This script replaces assert.Equal patterns with AssertYAMLEqualsGolden calls
for tests that use m.AsYaml() directly.
"""

import re
import sys

def migrate_test_file(content):
    """Convert assert.Equal patterns to AssertYAMLEqualsGolden."""
    
    # Pattern: assert.Equal(t, `multi-line string`, string(yml))
    # Replace with: AssertYAMLEqualsGolden(t, yml)
    # This matches multi-line backtick strings followed by string(yml)
    pattern = re.compile(
        r'assert\.Equal\(t,\s*`[^`]*`,\s*string\(yml\)\)',
        re.DOTALL
    )
    content = pattern.sub('AssertYAMLEqualsGolden(t, yml)', content)
    
    return content

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 migrate_assert_equal_to_golden.py <test_file>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Backup original
    with open(test_file + '.bak', 'w') as f:
        f.write(content)
    
    # Migrate
    new_content = migrate_test_file(content)
    
    # Write back
    with open(test_file, 'w') as f:
        f.write(new_content)
    
    print(f"Migrated {test_file}")
    print(f"Backup saved to {test_file}.bak")
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Add import if needed: kusttest_test.AssertYAMLEqualsGolden")
    print("3. Run: go test -update-golden -run TestName")
    print("4. Review generated golden files")
    print("5. Remove .bak file if everything looks good")

if __name__ == '__main__':
    main()
