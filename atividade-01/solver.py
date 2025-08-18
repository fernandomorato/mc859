#!/usr/bin/env python3

import gurobipy as gp
from gurobipy import GRB
import sys 
import os 
import csv

class MaxScQbfSolver:
    """
    A class to model and solve the MAX-SC-QBF problem using Gurobi.
    
    This class handles:
    - Parsing an instance file.
    - Building the corresponding Gurobi optimization model.
    - Solving the model.
    - Reporting the results to the console and saving them to a CSV file.
    """
    def __init__(self, file_path):
        """
        Initializes the solver by parsing the instance file and setting up paths.
        
        Args:
            file_path (str): The path to the MAX-SC-QBF instance file.
        """
        self.instance_path = file_path
        self.instance_name = os.path.basename(file_path)
        
        print(f"--- Initializing Solver for: {self.instance_name} ---")
        try:
            # Parse the instance file and store data as instance attributes
            self.n, self.subsets, self.A = self._parse_instance_file(file_path)
            print(f"Successfully loaded instance with n = {self.n}.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            # Exit if the file cannot be loaded
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while parsing the file: {e}")
            sys.exit(1)
            
        # Determine and create the output path for the solution CSV
        script_dir = os.path.dirname(os.path.abspath(__file__))
        solutions_dir = os.path.join(script_dir, "solutions")
        os.makedirs(solutions_dir, exist_ok=True)
        
        csv_filename = os.path.splitext(self.instance_name)[0] + '.csv'
        self.solution_csv_path = os.path.join(solutions_dir, csv_filename)
        
        # Initialize placeholders for the Gurobi model and variables
        self.model = None
        self.x_vars = None
        self.y_vars = None

    def _parse_instance_file(self, file_path):
        """
        Parses a MAX-SC-QBF instance file and returns the data in Python format.
        """
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        n = int(lines[0])
        subsets = []
        subset_lines = lines[2 : 2 + n]
        for line in subset_lines:
            elements = {int(element) - 1 for element in line.split()}
            subsets.append(elements)

        A = {}
        matrix_lines = lines[2 + n :]
        for i, line in enumerate(matrix_lines):
            coefficients = [int(c) for c in line.split()]
            for k, coeff in enumerate(coefficients):
                j = i + k
                if coeff != 0:
                    A[(i, j)] = coeff
        return n, subsets, A

    def _build_model(self):
        """Builds the Gurobi optimization model, including variables,
        objective, and constraints."""
        
        # Initialize the Gurobi model object
        self.model = gp.Model("MAX-SC-QBF")

        # Add decision variables
        self.x_vars = self.model.addVars(self.n, vtype=GRB.BINARY, name="x")
        self.y_vars = self.model.addVars(self.A.keys(), vtype=GRB.BINARY, name="y")

        # Set the objective function
        self.model.setObjective(self.y_vars.prod(self.A), GRB.MAXIMIZE)

        # Set Covering Constraints
        for k in range(self.n):
            self.model.addConstr(gp.quicksum(self.x_vars[i] for i, s in enumerate(self.subsets) if k in s) >= 1)
        
        # Linearization Constraints        
        for i, j in self.y_vars.keys():
            self.model.addConstr(self.y_vars[i, j] <= self.x_vars[i])
            self.model.addConstr(self.y_vars[i, j] <= self.x_vars[j])
            self.model.addConstr(self.y_vars[i, j] >= self.x_vars[i] + self.x_vars[j] - 1)
            
        # Update model to reflect changes, ensuring NumVars and NumConstrs are correct
        self.model.update()

    def solve(self, time_limit=None):
        """
        Builds and solves the model, then reports the results.
        
        Args:
            time_limit (int, optional): The time limit for the solver in seconds.
                                        Defaults to None (no limit).
        """
        # Build the model structure
        self._build_model()
        
        if time_limit:
            self.model.Params.TimeLimit = time_limit

        # Tell Gurobi to focus on finding good feasible solutions quickly.
        self.model.Params.MIPFocus = 1
        
        # Tell Gurobi to spend 10% of its time on heuristics.
        self.model.Params.Heuristics = 0.1            
        
        # Suppress Gurobi's console output for cleaner experiment logs
        self.model.Params.OutputFlag = 0
        self.model.optimize()
        
        # Print the solution details and save in CSV file
        self._report_results()
        self._save_results_to_csv()

    def _report_results(self):
        """Prints a summary of the solution found by Gurobi to the console."""
        status = self.model.Status
        if status == GRB.OPTIMAL:
            print(f"-> Optimal solution found. Objective: {self.model.ObjVal:g}")

            selected_subsets = [i + 1 for i in range(self.n) if self.x_vars[i].X > 0.5]
            print(f"\nSelected Subsets: {selected_subsets}")

        elif status == GRB.TIME_LIMIT:
            print(f"-> Time limit reached. Best objective: {self.model.ObjVal:g}, Gap: {self.model.MIPGap*100:.2f}%")
        elif status == GRB.INFEASIBLE:
            print("-> Model is infeasible.")
        else:
            print(f"-> Optimization finished with status code: {status}")

    def _save_results_to_csv(self):
        """Saves the required experiment results to a CSV file."""
        header = ['solution_value', 'optimality_gap', 'execution_time']
        
        # Prepare data, with fallbacks for non-optimal solutions
        if self.model.SolCount > 0:
            solution_value = self.model.ObjVal
            optimality_gap = self.model.MIPGap
        else:
            # Handle cases with no solution (e.g., infeasible)
            solution_value = 'N/A'
            optimality_gap = 'N/A'
            
        execution_time = self.model.Runtime
        
        data = [solution_value, optimality_gap, execution_time]
        
        try:
            with open(self.solution_csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(data)
            print(f"-> Results saved to '{self.solution_csv_path}'")
        except IOError as e:
            print(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    # Get the script's directory and define paths for instances and solutions
    script_dir = os.path.dirname(os.path.abspath(__file__))
    instances_directory = os.path.join(script_dir, "instances")
    solutions_directory = os.path.join(script_dir, "solutions")

    # Ensure the instances directory exists before proceeding
    if not os.path.isdir(instances_directory):
        print(f"Error: The 'instances' directory was not found at '{instances_directory}'")
        print("Please run the 'generator.py' script first to create the instances.")
        sys.exit(1)
        
    # Get all .txt instance files from the directory
    all_files = [f for f in os.listdir(instances_directory) if f.endswith('.txt')]

    # Sort files numerically based on the 'n' value in the filename for ordered processing
    instance_files = sorted(all_files, key=lambda f: int(f.split('_')[1][1:]))
    
    if not instance_files:
        print(f"No instance files (.txt) found in '{instances_directory}'.")
        sys.exit(1)
        
    print(f"Found {len(instance_files)} instances to process.")
    print("="*40)
    
    # Loop through all instance files
    for filename in instance_files:
        # Construct the expected path for the solution file
        solution_filename = os.path.splitext(filename)[0] + '.csv'
        solution_path = os.path.join(solutions_directory, solution_filename)
        
        # Check if the solution file already exists
        if os.path.exists(solution_path):
            print(f"--- Skipping {filename} (solution already exists) ---")
            continue # Move to the next file
        
        # If no solution exists, proceed with solving the instance
        instance_path = os.path.join(instances_directory, filename)
        
        # Instantiate and run the solver for the current instance
        solver = MaxScQbfSolver(instance_path)
        solver.solve(time_limit=600) # 10-minute time limit
        print("-" * 40)
        
    print("All instances have been processed.")