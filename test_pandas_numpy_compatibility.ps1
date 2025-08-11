# Create a temporary virtual environment
echo "Creating test environment..."
$env_name = "test_pandas_numpy"
$python_path = Get-Command python | Select-Object -ExpandProperty Source
$venv_path = Join-Path -Path $PSScriptRoot -ChildPath $env_name

# Remove existing environment if it exists
if (Test-Path -Path $venv_path) {
    Remove-Item -Path $venv_path -Recurse -Force
}

# Create new environment
& $python_path -m venv $venv_path
if (-not $?) {
    echo "Failed to create virtual environment"
    exit 1
}

echo "Virtual environment created at $venv_path"

# Activate environment
$activate_script = Join-Path -Path $venv_path -ChildPath "Scripts\Activate.ps1"
. $activate_script

# Install specific versions
 echo "Installing numpy==2.3.2..."
 pip install numpy==2.3.2
if (-not $?) {
    echo "Failed to install numpy==2.3.2"
    exit 1
}

echo "Installing pandas==1.5.3..."
 pip install pandas==1.5.3
if (-not $?) {
    echo "Failed to install pandas==1.5.3 with numpy==2.3.2"
    exit 1
}

echo "Successfully installed pandas==1.5.3 with numpy==2.3.2"

echo "Testing compatibility..."
# Create and run test script
$test_script = Join-Path -Path $PSScriptRoot -ChildPath "test_compatibility.py"
Set-Content -Path $test_script -Value @"
import pandas as pd
import numpy as np

# Check versions
print(f"Pandas version: {pd.__version__}")
print(f"Numpy version: {np.__version__}")

# Create a simple DataFrame
df = pd.DataFrame({
    ' A' : [1, 2, 3],
    ' B' : [4, 5, 6]
})

# Perform operations that use numpy
print("Testing numpy integration...")
df[' C' ] = np.square(df[' A' ])
print(df)

print("Compatibility test passed successfully!")
"@

# Run test script
python $test_script
if (-not $?) {
    echo "Compatibility test failed"
    exit 1
}

echo "Cleaning up..."
# Deactivate and remove environment
Remove-Item -Path $venv_path -Recurse -Force
Remove-Item -Path $test_script -Force

echo "Test completed successfully! pandas 1.5.3 is compatible with numpy 2.3.2"