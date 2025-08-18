import os
import random

def _generate_sparse_sets(n):
    """Generates sets where each element is covered by few other sets."""
    subsets = [set() for _ in range(n)]
    # For each element, choose a small number of sets to add it to.
    for element in range(n):
        num_covers = random.randint(2, 4)
        # Ensure we can select enough unique sets.
        num_covers = min(num_covers, n)
        covering_sets_indices = random.sample(range(n), num_covers)
        for index in covering_sets_indices:
            subsets[index].add(element)
    return subsets

def _generate_dense_sets(n):
    """Generates sets where each element is covered by many other sets."""
    subsets = [set() for _ in range(n)]
    # For each element, choose a large number of sets to add it to.
    for element in range(n):
        min_covers = n // 5  # At least 20%
        max_covers = n // 2  # At most 50%
        num_covers = random.randint(min_covers, max_covers)
        num_covers = min(num_covers, n)
        covering_sets_indices = random.sample(range(n), num_covers)
        for index in covering_sets_indices:
            subsets[index].add(element)
    return subsets
    
def _generate_structured_sets(n):
    """Generates a few large 'hub' sets and many small, specialized sets."""
    subsets = [set() for _ in range(n)]
    
    # Designate ~10% of sets as large hubs
    num_hubs = max(1, n // 10)
    hub_indices = random.sample(range(n), num_hubs)
    
    for i in range(n):
        if i in hub_indices:
            # Hubs are large: cover 20-50% of elements
            size = random.randint(n // 5, n // 2)
            subsets[i] = set(random.sample(range(n), size))
        else:
            # Other sets are small: cover 2-5 elements
            size = random.randint(2, 5)
            subsets[i] = set(random.sample(range(n), min(size, n)))

    # Final check: ensure every element is covered by at least one set
    all_covered_elements = set.union(*subsets)
    uncovered = set(range(n)) - all_covered_elements
    for element in uncovered:
        # Add any uncovered element to a random set
        random_set_index = random.randint(0, n - 1)
        subsets[random_set_index].add(element)
        
    return subsets

def _generate_matrix_A(n):
    """Generates the upper-triangular matrix A with random coefficients."""
    A = {}
    for i in range(n):
        for j in range(i, n):
            # Use a non-trivial range that includes negative values
            A[(i, j)] = random.randint(-20, 20)
    return A

def _write_instance_to_file(n, subsets, A, file_path):
    """Writes the generated instance data to a file in the specified format."""
    with open(file_path, 'w') as f:
        # Write n
        f.write(f"{n}\n")
        
        # Write the size of each subset
        subset_sizes = [len(s) for s in subsets]
        f.write(" ".join(map(str, subset_sizes)) + "\n")
        
        # Write the elements of each subset (1-indexed)
        for s in subsets:
            # Convert 0-indexed elements back to 1-indexed for the file
            elements_1_indexed = sorted([e + 1 for e in s])
            f.write(" ".join(map(str, elements_1_indexed)) + "\n")
            
        # Write the upper triangular matrix A
        for i in range(n):
            row_values = []
            for j in range(i, n):
                row_values.append(A.get((i, j), 0))
            f.write(" ".join(map(str, row_values)) + "\n")

def generate_instance(n, pattern, file_path):
    """
    Main function to generate a single instance.
    
    Args:
        n (int): The number of variables for the instance.
        pattern (str): The generation pattern ('sparse', 'dense', or 'structured').
        file_path (str): The full path where the instance file will be saved.
    """
    if pattern == 'sparse':
        subsets = _generate_sparse_sets(n)
    elif pattern == 'dense':
        subsets = _generate_dense_sets(n)
    elif pattern == 'structured':
        subsets = _generate_structured_sets(n)
    else:
        raise ValueError("Unknown pattern type specified.")
        
    A = _generate_matrix_A(n)
    
    _write_instance_to_file(n, subsets, A, file_path)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Set a seed for the random number generator to ensure replicability.
    # Using the same seed will produce the exact same set of instances every time.
    random.seed(42) 

    n_values = [25, 50, 100, 200, 400]
    patterns = ['sparse', 'dense', 'structured']
    
    # Get the directory of the current script to create the 'instances' subdir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    instances_dir = os.path.join(script_dir, "instances")
    
    # Create the 'instances' directory if it doesn't exist
    os.makedirs(instances_dir, exist_ok=True)
    
    print(f"Generating 15 instances in '{instances_dir}'...")
    
    # Loop through all combinations of n and pattern to generate 15 instances
    for n in n_values:
        for p in patterns:
            # Construct a descriptive filename
            filename = f"instance_n{n}_{p}.txt"
            full_path = os.path.join(instances_dir, filename)
            
            # Generate and save the instance
            generate_instance(n, p, full_path)
            print(f"  -> Created {filename}")
            
    print("\nInstance generation complete.")