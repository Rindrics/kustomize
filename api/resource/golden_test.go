// Copyright 2020 The Kubernetes Authors.
// SPDX-License-Identifier: Apache-2.0

package resource_test

import (
	"flag"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

var update = flag.Bool("update", false, "update golden files")

// goldenFile returns the path to the golden file for the given test name.
func goldenFile(t *testing.T, name string) string {
	return filepath.Join("testdata", "golden", name+".golden")
}

// assertGolden compares the actual output with the golden file.
// If -update flag is set, it updates the golden file instead.
func assertGolden(t *testing.T, name string, actual []byte) {
	t.Helper()
	goldenPath := goldenFile(t, name)

	if *update {
		// Update golden file
		dir := filepath.Dir(goldenPath)
		require.NoError(t, os.MkdirAll(dir, 0755))
		require.NoError(t, os.WriteFile(goldenPath, actual, 0644))
		t.Logf("Updated golden file: %s", goldenPath)
		return
	}

	// Read golden file
	expected, err := os.ReadFile(goldenPath)
	if err != nil {
		if os.IsNotExist(err) {
			t.Fatalf("Golden file does not exist: %s\nRun tests with -update flag to create it.\nActual output:\n%s", goldenPath, string(actual))
		}
		t.Fatalf("Failed to read golden file: %v", err)
	}

	// Compare
	assert.Equal(t, string(expected), string(actual), "Output does not match golden file. Run with -update to update it.")
}
