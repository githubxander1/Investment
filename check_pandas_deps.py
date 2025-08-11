import sys
import subprocess
import pkg_resources

def check_pandas_numpy_deps():
    try:
        # Install specific versions in a temporary environment
        print("Checking pandas 1.5.3 numpy dependencies...")
        
        # Get pandas 1.5.3's numpy requirement
        # We'll use pkg_resources to parse the requirements
        # This simulates what pip would do
        req = pkg_resources.Requirement.parse("pandas==1.5.3")
        print(f"Pandas 1.5.3 requires numpy: {req.requires('numpy')}")
        
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        print("Falling back to checking PyPI metadata...")
        
        # Alternative approach: Check PyPI metadata using pip show
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "pandas==1.5.3"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("Pip show output:")
                print(result.stdout)
            else:
                print("Failed to get pip show info")
                print(f"Error: {result.stderr}")
        except Exception as e2:
            print(f"Error with pip show: {e2}")

if __name__ == "__main__":
    check_pandas_numpy_deps()