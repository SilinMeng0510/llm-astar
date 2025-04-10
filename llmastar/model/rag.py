import json
import numpy as np
from typing import List, Dict, Tuple, Any
import math
import heapq
import os
from pathlib import Path

class RAG:
    """Retrieval-Augmented Generation for LLM-A*."""
    
    def __init__(self, dataset_path: str = 'dataset_sft/environment_50_30.json'):
        """
        Initialize the RAG system for pathfinding.
        
        Args:
            dataset_path: Path to the dataset containing historical pathfinding examples.
        """
        self.dataset_path = dataset_path
        self.examples = self._load_examples()
        
    def _load_examples(self) -> List[Dict]:
        """
        Load historical examples from the dataset.
        
        Returns:
            List of examples containing pathfinding problems and solutions.
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
        
        # Load a small subset of examples (first 10) to have some data ready
        examples = []
        try:
            with open(self.dataset_path, 'r') as f:
                # Skip the opening bracket if it's a JSON array
                first_char = f.read(1)
                if first_char != '[':
                    f.seek(0)  # Reset if not a JSON array
                
                # Read the file line by line
                buffer = ""
                depth = 0
                in_example = False
                count = 0
                
                for line in f:
                    buffer += line
                    
                    # Count opening and closing braces to track JSON objects
                    depth += line.count('{') - line.count('}')
                    
                    if depth > 0:
                        in_example = True
                    elif in_example and depth == 0:
                        # We have a complete example
                        try:
                            # Remove trailing comma if present
                            if buffer.rstrip().endswith(','):
                                buffer = buffer.rstrip()[:-1]
                            
                            example = json.loads(buffer)
                            examples.append(example)
                            count += 1
                            
                            # Only load a small subset
                            if count >= 10:
                                break
                        except json.JSONDecodeError:
                            # Skip invalid JSON
                            pass
                        
                        # Reset for next example
                        buffer = ""
                        in_example = False
        except Exception as e:
            print(f"Warning: Error loading examples from dataset: {e}")
            
        print(f"Preloaded {len(examples)} examples from dataset")
        return examples
    
    def _similarity_score(self, query: Dict[str, Any], example: Dict[str, Any]) -> float:
        """
        Calculate similarity score between query and example.
        
        Args:
            query: The current pathfinding query.
            example: A historical example from the dataset.
            
        Returns:
            Similarity score (higher means more similar).
        """
        score = 0.0
        
        # Start and goal points similarity
        start_distance = self._euclidean_distance(query['start'], example['start_goal'][0]['start'])
        goal_distance = self._euclidean_distance(query['goal'], example['start_goal'][0]['goal'])
        
        # Normalize by the diagonal of the environment
        env_diagonal = math.sqrt((query['range_x'][1] - query['range_x'][0])**2 + 
                                 (query['range_y'][1] - query['range_y'][0])**2)
        
        # Start and goal similarity (inversely proportional to distance)
        start_sim = 1.0 - (start_distance / env_diagonal)
        goal_sim = 1.0 - (goal_distance / env_diagonal)
        
        # Calculate barrier similarity
        h_barriers_sim = self._barrier_similarity(query.get('horizontal_barriers', []), 
                                                example.get('horizontal_barriers', []))
        v_barriers_sim = self._barrier_similarity(query.get('vertical_barriers', []), 
                                                example.get('vertical_barriers', []))
        
        # Look for intelligent waypoints if available
        waypoints_sim = 0.0
        if ('start_goal' in example and 
            'waypoints_intelligent' in example['start_goal'][0]):
            # For now, we don't need to compare waypoints, just note they exist
            waypoints_sim = 0.5  # Give a bonus to examples with waypoints
        
        # Print debug info
        if os.environ.get('RAG_DEBUG'):
            print(f"Similarity scores - Start: {start_sim:.2f}, Goal: {goal_sim:.2f}, " +
                  f"H-Barriers: {h_barriers_sim:.2f}, V-Barriers: {v_barriers_sim:.2f}, " +
                  f"Waypoints: {waypoints_sim:.2f}")
        
        # Weighted combination of similarities
        score = 0.35 * start_sim + 0.35 * goal_sim + 0.1 * h_barriers_sim + 0.1 * v_barriers_sim + 0.1 * waypoints_sim
        
        return score
    
    def _barrier_similarity(self, barriers1: List, barriers2: List) -> float:
        """
        Calculate similarity between two sets of barriers.
        
        Args:
            barriers1: First set of barriers.
            barriers2: Second set of barriers.
            
        Returns:
            Similarity score (higher means more similar).
        """
        if not barriers1 and not barriers2:
            return 1.0  # Both empty means they're identical
        
        if not barriers1 or not barriers2:
            return 0.0  # One empty and one not means they're different
        
        # Compare barriers by checking overlap
        total_similarity = 0.0
        normalizer = max(len(barriers1), len(barriers2))
        
        # Simple matching - just count how many are close to each other
        matched = 0
        for b1 in barriers1:
            for b2 in barriers2:
                # If they're the same type of barrier and have similar positions
                if len(b1) == len(b2) and abs(b1[0] - b2[0]) < 5:  # Arbitrary threshold
                    matched += 1
                    break
        
        return matched / normalizer if normalizer > 0 else 0.0
    
    @staticmethod
    def _euclidean_distance(p1: List[int], p2: List[int]) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            p1: First point as [x, y].
            p2: Second point as [x, y].
            
        Returns:
            Euclidean distance.
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def retrieve_examples(self, query: Dict[str, Any], top_k: int = 3) -> List[Dict]:
        """
        Retrieve the top k most similar examples to the query.
        
        Args:
            query: The current pathfinding query.
            top_k: Number of examples to retrieve.
            
        Returns:
            List of top k most similar examples.
        """
        # Check if we have preloaded examples first
        if self.examples:
            # Calculate similarity for preloaded examples
            top_examples = []
            similarities = []
            
            for i, example in enumerate(self.examples):
                similarity = self._similarity_score(query, example)
                
                # Keep track of top k examples
                if len(top_examples) < top_k:
                    heapq.heappush(similarities, (similarity, len(top_examples)))
                    top_examples.append(example)
                elif similarity > similarities[0][0]:
                    # Replace the least similar example
                    idx = similarities[0][1]
                    heapq.heapreplace(similarities, (similarity, idx))
                    top_examples[idx] = example
                    
            # If we have enough examples and the least similar is very similar, just return them
            if len(top_examples) == top_k and similarities[0][0] > 0.7:  # Arbitrary threshold
                return [top_examples[idx] for _, idx in sorted(similarities, reverse=True)]
        
        # If we don't have enough good examples, process more from the file
        top_examples = []
        similarities = []
        
        # Process the file in chunks to avoid loading it all at once
        with open(self.dataset_path, 'r') as f:
            # Skip the opening bracket
            first_char = f.read(1)
            if first_char != '[':
                f.seek(0)  # Reset if not a JSON array
                
            # Read the file line by line
            buffer = ""
            depth = 0
            in_example = False
            
            for line in f:
                buffer += line
                
                # Count opening and closing braces to track JSON objects
                depth += line.count('{') - line.count('}')
                
                if depth > 0:
                    in_example = True
                elif in_example and depth == 0:
                    # We have a complete example
                    try:
                        # Remove trailing comma if present
                        if buffer.rstrip().endswith(','):
                            buffer = buffer.rstrip()[:-1]
                        
                        example = json.loads(buffer)
                        similarity = self._similarity_score(query, example)
                        
                        # Keep track of top k examples
                        if len(top_examples) < top_k:
                            heapq.heappush(similarities, (similarity, len(top_examples)))
                            top_examples.append(example)
                        elif similarity > similarities[0][0]:
                            # Replace the least similar example
                            idx = similarities[0][1]
                            heapq.heapreplace(similarities, (similarity, idx))
                            top_examples[idx] = example
                    except json.JSONDecodeError:
                        # Skip invalid JSON
                        pass
                    
                    # Reset for next example
                    buffer = ""
                    in_example = False
        
        # Sort top examples by similarity (descending)
        top_examples = [top_examples[idx] for _, idx in sorted(similarities, reverse=True)]
        
        return top_examples
    
    def format_examples_for_prompt(self, examples: List[Dict]) -> str:
        """
        Format retrieved examples for inclusion in the LLM prompt.
        
        Args:
            examples: List of retrieved examples.
            
        Returns:
            Formatted string to be added to the prompt.
        """
        formatted = "\nHere are some similar pathfinding examples to help guide you:\n\n"
        
        for i, example in enumerate(examples):
            start = example['start_goal'][0]['start']
            goal = example['start_goal'][0]['goal']
            h_barriers = example['horizontal_barriers']
            v_barriers = example['vertical_barriers']
            range_x = example['range_x']
            range_y = example['range_y']
            
            # Get the intelligent waypoints if available
            waypoints = example['start_goal'][0].get('waypoints_intelligent', [])
            if not waypoints and 'path' in example['start_goal'][0]:
                # Fallback to path if waypoints_intelligent is not available
                waypoints = example['start_goal'][0]['path']
            
            formatted += f"Example {i+1}:\n"
            formatted += f"Start Point: {start}\n"
            formatted += f"Goal Point: {goal}\n"
            formatted += f"Range X: {range_x}\n"
            formatted += f"Range Y: {range_y}\n"
            formatted += f"Horizontal Barriers: {h_barriers}\n"
            formatted += f"Vertical Barriers: {v_barriers}\n"
            
            if waypoints:
                formatted += f"Waypoints: {waypoints}\n"
            
            formatted += "\n"
        
        return formatted 