# LLM-A*: LLM-Enhanced Pathfinding Algorithm

This repository contains the implementation of LLM-A*, a novel approach for pathfinding that combines the precision of A* with the contextual understanding of Large Language Models (LLMs).

## Overview

LLM-A* synergistically combines the precise pathfinding capabilities of A* with the global reasoning capability of LLMs. This hybrid approach enhances pathfinding efficiency in terms of time and space complexity while maintaining path validity, especially in large-scale scenarios.

## Features

- **Traditional A* Implementation**: Provides the baseline A* algorithm for pathfinding
- **LLM-A* Implementation**: Enhances A* with LLM-generated path suggestions
- **Multiple LLM Support**: Works with GPT and Llama models
- **Various Prompt Strategies**: Supports standard, chain-of-thought (CoT), and repetition-based prompting
- **RAG Enhancement**: Uses Retrieval-Augmented Generation to improve LLM suggestions based on historical examples

## RAG Implementation

The RAG (Retrieval-Augmented Generation) enhancement leverages historical examples of successful paths to improve the LLM's path suggestions:

1. **Historical Examples**: The system maintains a database of historical barrier configurations and successful paths
2. **Similarity Matching**: When planning a new path, the system retrieves the most similar historical example based on:
   - Barrier configuration (count and placement)
   - Start/goal distance
3. **Enhanced Prompting**: The retrieved example is incorporated into the LLM prompt to guide generation
4. **Descriptive Paths**: Rather than just generating coordinates, the system uses descriptive path reasoning

## Usage

Run the path planning with the following command:

```bash
python -m llmastar.main --algo [a_star|llm_a_star] --llm [gpt|llama] --prompt_type [standard|cot|repe] --query "your query" --use_rag
```

To disable RAG:

```bash
python -m llmastar.main --algo llm_a_star --llm gpt --prompt_type standard --query "your query" --no_rag
```

Query format example:
```
find the shortest path from (5, 5) to (45, 25) on a 51x31 grid, avoiding horizontal barriers at [15, 10-21] and vertical barriers at [20, 0-15], [30, 15-30], and [40, 0-16].
```

## Parameters

- `--algo`: Choose between traditional A* or LLM-A*
- `--llm`: Select which LLM to use (GPT or Llama)
- `--prompt_type`: Choose the prompting strategy
- `--query`: Either a direct query string or path to a query file
- `--use_rag`: Enable RAG enhancement (default is enabled)
- `--no_rag`: Disable RAG enhancement
- `--output_dir`: Directory to save results (default: ./output)

## ⏬ Installation
```bash
pip install llm-astar
```

## 🚀 Quick Start
```