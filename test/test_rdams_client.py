#!/usr/bin/env python
"""
Tests the functionality of rdams_client.py
"""

import sys
sys.path.append('../src/')
from gdex_api_client import gdex_client as gc




assert gc.add_ds_str('083.2') == 'ds083.2'
assert gc.add_ds_str('ds083.2') == 'ds083.2'


print('All tests succesful')
