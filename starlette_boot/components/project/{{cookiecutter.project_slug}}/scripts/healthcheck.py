#!/usr/bin/env python

import http.client
import sys

conn = http.client.HTTPConnection("localhost:8000", timeout=3)
conn.request("GET", "/health")
response = conn.getresponse()
assert response.status == 200
sys.stderr.write("healthy")
