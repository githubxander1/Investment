import pandas as pd
import numpy as np

# Check versions
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# Test basic operations
df = pd.DataFrame({'data': [1, 2, 3]})
print("DataFrame created successfully:")
print(df)

# Test numpy integration
df['squared'] = np.square(df['data'])
print("Added squared column using numpy:")
print(df)

print("All tests completed successfully!")