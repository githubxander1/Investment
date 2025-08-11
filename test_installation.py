import pandas as pd
import numpy as np

# Check versions
print(f"Pandas version: {pd.__version__}")
print(f"Numpy version: {np.__version__}")

# Create a simple DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Perform operations that use numpy
df['C'] = np.square(df['A'])

print("Test DataFrame:")
print(df)

print("Test completed successfully!")