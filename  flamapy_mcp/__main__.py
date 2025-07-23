import tempfile
from pathlib import Path
from flamapy.metamodels.configuration_metamodel.models import Configuration
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from fastmcp import FastMCP

# Import both interfaces - facade for simple operations, discover for advanced operations
from flamapy.interfaces.python.flamapy_feature_model import FLAMAFeatureModel
from flamapy.core.discover import DiscoverMetamodels


class UVLContent(BaseModel):
    content: str = Field(description="UVL (universal variability language) feature model content")


class UVLContentWithConfig(BaseModel):
    content: str = Field(description="UVL (universal variability language) feature model content")
    config_file: str = Field(description="Configuration content or parameter (e.g., feature name, list of features).")


class UVLContentWithSimpleConfig(BaseModel):
    content: str = Field(description="UVL (universal variability language) feature model content")
    selected_features: List[str] = Field(
        description="A list of feature names to be considered 'selected' in the configuration.")


mcp = FastMCP(
    name="UVL Analyzer",
    version="1.0.0",
)


def _create_temp_file(content: str, suffix: str = ".uvl") -> str:
    """Create a temporary file with content and return its path"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        return temp_file.name


def _cleanup_temp_file(file_path: str):
    """Clean up temporary file"""
    try:
        Path(file_path).unlink()
    except Exception:
        pass


def _run_facade_operation(content: str, operation_method: str, *args) -> Any:
    """Run operation using the simple facade interface"""
    temp_file = _create_temp_file(content)
    try:
        fm = FLAMAFeatureModel(temp_file)
        method = getattr(fm, operation_method)
        result = method(*args)
        return result
    except Exception as e:
        raise Exception(f"Error executing {operation_method}: {str(e)}")
    finally:
        _cleanup_temp_file(temp_file)


def _run_framework_operation(content: str, operation_name: str, **kwargs) -> Any:
    """Run operation using the core framework interface with optional parameters"""
    temp_file = _create_temp_file(content)
    try:
        dm = DiscoverMetamodels()
        op = dm.use_operation_from_file(operation_name, temp_file)

        # If operation requires execution
        if hasattr(op, 'execute'):
            # Set parameters if any were passed
            for key, value in kwargs.items():
                if hasattr(op, key):
                    setattr(op, key, value)

            op.execute()
            return op.get_result()

        # If result is already final
        return op
    except Exception as e:
        raise Exception(f"Error executing {operation_name}: {str(e)}")
    finally:
        _cleanup_temp_file(temp_file)


@mcp.tool(
    name="atomic_sets",
    description="Identifies atomic sets, which are groups of features that always appear together in all valid configurations."
)
def atomic_sets(input: UVLContent) -> List[List[str]]:
    try:
        return _run_facade_operation(input.content, "atomic_sets")
    except Exception as e:
        raise Exception(f"Failed to compute atomic sets: {str(e)}")


@mcp.tool(
    name="average_branching_factor",
    description="Calculates the average number of child features per parent feature, indicating model complexity."
)
def average_branching_factor(input: UVLContent) -> float:
    try:
        result = _run_facade_operation(input.content, "average_branching_factor")
        return round(float(result), 2)
    except Exception as e:
        raise Exception(f"Failed to compute average branching factor: {str(e)}")


@mcp.tool(
    name="commonality",
    description="Measures the frequency of a feature in valid configurations, expressed as a percentage."
)
def commonality(input: UVLContentWithConfig) -> float:
    try:
        # Use the core framework to get the inclusion probabilities for ALL features.
        all_probabilities = _run_framework_operation(input.content, "FeatureInclusionProbability")

        # Get the specific feature name we are interested in from the input.
        feature_name = input.config_file

        # Look up the probability (commonality) for the requested feature.
        feature_commonality = all_probabilities.get(feature_name)

        # Check if the feature was found in the results. If not, it's an invalid name.
        if feature_commonality is None:
            raise ValueError(f"Feature '{feature_name}' not found in the model or has no commonality value.")

        # The value is already a float (e.g., 0.75), so we can just round it.
        return round(feature_commonality, 2)
    except Exception as e:
        raise Exception(f"Failed to compute commonality: {str(e)}")


@mcp.tool(
    name="configurations",
    description="Generates all possible valid configurations from the feature model."
)
def configurations(input: UVLContent) -> List[Dict[str, bool]]:
    try:
        configs_result = _run_facade_operation(input.content, "configurations")

        serializable_configs = []
        for config in configs_result:
            if isinstance(config, Configuration):
                serializable_configs.append(config.elements)
        return serializable_configs
    except Exception as e:
        raise Exception(f"Failed to generate configurations: {str(e)}")


@mcp.tool(
    name="configurations_number",
    description="Returns the total number of valid configurations for the feature model."
)
def configurations_number(input: UVLContent) -> int:
    try:
        result = _run_framework_operation(input.content, "PySATConfigurationsNumber")
        return int(result)
    except Exception as e:
        raise Exception(f"Failed to count configurations: {str(e)}")


@mcp.tool(
    name="core_features",
    description="Identifies features that are present in all valid configurations (mandatory features)."
)
def core_features(input: UVLContent) -> List[str]:
    try:
        return _run_facade_operation(input.content, "core_features")
    except Exception as e:
        raise Exception(f"Failed to identify core features: {str(e)}")


@mcp.tool(
    name="count_leafs",
    description="Counts the number of leaf features (features with no children) in the model."
)
def count_leafs(input: UVLContent) -> int:
    try:
        result = _run_facade_operation(input.content, "count_leafs")
        return int(result)
    except Exception as e:
        raise Exception(f"Failed to count leaf features: {str(e)}")


@mcp.tool(
    name="dead_features",
    description="Identifies features that cannot be included in any valid configuration, often indicating model errors."
)
def dead_features(input: UVLContent) -> List[str]:
    try:
        return _run_facade_operation(input.content, "dead_features")
    except Exception as e:
        raise Exception(f"Failed to identify dead features: {str(e)}")


@mcp.tool(
    name="estimated_number_of_configurations",
    description="Estimates the total number of configurations by considering all feature combinations, ignoring constraints."
)
def estimated_number_of_configurations(input: UVLContent) -> int:
    try:
        result = _run_facade_operation(input.content, "estimated_number_of_configurations")
        return int(result)
    except Exception as e:
        raise Exception(f"Failed to estimate number of configurations: {str(e)}")


@mcp.tool(
    name="false_optional_features",
    description="Identifies features that seem optional but are mandatory due to model constraints."
)
def false_optional_features(input: UVLContent) -> List[str]:
    try:
        return _run_facade_operation(input.content, "false_optional_features")
    except Exception as e:
        raise Exception(f"Failed to identify false optional features: {str(e)}")


@mcp.tool(
    name="feature_ancestors",
    description="Returns all ancestor features for a given feature in the model hierarchy."
)
def feature_ancestors(input: UVLContentWithConfig) -> List[str]:
    try:
        return _run_facade_operation(input.content, "feature_ancestors", input.config_file)
    except Exception as e:
        raise Exception(f"Failed to get feature ancestors: {str(e)}")


@mcp.tool(
    name="feature_inclusion_probability",
    description="Calculates the probability of each feature being included in a random valid configuration."
)
def feature_inclusion_probability(input: UVLContent) -> Dict[str, float]:
    try:
        result = _run_framework_operation(input.content, "FeatureInclusionProbability")
        return {feature: round(prob, 4) for feature, prob in result.items()}
    except Exception as e:
        raise Exception(f"Failed to compute feature inclusion probability: {str(e)}")


@mcp.tool(
    name="filter",
    description="Filters and selects a subset of configurations based on specified criteria."
)
def filter_features(input: UVLContentWithConfig) -> List[List]:
    config_file = None
    try:
        config_file = _create_temp_file(input.config_file, ".csvconf")
        return _run_facade_operation(input.content, "filter", config_file)
    except Exception as e:
        raise Exception(f"Failed to filter features: {str(e)}")
    finally:
        if config_file:
            _cleanup_temp_file(config_file)


@mcp.tool(
    name="homogeneity",
    description="Measures the similarity of configurations. A higher value (closer to 1) indicates more similar configurations."
)
def homogeneity(input: UVLContent) -> float:
    try:
        result = _run_framework_operation(input.content, "Homogeneity")
        return round(float(result), 4)
    except Exception as e:
        raise Exception(f"Failed to compute homogeneity: {str(e)}")


@mcp.tool(
    name="leaf_features",
    description="Identifies all leaf features in the model (features with no children)."
)
def leaf_features(input: UVLContent) -> List[str]:
    try:
        return _run_facade_operation(input.content, "leaf_features")
    except Exception as e:
        raise Exception(f"Failed to identify leaf features: {str(e)}")


@mcp.tool(
    name="max_depth",
    description="Finds the maximum depth of the feature tree, indicating the longest path from root to leaf."
)
def max_depth(input: UVLContent) -> int:
    try:
        result = _run_facade_operation(input.content, "max_depth")
        return int(result)
    except Exception as e:
        raise Exception(f"Failed to compute max depth: {str(e)}")


# TODO: FIX PROBLEM WHERE configs_result LIST IS EMPTY
@mcp.tool(
    name="sampling",
    description="Generates a sample of valid configurations from the feature model."
)
def sampling(input: UVLContent) -> List[Dict[str, bool]]:
    try:
        return _run_framework_operation(input.content, "Sampling")
    except Exception as e:
        # It's possible the model is invalid and has no configurations, which is not an error.
        if "is a void feature model" in str(e):
            return []  # Return an empty list if no configurations exist.
        raise Exception(f"Failed to generate samples: {str(e)}")


@mcp.tool(
    name="satisfiability",
    description="Checks if the feature model is valid and can produce at least one valid configuration."
)
def satisfiability(input: UVLContent) -> bool:
    try:
        result = _run_facade_operation(input.content, "satisfiable")
        return bool(result)
    except Exception as e:
        raise Exception(f"Failed to check satisfiability: {str(e)}")


@mcp.tool(
    name="satisfiable_configuration",
    description="Checks if a given configuration of selected features is valid according to the model's constraints."
)
def satisfiable_configuration(input: UVLContentWithSimpleConfig) -> bool:
    config_temp_file_path = None
    try:
        config_lines = [f"{feature_name},True" for feature_name in input.selected_features]
        config_content = "\n".join(config_lines)

        # Create the temporary file with the correctly formatted configuration
        config_temp_file_path = _create_temp_file(config_content, suffix=".csvconf")

        # Run the operation using the facade, passing the required 'False' argument
        result = _run_facade_operation(input.content, "satisfiable_configuration", config_temp_file_path, False)

        return bool(result)

    except Exception as e:
        raise Exception(f"Failed to check configuration satisfiability: {str(e)}")
    finally:
        if config_temp_file_path:
            _cleanup_temp_file(config_temp_file_path)


@mcp.tool(
    name="unique_features",
    description="Identifies features that are part of a unique variability point."
)
def unique_features(input: UVLContent) -> List[str]:
    try:
        # Use the core framework with the correct operation name
        return _run_framework_operation(input.content, "UniqueFeatures")
    except Exception as e:
        raise Exception(f"Failed to identify unique features: {str(e)}")


@mcp.tool(
    name="variability",
    description="Calculates the ratio of variant features to the total number of features."
)
def variability(input: UVLContent) -> float:
    try:
        result_tuple = _run_framework_operation(input.content, "Variability")

        # We only need the first element, which is the variability ratio
        variability_ratio = result_tuple[0]

        return round(float(variability_ratio), 2)
    except Exception as e:
        raise Exception(f"Failed to compute variability: {str(e)}")


@mcp.tool(
    name="variant_features",
    description="Identifies features that are neither core nor dead (i.e., truly optional)."
)
def variant_features(input: UVLContent) -> List[str]:
    try:
        return _run_framework_operation(input.content, "VariantFeatures")
    except Exception as e:
        raise Exception(f"Failed to identify variant features: {str(e)}")


if __name__ == "__main__":
    mcp.run(
        transport="http",  # Enables both HTTP + SSE fallback
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
