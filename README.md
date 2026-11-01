# genpark-agentic-commerce-customs-cbp-section-301-china-tariff-exclusion-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

US Customs Section 301 China punitive tariff exclusions, Chapter 99 secondary HTS classification & refund recovery.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_section301_tariff_exclusion`
- **Category**: `agentic_commerce`

### Method Documentation
Audit US import entries for Section 301 China punitive tariff exclusion eligibility (HTS 9903.88.01 - 9903.88.68).
Identifies misclassified entries subject to 25% or 7.5% punitive duties where product scope matches reinstated USTR exclusions,
calculating Post Summary Correction (PSC) duty refunds.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_section301_tariff_exclusion",
    "arguments": {
    "import_entries": [
        {
            "entry_number": "CBP-01",
            "primary_hts": "8414.90.4175",
            "customs_value_usd": 68000.0,
            "section_301_duty_paid_usd": 17000.0
        },
        {
            "entry_number": "CBP-02",
            "primary_hts": "8504.40.9580",
            "customs_value_usd": 42000.0,
            "section_301_duty_paid_usd": 10500.0
        },
        {
            "entry_number": "CBP-03",
            "primary_hts": "7318.15.2000",
            "customs_value_usd": 15000.0,
            "section_301_duty_paid_usd": 3750.0
        }
    ]
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
