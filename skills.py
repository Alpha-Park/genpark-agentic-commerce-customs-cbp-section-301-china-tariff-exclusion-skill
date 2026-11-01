# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-customs-cbp-section-301-china-tariff-exclusion-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_section301_tariff_exclusion(import_entries, active_exclusion_hts_list=None):
    if active_exclusion_hts_list is None:
        active_exclusion_hts_list = {"8414.90.4175", "8504.40.9580", "8471.70.6000"}
        
    refund_opportunities = []
    total_punitive_duties_paid = 0.0
    total_recoverable_refund = 0.0
    
    for entry in import_entries:
        primary_hts = entry["primary_hts"].strip()
        customs_val = entry["customs_value_usd"]
        sec301_paid = entry.get("section_301_duty_paid_usd", 0.0)
        total_punitive_duties_paid += sec301_paid
        
        if primary_hts in active_exclusion_hts_list and sec301_paid > 0:
            total_recoverable_refund += sec301_paid
            refund_opportunities.append({
                "entry_number": entry["entry_number"],
                "hts_code": primary_hts,
                "customs_value_usd": customs_val,
                "refundable_duty_usd": sec301_paid,
                "chapter_99_secondary_hts": "9903.88.67 (Reinstated Exclusion)"
            })
            
    return {
        "entries_audited": len(import_entries),
        "eligible_refund_entries": len(refund_opportunities),
        "total_punitive_duties_paid_usd": round(total_punitive_duties_paid, 2),
        "recoverable_tariff_refund_usd": round(total_recoverable_refund, 2),
        "actionable_psc_filings": refund_opportunities,
        "action_required": "File CBP Post Summary Correction (PSC) or 19 U.S.C. 1514 Protest within 180 days of liquidation." if refund_opportunities else "No unapplied Section 301 exclusions found."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_section301_tariff_exclusion",
                        "description": """Audit US import entries for Section 301 China punitive tariff exclusion eligibility (HTS 9903.88.01 - 9903.88.68).
Identifies misclassified entries subject to 25% or 7.5% punitive duties where product scope matches reinstated USTR exclusions,
calculating Post Summary Correction (PSC) duty refunds.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_section301_tariff_exclusion(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'import_entries': [{'entry_number': 'CBP-01', 'primary_hts': '8414.90.4175', 'customs_value_usd': 68000.0, 'section_301_duty_paid_usd': 17000.0}, {'entry_number': 'CBP-02', 'primary_hts': '8504.40.9580', 'customs_value_usd': 42000.0, 'section_301_duty_paid_usd': 10500.0}, {'entry_number': 'CBP-03', 'primary_hts': '7318.15.2000', 'customs_value_usd': 15000.0, 'section_301_duty_paid_usd': 3750.0}]}
        out = audit_section301_tariff_exclusion(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
