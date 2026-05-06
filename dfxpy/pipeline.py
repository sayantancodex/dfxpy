import pandas as pd
from typing import List, Callable, Any, Dict
import json

class Pipeline:
    """
    A reusable cleaning and transformation pipeline.
    """
    def __init__(self, steps: List[Callable] = None):
        self.steps = steps or []
        self.history = []

    def add(self, step: Callable):
        """Add a transformation step to the pipeline."""
        self.steps.append(step)
        return self

    def run(self, df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
        """Run the pipeline on a DataFrame."""
        if verbose: print(f"\n--- RUNNING PIPELINE ({len(self.steps)} steps) ---")
        
        current_df = df.copy()
        for i, step in enumerate(self.steps):
            step_name = getattr(step, '__name__', f"Step {i+1}")
            if verbose: print(f"Executing: {step_name}...")
            current_df = step(current_df)
            self.history.append(step_name)
            
        if verbose: print("--- PIPELINE COMPLETED ---\n")
        return current_df

    def save(self, path: str):
        """Save pipeline steps to a JSON file."""
        step_names = [getattr(s, '__name__', 'unknown') for s in self.steps]
        with open(path, 'w') as f:
            json.dump({"steps": step_names}, f)
        print(f"Pipeline saved to {path}")

    @classmethod
    def load(cls, path: str, registry: Dict[str, Callable] = None):
        """Load pipeline steps from a JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        # If no registry provided, we'll try to find them in dfxpy (if we can)
        # For now, let's assume a registry is helpful or we just return the names
        steps = []
        if registry:
            steps = [registry[name] for name in data['steps'] if name in registry]
        
        pipe = cls(steps)
        print(f"Pipeline loaded from {path} ({len(steps)} steps resolved)")
        return pipe

    def __repr__(self):
        return f"DfxPipeline(steps={[getattr(s, '__name__', 'func') for s in self.steps]})"

def pipeline(steps: List[Callable] = None) -> Pipeline:
    """Helper to create a new Pipeline."""
    return Pipeline(steps)
