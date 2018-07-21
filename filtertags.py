#!env python3
"""Strip POS tags.

Usage: python3 filtertags GZIPPED_INPUT_FILES.. -o OUTPUT
Example input line:

WR-P-E-A-0000005889.p.1.s.1|[ @folia wie VNW(vb,pron,stan,vol,3p,getal) Wie ] [ @folia hebben WW(pv,tgw,met-t) heeft ] [ @folia hier VNW(aanw,adv-pron,obl,vol,3o,getal) hier ] [ @folia geklikt?:p N(soort,ev,basis,zijd,stan) geklikt?:p ]
"""
import re
import sys
import gzip
import getopt

SENTID = re.compile(rb'^[^|]+\|', flags=re.MULTILINE)
TOKEN = re.compile(rb'\[ @folia [^ ]+ [^ ]+ ([^ ]+ )\]|\n')

def main():
	opts, args = getopt.gnu_getopt(sys.argv[1:], 'o:')
	opts = dict(opts)
	with open(opts['-o'], 'ab') as out:
		for fname in args:
			with gzip.open(fname, 'rb') as inp:
				out.writelines(a or b'\n' for a in TOKEN.findall(inp.read()))

if __name__ == '__main__':
	main()
