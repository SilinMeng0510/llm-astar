import os
import sys
import argparse
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llmastar.pather import AStar, LLMAStar

def parse_args():
    parser = argparse.ArgumentParser(description='LLM-A* with RAG example using intelligent waypoints')
    parser.add_argument('--llm', type=str, default='gpt', choices=['gpt', 'llama', 'qwen'], 
                        help='LLM model to use')
    parser.add_argument('--prompt', type=str, default='standard', choices=['standard', 'cot', 'repe'], 
                        help='Prompt type to use')
    parser.add_argument('--dataset', type=str, default='dataset_sft/environment_50_30.json', 
                        help='Path to the dataset for RAG (containing waypoints_intelligent)')
    parser.add_argument('--output', type=str, default='rag_result.png', 
                        help='Output file path for the result visualization')
    parser.add_argument('--query', type=str, default=None, 
                        help='Query JSON file path')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output for RAG similarity calculations')
    parser.add_argument('--skip-astar', action='store_true',
                        help='Skip A* baseline run')
    parser.add_argument('--skip-llm', action='store_true',
                        help='Skip standard LLM run')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Set debug environment variable if requested
    if args.debug:
        os.environ['RAG_DEBUG'] = '1'
        print("Debug mode enabled")
        
    # Load query from file or use default
    if args.query:
        with open(args.query, 'r') as f:
            query = json.load(f)
    else:
        # Use a default query
        query = {
            "start": [8, 28],
            "goal": [16, 3],
            "range_x": [0, 51], 
            "range_y": [0, 31],
            "horizontal_barriers": [
                [9, 11, 40],
                [13, 2, 13],
                [16, 1, 11]
            ],
            "vertical_barriers": [
                [33, 17, 20]
            ]
        }
    
    results = {}
    
    if not args.skip_astar:
        print("Running A* baseline...")
        astar_result = AStar().searching(query=query, filepath='astar_result.png')
        print(f"A* result: {astar_result}")
        results['A*'] = astar_result
    
    if not args.skip_llm:
        print("Running LLM-A* without RAG...")
        llm_result = LLMAStar(
            llm=args.llm, 
            prompt=args.prompt,
            use_rag=False
        ).searching(query=query, filepath='llm_result.png')
        print(f"LLM-A* result: {llm_result}")
        results['LLM-A*'] = llm_result
    
    print("Running LLM-A* with RAG (using intelligent waypoints)...")
    llm_rag_result = LLMAStar(
        llm=args.llm, 
        prompt=args.prompt,
        use_rag=True,
        dataset_path=args.dataset
    ).searching(query=query, filepath=args.output)
    print(f"LLM-A* with RAG result: {llm_rag_result}")
    results['LLM-A*+RAG'] = llm_rag_result
    
    # Compare results
    print("\nComparison:")
    for name, result in results.items():
        print(f"{name} - Operations: {result['operation']}, Storage: {result['storage']}, Path length: {result['length']}")
    
    # Save results to JSON file
    with open('rag_comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to rag_comparison_results.json")

if __name__ == "__main__":
    main() 