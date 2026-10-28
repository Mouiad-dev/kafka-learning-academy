"""Foundation smoke checks for the Kafka Learning Academy.

Run: python tests/foundation_smoke.py
Uses the Python standard library only.
These checks validate introductory examples, not Kafka/Django integration.
References: https://docs.python.org/3/
"""
import asyncio
import json
import os
import pathlib
import sqlite3
import threading
from urllib.parse import urlsplit
from urllib.request import Request

checks = []

def verify(name, actual, expected):
    assert actual == expected, f"{name}: {actual!r} != {expected!r}"
    checks.append(name)

# F01
verify("F01 arithmetic", 10 + 5, 15)

# F02
verify("F02 working directory", pathlib.Path.cwd().is_dir(), True)

# F03
verify("F03 process ID", isinstance(os.getpid(), int), True)
verify("F03 main thread", threading.current_thread().name, "MainThread")

# F04
verify("F04 number", 2 * 7.5, 15.0)
verify("F04 string type", type("Phone").__name__, "str")

# F05
def describe_order(quantity):
    return "valid" if quantity > 0 else "invalid"
verify("F05 condition", [describe_order(n) for n in (2, 0, -1)],
       ["valid", "invalid", "invalid"])

# F06
order = {"order_id": 105, "items": ["phone", "case"]}
restored = json.loads(json.dumps(order))
verify("F06 JSON", (restored["order_id"], restored["items"][0]),
       (105, "phone"))

# F07
text = "Hello, Sara"
encoded = text.encode("utf-8")
verify("F07 encoding", (type(encoded).__name__, encoded.decode("utf-8")),
       ("bytes", text))

# F08
data = {"order_id": 105}
steps = []
try:
    steps.append(data["customer_id"])
except KeyError:
    steps.append("Missing customer_id")
finally:
    steps.append("Finished this check")
verify("F08 exceptions", steps,
       ["Missing customer_id", "Finished this check"])

# F10
result = []
def show_result(value):
    result.append(value)
def calculate_total(a, b, callback):
    callback(a + b)
calculate_total(5, 7, show_result)
verify("F10 callback", result, [12])

# F11
async def main():
    await asyncio.sleep(0.01)
    return "ready"
verify("F11 async", asyncio.run(main()), "ready")

# F13
address = urlsplit("https://example.com:443/path")
verify("F13 URL", (address.hostname, address.port, address.scheme),
       ("example.com", 443, "https"))

# F14
attempts = 0
visited = []
while attempts < 3:
    attempts += 1
    visited.append(attempts)
    if attempts == 2:
        break
verify("F14 retry loop", visited, [1, 2])

# F15
request = Request("https://example.com/orders/105", method="GET")
verify("F15 HTTP request object", (request.get_method(), request.full_url),
       ("GET", "https://example.com/orders/105"))

# F16
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT)")
    conn.execute("INSERT INTO orders (id,status) VALUES (?,?)", (105,"new"))
    row = conn.execute("SELECT id,status FROM orders").fetchone()
verify("F16 database row", row, (105, "new"))

# F17
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT)")
    conn.execute("INSERT INTO orders VALUES (?,?)", (105, "new"))
    conn.execute("UPDATE orders SET status=? WHERE id=?", ("paid", 105))
    row = conn.execute("SELECT status FROM orders WHERE id=?", (105,)).fetchone()
verify("F17 SQL update", row, ("paid",))

# F18
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY)")
try:
    conn.execute("INSERT INTO orders VALUES (105)")
    conn.execute("INSERT INTO orders VALUES (105)")
    conn.commit()
except sqlite3.IntegrityError:
    conn.rollback()
verify("F18 rollback",
       conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 0)
conn.close()

# F30
verify("F30 throughput arithmetic", 240 / 4, 60.0)

print(f"PASS: {len(checks)} independent foundation smoke checks")
for name in checks:
    print(f"  PASS {name}")
