#!/usr/bin/env python

import sys
import dateutil
from dateutil.parser import parse

EXPECTED = "2022-12-01 16:00:00-06:00"

def check_chicago_offset() -> None:
    """Convert a known UTC instant to America/Chicago and compare to EXPECTED.

    Why fixed string comparison: the bug only manifests as a wrong UTC
    offset/fold result with slim tzdata, so comparing str(result) pins
    down both the wall-clock time and the offset in one assertion.
    """
    utc_time = parse("2022-12-01 22:00:00 UTC")
    local_time = utc_time.astimezone(dateutil.tz.gettz("America/Chicago"))
    actual = str(local_time)

    if actual != EXPECTED:
        # Fail fast with a message that shows both values for quick diagnosis.
        raise AssertionError(
            f"dateutil tz bug present: expected {EXPECTED!r}, got {actual!r}"
        )

    print(f"OK: America/Chicago conversion correct -> {actual}")

if __name__ == "__main__":
    try:
        check_chicago_offset()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
