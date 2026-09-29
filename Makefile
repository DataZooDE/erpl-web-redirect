PROJ_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Configuration of extension
EXT_NAME=erpl_web
EXT_CONFIG=${PROJ_DIR}extension_config.cmake

# The stub cannot pass the extension-ci-tools SQL tests: they `require` the extension,
# and this one deliberately fails to load. scripts/smoke_test.py asserts that instead.
SKIP_TESTS=1

# Include the Makefile from extension-ci-tools
include extension-ci-tools/makefiles/duckdb_extension.Makefile

# Local end-to-end check of the release build: LOAD must fail with the redirect message.
.PHONY: test_redirect
test_redirect: release
	DUCKDB_BIN=./build/release/duckdb python3 scripts/smoke_test.py \
		$(PROJ_DIR)build/release/extension/erpl_web/erpl_web.duckdb_extension local local
