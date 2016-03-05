# Script to pickle json data automatically
# Should only work with tables created with Apache drill since they have a different format
# Usage:
# 
# python path\to\json_to_pickle.py path\to\json_file.json
import json
import re
import os
import sys
import pandas as pd
from pandas.io.json import json_normalize

#shameless copy paste from json/decoder.py
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

if len(sys.argv)> 1:
	filename = sys.argv[1]
	pkl_file = os.path.splitext(filename)[0] + '.pkl'
	with open(filename) as f:
		json_data = json.load(f, cls=ConcatJSONDecoder)
	df = json_normalize(json_data)
	df.to_pickle(pkl_file)
	print 'JSON data saved as' + pkl_file

else:
	filename = 'C:\path\to\json'
	pkl_file = os.path.splitext(filename)[0] + '.pkl'
	with open(filename) as f:
		json_data = json.load(f, cls=ConcatJSONDecoder)
	df = json_normalize(json_data)
	df.to_pickle(pkl_file)
	print 'JSON data saved as' + pkl_file
