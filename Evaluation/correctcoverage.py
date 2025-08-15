import os
import pandas as pd
import json
import re
import tempfile
import importlib.util
import coverage
import uuid
import sys

def get_expected_function_name(test_code):
    match = re.search(r'assert\s+(\w+)\s*\(', test_code)
    return match.group(1) if match else None

def run_tests(code_string, test_cases):
    func_name = "solve"
    total_tests = len(test_cases)
    tests_passed = 0

    # Save code to a temp file so coverage can access
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
        tmp_file.write(code_string)
        tmp_file.flush()
        tmp_path = tmp_file.name

    # Start coverage on that file
    cov = coverage.Coverage(include=[tmp_path])
    cov.start()

    # Import the file as a Python module
    module_name = f"mod_{uuid.uuid4().hex}"
    try:
        spec = importlib.util.spec_from_file_location(module_name, tmp_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error executing code: {e}")
        cov.stop()
        os.remove(tmp_path)
        return 0.0, 0.0

    if not hasattr(module, func_name):
        print(f"function '{func_name}' not defined. Skipping tests.")
        cov.stop()
        os.remove(tmp_path)
        return 0.0, 0.0

    for test_code in test_cases:
        expected_func_name = get_expected_function_name(test_code)
        try:
            test_env = {func_name: getattr(module, func_name)}
            if expected_func_name and expected_func_name != func_name:
                test_env[expected_func_name] = test_env[func_name]
            exec(test_code, {}, test_env)
            tests_passed += 1
        except Exception:
            continue

    cov.stop()
    cov.save()

    try:
        _, executable, missing, _ = cov.analysis(tmp_path)
        total = len(executable)
        covered = total - len(missing)
        coverage_pct = 100 * covered / total if total > 0 else 0.0
    except Exception as e:
        print(f"Coverage analysis failed: {e}")
        coverage_pct = 0.0

    os.remove(tmp_path)
    correctness_pct = 100 * tests_passed / total_tests if total_tests > 0 else 0.0
    return correctness_pct, coverage_pct

# Load test cases
test_cases = []
with open('mbpp.jsonl', 'r') as f:
    for line in f:
        entry = json.loads(line)
        test_cases.append(entry.get("test_list", []))

if len(sys.argv) < 2:
    print("Missing input folder")
    sys.sexit(1)
    
folder = sys.argv[1]
output_path = "correctcoverage.txt"

# Clear the output file at the start
with open(output_path, 'w') as out_file:
    out_file.write("")

for i in range(1, 975):

    file_path = os.path.join(folder, f"solution_{i}.csv")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    try:
        df = pd.read_csv(file_path)
        response_code = str(df.iloc[0, 2]).replace('\x00', '').strip()
        correctness_pct, coverage_pct = run_tests(response_code, test_cases[i - 1])

        # Write only correctness if coverage is 100%
        if coverage_pct == 100.0:
            with open(output_path, 'a') as out_file:
                out_file.write(f"solution_{i}.csv {correctness_pct:.2f}%\n")

        print(f"[{i}] correctness = {correctness_pct:.2f}% | coverage = {coverage_pct:.2f}%")
    except Exception as e:
        print(f"[{i}] Failed: {e}")

