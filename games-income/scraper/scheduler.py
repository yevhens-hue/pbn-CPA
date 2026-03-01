#!/usr/bin/env python3
"""
Scheduler for games-income.com bonus scraper.
Runs the scraper for all configured GEOs every N hours.

Usage:
    python scheduler.py              # Run once for all GEOs
    python scheduler.py --loop       # Run in loop every 6 hours
    python scheduler.py --export     # Export JSON after scraping
"""

import time
import argparse
import subprocess
import sys
from pathlib import Path

# All GEOs to scrape
ALL_GEOS = ["IN", "UA", "BR"]
INTERVAL_HOURS = 6


def run_for_geo(geo: str, export: bool = False):
    """Run the scraper for a given GEO."""
    print(f"\n{'='*50}")
    print(f"🌍 Starting scrape for GEO: {geo}")
    print(f"{'='*50}")
    cmd = [sys.executable, str(Path(__file__).parent / "bonus_scraper.py"),
           "--geo", geo, "--type", "all"]
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Scraper failed for {geo}")
        return

    if export:
        # Export casino bonuses
        export_cmd = [sys.executable, str(Path(__file__).parent / "bonus_scraper.py"),
                      "--geo", geo, "--export",
                      "--output", f"output/bonuses_{geo.lower()}.json"]
        subprocess.run(export_cmd, capture_output=False)

    print(f"✅ GEO {geo} complete.")


def run_all(export: bool = False):
    """Run scraper for all GEOs sequentially."""
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)

    for geo in ALL_GEOS:
        run_for_geo(geo, export=export)
        time.sleep(5)  # Brief pause between GEOs

    print(f"\n🎉 All GEOs scraped successfully!")


def main():
    parser = argparse.ArgumentParser(description="Bonus Scraper Scheduler")
    parser.add_argument("--loop",   action="store_true", help=f"Loop every {INTERVAL_HOURS}h")
    parser.add_argument("--export", action="store_true", help="Export JSON after each run")
    parser.add_argument("--geo",    default=None, help="Single GEO to run (default: all)")
    args = parser.parse_args()

    if args.loop:
        print(f"⏰ Scheduler started. Running every {INTERVAL_HOURS} hours.")
        while True:
            if args.geo:
                run_for_geo(args.geo.upper(), export=args.export)
            else:
                run_all(export=args.export)
            print(f"\n💤 Next run in {INTERVAL_HOURS} hours...")
            time.sleep(INTERVAL_HOURS * 3600)
    else:
        if args.geo:
            run_for_geo(args.geo.upper(), export=args.export)
        else:
            run_all(export=args.export)


if __name__ == "__main__":
    main()
