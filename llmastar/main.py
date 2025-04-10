import argparse
from time import strftime
import os
import json
import matplotlib.pyplot as plt

from llmastar.pather.a_star.a_star import AStar
from llmastar.pather.llm_a_star.llm_a_star import LLMAStar
from llmastar.pather.llm_a_star.prompt import *

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Path Planning Algorithms')
    parser.add_argument('--algo', choices=['a_star', 'llm_a_star'], default='llm_a_star',
                        help='Choose a path planning algorithm')
    parser.add_argument('--llm', choices=['gpt', 'llama'], default='gpt',
                        help='Choose an LLM for path planning')
    parser.add_argument('--prompt_type', choices=['standard', 'cot', 'repe'], default='standard',
                        help='Choose a prompt type for LLM-A*')
    parser.add_argument('--query', type=str, required=True,
                        help='Input query for planning (or a JSON config file)')
    parser.add_argument('--output_dir', type=str, default='./output',
                        help='Output directory for results')
    parser.add_argument('--use_rag', action='store_true', default=True,
                        help='Use RAG (Retrieval-Augmented Generation) for LLM-A*')
    parser.add_argument('--no_rag', dest='use_rag', action='store_false',
                        help='Disable RAG (Retrieval-Augmented Generation)')
    
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Generate output filename
    timestamp = strftime("%Y%m%d_%H%M%S")
    output_file = f"{args.output_dir}/{args.algo}_{timestamp}"
    
    # Initialize planner
    if args.algo == 'a_star':
        planner = AStar()
    elif args.algo == 'llm_a_star':
        planner = LLMAStar(llm=args.llm, prompt=args.prompt_type, use_rag=args.use_rag)
    else:
        raise ValueError(f"Invalid algorithm: {args.algo}")
    
    # Read query
    if os.path.isfile(args.query):
        with open(args.query, 'r') as f:
            query = f.read()
    else:
        query = args.query
    
    # Run planning
    result = planner.searching(query, filepath=f"{output_file}.png")
    
    # Save result
    with open(f"{output_file}.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Results saved to {output_file}.json and {output_file}.png")

if __name__ == '__main__':
    main() 