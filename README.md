# flamapy-mcp: A Flamapy MCP server

## Overview

A Model Context Protocol server for Flamapy operations. This server provides tools to analyze, validate, and interact with UVL (Universal Variability Language) feature models via Large Language Models.

Please note that flamapy-mcp is currently in early development. The functionality and available tools are subject to change and expansion as we continue to develop and improve the server.

### Tools

1.  `atomic_sets`
    -   Identifies atomic sets, which are groups of features that always appear together in all valid configurations.
    -   **Input:**
        -   `content` (string): UVL (universal variability language) feature model content.
    -   **Returns:** A list of lists, where each inner list represents an atomic set of features.

2.  `average_branching_factor`
    -   Calculates the average number of child features per parent feature, indicating model complexity.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The average branching factor as a floating-point number.

3.  `commonality`
    -   Measures the frequency of a feature in valid configurations, expressed as a percentage.
    -   **Inputs:**
        -   `content` (string): UVL feature model content.
        -   `config_file` (string): The name of the feature to calculate commonality for.
    -   **Returns:** The commonality of the specified feature as a float.

4.  `configurations`
    -   Generates all possible valid configurations from the feature model.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of configurations, where each configuration is a dictionary of feature names to their boolean selection state (e.g., `[{'FeatureA': True, 'FeatureB': False}, ...]`).

5.  `configurations_number`
    -   Returns the total number of valid configurations for the feature model.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The total number of valid configurations as an integer.

6.  `core_features`
    -   Identifies features that are present in all valid configurations (mandatory features).
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of core feature names.

7.  `count_leafs`
    -   Counts the number of leaf features (features with no children) in the model.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The number of leaf features as an integer.

8.  `dead_features`
    -   Identifies features that cannot be included in any valid configuration, often indicating model errors.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of dead feature names.

9.  `estimated_number_of_configurations`
    -   Estimates the total number of configurations by considering all feature combinations, ignoring constraints.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The estimated number of configurations as an integer.

10. `false_optional_features`
    -   Identifies features that seem optional but are mandatory due to model constraints.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of false optional feature names.

11. `feature_ancestors`
    -   Returns all ancestor features for a given feature in the model hierarchy.
    -   **Inputs:**
        -   `content` (string): UVL feature model content.
        -   `config_file` (string): The feature name for which to find ancestors.
    -   **Returns:** A list of ancestor feature names.

12. `feature_inclusion_probability`
    -   Calculates the probability of each feature being included in a random valid configuration.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A dictionary mapping each feature to its inclusion probability (e.g., `{'FeatureA': 1.0, 'FeatureB': 0.5}`).

13. `filter`
    -   Filters and selects a subset of configurations based on specified criteria.
    -   **Inputs:**
        -   `content` (string): UVL feature model content.
        -   `config_file` (string): The filtering criteria, formatted as `.csvconf` content.
    -   **Returns:** A list of configurations that match the criteria.

14. `homogeneity`
    -   Measures the similarity of configurations. A higher value (closer to 1) indicates more similar configurations.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The homogeneity score as a float.

15. `leaf_features`
    -   Identifies all leaf features in the model (features with no children).
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of leaf feature names.

16. `max_depth`
    -   Finds the maximum depth of the feature tree, indicating the longest path from root to leaf.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The maximum depth as an integer.

17. `sampling`
    -   Generates a sample of valid configurations from the feature model.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of sample configurations, where each configuration is a dictionary of feature names to their boolean selection state.

18. `satisfiability`
    -   Checks if the feature model is valid and can produce at least one valid configuration.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A boolean indicating if the model is satisfiable.

19. `satisfiable_configuration`
    -   Checks if a given configuration of selected features is valid according to the model's constraints.
    -   **Inputs:**
        -   `content` (string): UVL feature model content.
        -   `selected_features` (List[str]): A list of feature names to be considered 'selected' in the configuration.
    -   **Returns:** A boolean indicating if the configuration is satisfiable.

20. `unique_features`
    -   Identifies features that are part of a unique variability point.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of unique feature names.

21. `variability`
    -   Calculates the ratio of variant features to the total number of features.
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** The variability ratio as a float.

22. `variant_features`
    -   Identifies features that are neither core nor dead (i.e., truly optional).
    -   **Input:**
        -   `content` (string): UVL feature model content.
    -   **Returns:** A list of variant feature names.

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *flamapy-mcp*.

### Using PIP

Alternatively you can install `flamapy-mcp` via pip:

```
pip install flamapy-mcp
```

After installation, you can run it as a script using:

```
python -m flamapy_mcp
```

## Configuration

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "flamapy": {
    "command": "uvx",
    "args": ["flamapy-mcp"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "flamapy": {
    "command": "python",
    "args": ["-m", "flamapy_mcp"]
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "flamapy-mcp": {
    "command": "docker",
    "args": ["run", "--rm", "-i", "mcp/flamapy"]
  }
}
```
</details>

### Usage with VS Code

For quick installation, use one of the one-click install buttons below...

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=flamapy&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22flamapy-mcp%22%5D%7D) [![Install with UV in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-UV-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=flamapy&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22flamapy-mcp%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

```json
{
  "mcp": {
    "servers": {
      "flamapy": {
        "command": "uvx",
        "args": ["flamapy-mcp"]
      }
    }
  }
}
```

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "flamapy-mcp": {
    "command": {
      "path": "uvx",
      "args": ["flamapy-mcp"]
    }
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "flamapy-mcp": {
    "command": {
      "path": "python",
      "args": ["-m", "flamapy_mcp"]
    }
  }
},
```
</details>

### Usage with [Zencoder](https://zencoder.ai)

1. Go to the Zencoder menu (...)
2. From the dropdown menu, select `Agent Tools`
3. Click on the `Add Custom MCP`
4. Add the name (i.e. flamapy) and server configuration from below, and make sure to hit the `Install` button

<details>
<summary>Using uvx</summary>

```json
{
    "command": "uvx",
    "args": ["flamapy-mcp"]
}
```
</details>

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx flamapy-mcp
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Development

If you are doing local development, you can test your changes using the MCP inspector. See [Debugging](#debugging) for run instructions.

## Collaborators

Created in collaboration with the **Laboratorio de Bases de Datos** (Database Lab), [LBD](https://github.com/lbdudc).

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
