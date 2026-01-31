# run_tests_10_times.py
import pytest
import sys

if __name__ == "__main__":
    passed = 0
    failed = 0
    
    for i in range(1, 11):
        print(f"\n{'='*60}")
        print(f"EXECUTING TEST RUN {i}/10")
        print(f"{'='*60}")
        
        # Run pytest programmatically
        result = pytest.main([
            'tests/test_twich.py',
            '-v',
            '--tb=short'
        ])
        
        if result == 0:
            passed += 1
            print(f"✓ Run {i} PASSED")
        else:
            failed += 1
            print(f"✗ Run {i} FAILED")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {passed} passed, {failed} failed out of 10 runs")
    print(f"{'='*60}")
