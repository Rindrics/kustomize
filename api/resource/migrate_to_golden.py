#!/usr/bin/env python3
"""
Migrate resource_test.go to use golden file testing.

This script replaces assert.Equal patterns with assertGoldenYAML calls.
"""

import re
import sys

def migrate_test_file(content):
    """Convert assert.Equal patterns to assertGoldenYAML."""
    
    # Pattern 1: assert.Equal(t, `multi-line string`, string(bytes))
    # Replace with: assertGoldenYAML(t, bytes)
    pattern1 = re.compile(
        r'assert\.Equal\(t,\s*`[^`]*`,\s*string\(bytes\)\)',
        re.DOTALL
    )
    content = pattern1.sub('assertGoldenYAML(t, bytes)', content)
    
    # Pattern 2: assert.Equal(t, expected, string(bytes))
    # Replace with: assertGoldenYAML(t, bytes)
    # Note: This assumes 'expected' variable is no longer needed
    pattern2 = re.compile(
        r'assert\.Equal\(t,\s*expected,\s*string\(bytes\)\)'
    )
    content = pattern2.sub('assertGoldenYAML(t, bytes)', content)
    
    # Pattern 3: assert.Equal(t, tc.expectedOutput, string(bytes))
    # Replace with: assertGoldenYAML(t, bytes)
    pattern3 = re.compile(
        r'assert\.Equal\(t,\s*tc\.expectedOutput,\s*string\(bytes\)\)'
    )
    content = pattern3.sub('assertGoldenYAML(t, bytes)', content)
    
    # Pattern 4: assert.Equal(t, test.expected, string(bytes), ...)
    # Replace with: assertGoldenYAML(t, bytes)
    pattern4 = re.compile(
        r'assert\.Equal\(t,\s*test\.expected,\s*string\(bytes\)[^)]*\)'
    )
    content = pattern4.sub('assertGoldenYAML(t, bytes)', content)
    
    return content

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 migrate_to_golden.py <test_file>")
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
    print("2. Run: go test -update ./...")
    print("3. Review generated golden files")
    print("4. Remove .bak file if everything looks good")

if __name__ == '__main__':
    main()
