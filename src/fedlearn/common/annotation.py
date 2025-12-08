from __future__ import annotations

from typing import Any

import pandas as pd

# -------------------------------------------------------------------
# Annotation configuration
# -------------------------------------------------------------------
# For each categorical column, we define:
#   - "categories": the canonical category list
#   - "mapping": mapping from raw values -> canonical
# -------------------------------------------------------------------
ANNOTATION_CONFIG: dict[str, dict[str, Any]] = {
    "admissiondx_category": {
        "categories": ["cardiac", "hepatic", "neurologic", "other", "respiratory", "sepsis", "trauma"],
        "mapping": {
            "cardiac": "cardiac",
            "hepatic": "hepatic",
            "neurologic": "neurologic",
            "other": "other",
            "respiratory": "respiratory",
            "sepsis": "sepsis",
            "trauma": "trauma",
        },
    },
    "age_group": {
        "categories": ["elderly", "middle", "older", "young"],
        "mapping": {
            "elderly": "elderly",
            "middle": "middle",
            "older": "older",
            "young": "young",
        },
    },
    "ethnicity": {
        "categories": ["African American", "Asian", "Caucasian", "Hispanic", "Native American", "Other/Unknown"],
        "mapping": {
            "african american": "african",
            "asian": "asian",
            "caucasian": "caucasian",
            "hispanic": "hispanic",
            "native american": "native",
            "other/unknown": "unknown",
        },
    },
    "gender": {
        "categories": ["female", "male", "other", "unknown"],
        "mapping": {
            "f": "f",
            "female": "f",
            "m": "m",
            "male": "m",
            "nb": "other",
            "non-binary": "other",
            "other": "other",
            "unknown": "unknown",
        },
    },
    "hospital_region": {
        "categories": ["Midwest", "Northeast", "South", "West"],
        "mapping": {
            "midwest": "midwest",
            "northeast": "northeast",
            "south": "south",
            "west": "west",
        },
    },
    "hospitaladmitsource": {
        "categories": ["Acute Care/Floor", "Chest Pain Center", "Direct Admit", "Emergency Department", "Floor",
                       "ICU", "ICU to SDU", "Observation", "Operating Room", "Other Hospital", "Other ICU", "PACU",
                       "Recovery Room", "Step-Down Unit (SDU)", "Other"],
        "mapping": {
            "acute care/floor": "acute_care",
            "chest pain center": "cp_center",
            "direct admit": "direct",
            "emergency department": "emergency",
            "floor": "floor",
            "icu": "icu",
            "icu to sdu": "icu_sdu",
            "observation": "observation",
            "operating room": "operating",
            "other hospital": "other_hospital",
            "other icu": "other_icu",
            "pacu": "pacu",
            "recovery room": "recovery",
            "step-down unit (sdu)": "sdu",
            "Other": "other",
        },
    },
    "numbedscategory": {
        "categories": ["<100", "100 - 249", "250 - 499", ">= 500"],
        "mapping": {
            "<100": "low",
            "100 - 249": "lowmid",
            "250 - 499": "highmid",
            ">= 500": "high",
        },
    },
    "teachingstatus": {
        "categories": ["true", "false"],
        "mapping": {
            "true": "1",
            "false": "0",
        },
    },
    "unitadmitsource": {
        "categories": ["Acute Care/Floor", "Chest Pain Center", "Direct Admit", "Emergency Department", "Floor",
                       "ICU", "ICU to SDU", "Observation", "Operating Room", "Other Hospital", "Other ICU", "PACU",
                       "Recovery Room", "Step-Down Unit (SDU)", "Other"],
        "mapping": {
            "acute care/floor": "acute_care",
            "chest pain center": "cp_center",
            "direct admit": "direct",
            "emergency department": "emergency",
            "floor": "floor",
            "icu": "icu",
            "icu to sdu": "icu_sdu",
            "observation": "observation",
            "operating room": "operating",
            "other hospital": "other_hospital",
            "other icu": "other_icu",
            "pacu": "pacu",
            "recovery room": "recovery",
            "step-down unit (sdu)": "sdu",
            "Other": "other",
        },
    },
    "unittype": {
        "categories": ["Cardiac ICU", "CCU-CTICU", "CTICU", "CSICU", "Med-Surg ICU", "MICU", "Neuro ICU", "SICU"],
        "mapping": {
            "cardiac icu": "cardiac",
            "ccu-cticu": "ccu",
            "cticu": "cticu",
            "csicu": "csicu",
            "med-surg icu": "surgery",
            "micu": "micu",
            "neuro icu": "neuro",
            "sicu": "sicu",
        },
    },
}


def _normalize_raw_value(val: Any) -> str | None:
    """
    Normalize raw categorical values to lowercase strings for lookup.
    """
    if val is None:
        return None

    if isinstance(val, str):
        s = val.strip()
        if not s:
            return None
        return s.lower()

    # for non-strings, convert to string then lowercase
    return str(val).strip().lower() or None


def annotate_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply annotation rules to known categorical columns.
    """
    df = df.copy()

    for col, cfg in ANNOTATION_CONFIG.items():
        if col not in df.columns:
            continue  # skip if column not found in dataset

        categories = cfg["categories"]
        mapping = cfg["mapping"]

        # determine fallback category
        fallback = (
            "unknown" if "Unknown" or "unknown" in categories else
            "other" if "Other" or "other" in categories else
            (categories[-1] if categories else "unknown")
        )

        # normalize raw values
        normalized = df[col].map(_normalize_raw_value)

        def map_value(raw_norm: str | None) -> str:
            if raw_norm is None:
                return fallback
            return mapping.get(raw_norm, fallback)

        df[col] = normalized.map(map_value).astype("category")

    return df
