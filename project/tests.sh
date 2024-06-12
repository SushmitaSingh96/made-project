#!/bin/bash

# Path to the test scripts
TEST_SCRIPTS=(
    "project/components/ingest_dataprep_integration_test.py"
    "project/components/save_data_component_test.py"
    "project/pipeline_system_test.py"
)

# Run each test script
for TEST_SCRIPT in "${TEST_SCRIPTS[@]}"; do
    echo "Running test: $TEST_SCRIPT"
    python3 "$TEST_SCRIPT"
    if [ $? -ne 0 ]; then
        echo "Test failed: $TEST_SCRIPT"
        exit 1
    fi
done

echo "All tests passed."
