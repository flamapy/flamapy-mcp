# Flamapy MCP - Feature Model Analysis Tools

This repository provides a comprehensive set of Model Control Protocol (MCP) tools for analyzing feature models using the Universal Variability Language (UVL) format. These tools enable developers and researchers to perform various analyses on software product lines and feature models.

## Overview

Flamapy MCP offers a collection of automated analysis tools that help you understand and validate feature models. Whether you're working with software product lines, variability modeling, or configuration management, these tools provide essential insights into your feature models.

## Available Tools

### Core Analysis Tools

#### 1. **Configurations**
- **Purpose**: Generate all possible valid configurations from a feature model
- **Use Case**: Understanding all possible product variants that can be derived
- **Input**: UVL feature model content
- **Output**: List of all valid feature combinations

#### 2. **Configuration Count**
- **Purpose**: Get the total number of valid configurations
- **Use Case**: Quick assessment of model complexity and variant space size
- **Input**: UVL feature model content
- **Output**: Numerical count of possible configurations

#### 3. **Estimated Configuration Count**
- **Purpose**: Estimate total configurations considering all feature combinations
- **Use Case**: Performance-friendly approximation for very large models
- **Input**: UVL feature model content
- **Output**: Estimated number of configurations

### Feature Analysis Tools

#### 4. **Core Features**
- **Purpose**: Identify mandatory features present in all configurations
- **Use Case**: Finding essential components that cannot be excluded
- **Input**: UVL feature model content
- **Output**: List of features that appear in every valid configuration

#### 5. **Dead Features**
- **Purpose**: Detect features that cannot be included in any valid configuration
- **Use Case**: Identifying modeling errors and unreachable features
- **Input**: UVL feature model content
- **Output**: List of features that are impossible to select

#### 6. **False Optional Features**
- **Purpose**: Find features marked as optional but actually mandatory due to constraints
- **Use Case**: Detecting inconsistencies in feature model design
- **Input**: UVL feature model content
- **Output**: List of seemingly optional but actually required features

#### 7. **Leaf Features**
- **Purpose**: Identify features without child features
- **Use Case**: Finding the most specific options in the product line
- **Input**: UVL feature model content
- **Output**: List of leaf-level features

#### 8. **Feature Ancestors**
- **Purpose**: Find all parent features of a specific feature
- **Use Case**: Understanding feature hierarchy and dependencies
- **Input**: UVL content + target feature name
- **Output**: List of ancestor features

### Structural Analysis Tools

#### 9. **Atomic Sets**
- **Purpose**: Identify groups of features that always appear together
- **Use Case**: Simplifying models by grouping inseparable features
- **Input**: UVL feature model content
- **Output**: Sets of features that behave as single units

#### 10. **Average Branching Factor**
- **Purpose**: Calculate average number of children per parent feature
- **Use Case**: Assessing model complexity and structure balance
- **Input**: UVL feature model content
- **Output**: Numerical average of child features per parent

#### 11. **Maximum Depth**
- **Purpose**: Find the longest path from root to leaf in the feature tree
- **Use Case**: Understanding model hierarchy depth
- **Input**: UVL feature model content
- **Output**: Maximum depth value

#### 12. **Leaf Count**
- **Purpose**: Count total number of leaf features
- **Use Case**: Quick assessment of feature granularity
- **Input**: UVL feature model content
- **Output**: Number of leaf features

### Validation and Filtering Tools

#### 13. **Satisfiability**
- **Purpose**: Check if the feature model is valid and consistent
- **Use Case**: Validating model correctness before analysis
- **Input**: UVL feature model content
- **Output**: Boolean indicating model validity

#### 14. **Commonality**
- **Purpose**: Measure how often features appear across configurations
- **Use Case**: Identifying frequently used vs. rare features
- **Input**: UVL content + configuration parameters
- **Output**: Percentage frequency of feature appearances

#### 15. **Filter**
- **Purpose**: Select configurations meeting specific criteria
- **Use Case**: Narrowing down configuration space based on requirements
- **Input**: UVL content + filter criteria
- **Output**: Filtered subset of configurations