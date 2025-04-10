from llmastar.dataset import Dataset

dataset = Dataset(
    root_dir="dataset_sft",
    seed=42,
)
dataset.generate_environment_Astar()
dataset.run_astar_and_add_waypoints(
    waypoint_strategy='intelligent',
    num_waypoints=3,
    save_visualizations=True  # Yellow star waypoints will show critical points near barriers
)

# def main():
#     # Example 1: Basic dataset generation with default settings
#     print("Example 1: Basic dataset generation with default settings")
#     dataset = Dataset(root_dir="sft_dataset", seed=42)
#     dataset.generate_environment_Astar()
#     dataset.add_query_Astar()
    
#     # Example 2: Generate a smaller dataset with custom map sizes and more barriers
#     print("\nExample 2: Custom dataset with more barriers")
#     small_dataset = Dataset(
#         root_dir="small_dataset", 
#         seed=123, 
#         maps=[(30, 20)],  # Smaller maps
#         unique_env=10,     # Fewer environments
#         unique_sg=5        # Fewer start-goal pairs
#     )
#     small_dataset.generate_environment_Astar(
#         horizontal_range=(2, 6),  # More horizontal barriers
#         vertical_range=(2, 6)     # More vertical barriers
#     )
#     small_dataset.add_query_Astar()
    
#     # Example 3: Run A* and generate waypoints with different strategies (with visualizations)
#     print("\nExample 3: Running A* with uniform waypoint sampling (visualized)")
#     uniform_dataset = Dataset(
#         root_dir="uniform_dataset",
#         seed=42,
#         maps=[(40, 30)],
#         unique_env=5,
#         unique_sg=3
#     )
    
#     # Generate environments
#     uniform_dataset.generate_environment_Astar()
    
#     # Run A* with uniform waypoint sampling
#     uniform_dataset.run_astar_and_add_waypoints(
#         waypoint_strategy='uniform',
#         num_waypoints=5,
#         save_visualizations=True  # This will create visualizations with yellow star waypoints
#     )
    
#     # Example 4: Generate another dataset and run A* with intelligent waypoint sampling
#     print("\nExample 4: Intelligent waypoint sampling (visualized)")
#     intelligent_dataset = Dataset(
#         root_dir="intelligent_dataset",
#         seed=42,
#         maps=[(40, 30)],
#         unique_env=5,
#         unique_sg=3
#     )
#     intelligent_dataset.generate_environment_Astar()
#     intelligent_dataset.run_astar_and_add_waypoints(
#         waypoint_strategy='intelligent',
#         num_waypoints=7,
#         save_visualizations=True  # Yellow star waypoints will show critical points near barriers
#     )
    
#     # Example 5: Normal distribution waypoint sampling
#     print("\nExample 5: Normal distribution waypoint sampling (visualized)")
#     normal_dataset = Dataset(
#         root_dir="normal_dataset",
#         seed=42,
#         maps=[(40, 30)],
#         unique_env=5,
#         unique_sg=3
#     )
#     normal_dataset.generate_environment_Astar()
#     normal_dataset.run_astar_and_add_waypoints(
#         waypoint_strategy='normal',
#         num_waypoints=5,
#         save_visualizations=True  # Yellow star waypoints concentrated in the middle of the path
#     )
    
#     print("\nVisualizations have been saved to the respective dataset folders.")
#     print("Three types of visualizations are created for each start-goal pair:")
#     print("1. Basic A* path and visited nodes")
#     print("2. Grid with waypoints as yellow stars")
#     print("3. Full visualization with path, visited nodes, and waypoints")

# if __name__ == "__main__":
#     main()
