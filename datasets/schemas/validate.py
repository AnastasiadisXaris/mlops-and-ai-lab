"""
validate.py — Validate a processed dataset against its JSON schema.

Usage:
    python datasets/schemas/validate.py \\
        --data datasets/synthetic/marketing/marketing-synthetic-conjoint-v1.parquet \\
        --schema datasets/schemas/consumer-conjoint-schema-v1.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd
import pandera as pa
from pandera import Check, Column, DataFrameSchema

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

TYPE_MAP = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
}


def build_pandera_schema(schema_def: dict) -> DataFrameSchema:
    """Build a Pandera DataFrameSchema from a JSON schema definition."""
    columns = {}
    for col in schema_def["columns"]:
        dtype = TYPE_MAP.get(col["type"], object)
        nullable = col.get("nullable", True)
        c = col.get("constraints", {})

        checks = []
        if c.get("min") is not None:
            checks.append(Check.greater_than_or_equal_to(c["min"]))
        if c.get("max") is not None:
            checks.append(Check.less_than_or_equal_to(c["max"]))
        if c.get("allowed_values"):
            checks.append(Check.isin(c["allowed_values"]))
        if c.get("regex"):
            checks.append(Check.str_matches(c["regex"]))

        columns[col["name"]] = Column(dtype, checks=checks, nullable=nullable)

    return DataFrameSchema(columns)


def validate(data_path: str, schema_path: str) -> bool:
    log.info(f"Dataset : {data_path}")
    log.info(f"Schema  : {schema_path}")

    # Load
    df = pd.read_parquet(data_path)
    log.info(f"Shape   : {df.shape}")

    with open(schema_path) as f:
        schema_def = json.load(f)

    log.info(
        f"Validating against schema: {schema_def['name']} v{schema_def['version']}"
    )

    # Build and validate
    schema = build_pandera_schema(schema_def)
    try:
        schema.validate(df, lazy=True)
        log.info("✓ Validation PASSED")
        return True
    except pa.errors.SchemaErrors as e:
        log.error("✗ Validation FAILED")
        log.error(f"\n{e.failure_cases.to_string()}")
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate a dataset against a JSON schema."
    )
    parser.add_argument("--data", required=True, help="Path to parquet dataset")
    parser.add_argument("--schema", required=True, help="Path to JSON schema file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not Path(args.data).exists():
        log.error(f"Dataset not found: {args.data}")
        sys.exit(1)
    if not Path(args.schema).exists():
        log.error(f"Schema not found: {args.schema}")
        sys.exit(1)

    success = validate(args.data, args.schema)
    sys.exit(0 if success else 1)
