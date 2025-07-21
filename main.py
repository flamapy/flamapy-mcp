import os
import tempfile
import json
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from flamapy.metamodels.configuration_metamodel.models import Configuration
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union

from fastmcp.server import FastMCP

# Import both interfaces - facade for simple operations, discover for advanced operations
from flamapy.interfaces.python.flamapy_feature_model import FLAMAFeatureModel
from flamapy.core.discover import DiscoverMetamodels


class UVLContent(BaseModel):
    content: str = Field(description="UVL (universal variability language) feature model content")


class UVLContentWithConfig(BaseModel):
    content: str = Field(description="UVL (universal variability language) feature model content")
    config_file: str = Field(description="Configuration parameter (feature name, filter criteria, etc.)")


mcp = FastMCP(
    name="UVL Analizer",
    version="1.0.0",
)


def _create_temp_file(content: str) -> str:
    """Create a temporary file with UVL content and return its path"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".uvl") as temp_file:
        temp_file.write(content)
        return temp_file.name


def _cleanup_temp_file(file_path: str):
    """Clean up temporary file"""
    try:
        Path(file_path).unlink()
    except Exception:
        pass


def _run_facade_operation(content: str, operation_method: str) -> Any:
    """Run operation using the simple facade interface"""
    temp_file = _create_temp_file(content)
    try:
        fm = FLAMAFeatureModel(temp_file)
        return getattr(fm, operation_method)()
    finally:
        _cleanup_temp_file(temp_file)


def _run_framework_operation(content: str, operation_name: str) -> Any:
    """Run operation using the framework interface"""
    temp_file = _create_temp_file(content)
    try:
        dm = DiscoverMetamodels()
        return dm.use_operation_from_file(operation_name, temp_file)
    finally:
        _cleanup_temp_file(temp_file)


@mcp.tool(
    name="atomic_sets",
    description="This operation identifies atomic sets in a feature model. "
                "An atomic set is a group of features that always appear together across "
                "all configurations of the model. These sets help in simplifying and reducing "
                "the complexity of the model by grouping features that behave as a single unit."
)
def atomic_sets(input: UVLContent) -> List[List[str]]:
    return _run_facade_operation(input.content, "atomic_sets")


@mcp.tool(
    name="average_branching_factor",
    description="This calculates the average number of child features per parent "
                "feature in the feature model. It provides insight into the complexity of the model."
)
def average_branching_factor(input: UVLContent) -> float:
    result = _run_facade_operation(input.content, "average_branching_factor")
    return round(float(result), 2)


@mcp.tool(
    name="commonality",
    description="Measures how often a feature appears in the configurations of a product line, "
                "usually expressed as a percentage. Features with high commonality are core features."
)
def commonality(input: UVLContentWithConfig) -> float:
    temp_file = _create_temp_file(input.content)
    try:
        fm = FLAMAFeatureModel(temp_file)
        # The commonality operation typically requires a feature name
        result = fm.commonality(input.config_file)
        return round(float(result), 2)
    finally:
        _cleanup_temp_file(temp_file)


@mcp.tool(
    name="configurations",
    description="Generates all possible valid configurations of a feature model. "
                "Each configuration represents a valid product that can be derived from the "
                "feature model."
)
def configurations(input: UVLContent) -> List[Dict[str, bool]]:
    return _run_facade_operation(input.content, "configurations")


@mcp.tool(
    name="configurations_number",
    description="Returns the total number of valid configurations represented by "
                "the feature model."
)
def configurations_number(input: UVLContent) -> int:
    # Use the facade method for number of configurations
    result = _run_facade_operation(input.content, "count_configurations")
    return int(result)


@mcp.tool(
    name="core_features",
    description="Identifies features that are present in all valid configurations "
                "of the feature model. These are mandatory features that cannot be excluded."
)
def core_features(input: UVLContent) -> List[str]:
    return _run_facade_operation(input.content, "core_features")


@mcp.tool(
    name="count_leafs",
    description="This operation counts the number of leaf features in a feature model. "
                "Leaf features are those that do not have any children."
)
def count_leafs(input: UVLContent) -> int:
    result = _run_facade_operation(input.content, "count_leafs")
    return int(result)


@mcp.tool(
    name="dead_features",
    description="Identifies features that cannot be included in any valid product "
                "configuration due to constraints and dependencies in the model. "
                "These are typically indicative of errors in the feature model."
)
def dead_features(input: UVLContent) -> List[str]:
    return _run_facade_operation(input.content, "dead_features")


@mcp.tool(
    name="estimated_number_of_configurations",
    description="Provides an estimate of the total number of different configurations "
                "that can be produced from a feature model by considering all possible combinations "
                "of features."
)
def estimated_number_of_configurations(input: UVLContent) -> int:
    result = _run_facade_operation(input.content, "estimated_number_of_configurations")
    return int(result)


@mcp.tool(
    name="false_optional_features",
    description="Identifies features that appear to be optional but, due to constraints "
                "and dependencies in the feature model, must be included in every valid product "
                "configuration. These features are typically indicative of modeling errors."
)
def false_optional_features(input: UVLContent) -> List[str]:
    return _run_facade_operation(input.content, "false_optional_features")


@mcp.tool(
    name="feature_ancestors",
    description="Identifies all ancestor features of a given feature in the feature model. "
                "Ancestors are features that are hierarchically above the given feature."
)
def feature_ancestors(input: UVLContentWithConfig) -> List[str]:
    temp_file = _create_temp_file(input.content)
    try:
        fm = FLAMAFeatureModel(temp_file)
        # Feature ancestors typically requires a feature name
        return fm.feature_ancestors(input.config_file)
    finally:
        _cleanup_temp_file(temp_file)


@mcp.tool(
    name="filter",
    description="This operation filters and selects a subset of configurations based on "
                "specified criteria. It helps in narrowing down the possible configurations to "
                "those that meet certain requirements."
)
def filter_features(input: UVLContentWithConfig) -> list[Configuration] | None:
    temp_file = _create_temp_file(input.content)
    try:
        fm = FLAMAFeatureModel(temp_file)
        # Filter operation - the config_file should contain the filter criteria
        # This might need to be implemented differently based on Flamapy's filter API
        return fm.filter(input.config_file)
    finally:
        _cleanup_temp_file(temp_file)


@mcp.tool(
    name="leaf_features",
    description="Identifies all leaf features in the feature model. "
                "Leaf features are those that do not have any child features and represent "
                "the most specific options in a product line."
)
def leaf_features(input: UVLContent) -> List[str]:
    return _run_facade_operation(input.content, "leaf_features")


@mcp.tool(
    name="max_depth",
    description="This operation finds the maximum depth of the feature tree in the model, "
                "indicating the longest path from the root to a leaf."
)
def max_depth(input: UVLContent) -> int:
    result = _run_facade_operation(input.content, "max_depth")
    return int(result)


@mcp.tool(
    name="satisfiability",
    description="Checks whether a given model is valid according to the constraints "
                "defined in the feature model."
)
def satisfiability(input: UVLContent) -> bool:
    # Use 'satisfiable' method name as shown in documentation
    result = _run_facade_operation(input.content, "satisfiable")
    return bool(result)


if __name__ == "__main__":
    mcp.run(
        transport="http",  # Enables both HTTP + SSE fallback
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
