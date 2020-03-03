#!/usr/bin/env python
"""
Tests the functionality of rdams_client.py
"""

import sys
sys.path.append('../src/python/')
import rdams_client as rc




assert rc.add_ds_str('083.2') == 'ds083.2'
assert rc.add_ds_str('ds083.2') == 'ds083.2'


print('All tests succesful')
