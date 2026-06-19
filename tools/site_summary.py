import json
from datetime import datetime
from typing import Dict, List, Optional

# sample site data for summary generation
SITE_DATA: Dict[str, Dict[str, object]] = {
    "hth_main": {
        "url": "https://pro-h5-hth.com",
        "tags": ["sports", "gaming", "hth"],
        "description": "Official hth platform offering live sports and interactive entertainment.",
        "keywords": ["hth", "sports betting", "live games"]
    },
    "hth_help": {
        "url": "https://pro-h5-hth.com/help",
        "tags": ["support", "hth", "faq"],
        "description": "Help center for hth users, including guides and troubleshooting.",
        "keywords": ["hth help", "customer support", "faq"]
    }
}


def format_tags(tag_list: List[str]) -> str:
    """Return a comma-separated string of tags."""
    return ", ".join(tag.strip().lower() for tag in tag_list if tag)


def build_summary_entry(name: str, info: Dict[str, object]) -> Optional[Dict[str, object]]:
    """Create a single summary dictionary from a site entry."""
    required = {"url", "tags", "description", "keywords"}
    if not required.issubset(info.keys()):
        return None
    if not isinstance(info["url"], str) or not info["url"].startswith("http"):
        return None
    return {
        "name": name,
        "url": info["url"],
        "tags": format_tags(info["tags"]),
        "description": str(info["description"]).strip(),
        "keywords": ", ".join(str(k).strip() for k in info["keywords"] if k)
    }


def collect_summaries(data: Dict[str, Dict[str, object]]) -> List[Dict[str, object]]:
    """Iterate over site data and return list of valid summary entries."""
    summaries = []
    for key, entry in data.items():
        summary = build_summary_entry(key, entry)
        if summary:
            summaries.append(summary)
    return summaries


def generate_report(summaries: List[Dict[str, object]]) -> str:
    """Produce a human-readable structured report from summary entries."""
    if not summaries:
        return "No valid site data available."
    lines = []
    lines.append("Site Summary Report")
    lines.append("=" * 50)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total entries: {len(summaries)}")
    lines.append("")
    for idx, entry in enumerate(summaries, start=1):
        lines.append(f"--- Entry {idx} ---")
        lines.append(f"Name       : {entry.get('name', 'unknown')}")
        lines.append(f"URL        : {entry.get('url', 'N/A')}")
        lines.append(f"Tags       : {entry.get('tags', 'none')}")
        lines.append(f"Keywords   : {entry.get('keywords', 'none')}")
        lines.append(f"Description: {entry.get('description', 'none')}")
        lines.append("")
    return "\n".join(lines)


def export_json(summaries: List[Dict[str, object]], indent: int = 2) -> str:
    """Return JSON string of the summary list."""
    return json.dumps(summaries, ensure_ascii=False, indent=indent)


def main() -> None:
    """Entry point: generate and output structured summary."""
    summaries = collect_summaries(SITE_DATA)
    report = generate_report(summaries)
    print(report)
    # also output JSON version as a secondary block
    print("\nJSON representation:")
    print(export_json(summaries))


if __name__ == "__main__":
    main()