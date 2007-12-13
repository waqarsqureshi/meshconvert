#! /usr/bin/env python

import unittest
import os, sys
import StringIO

dirname = os.path.dirname(__file__)
if (dirname == ''):
	dirname = '.'
dirname = os.path.realpath(dirname)
parent = os.path.split(dirname)[0]
if parent not in sys.path:
	sys.path.append(parent)

import mesh

class meshTest(unittest.TestCase):
	strTest1 = """
MeshVersionFormatted 1

Dimension
3

Geometry
""


Vertices
3
0 0 0 0
0 0 0 0
0 0 0 0

Triangles
1
1 2 3 1

SubDomainFromMesh
1
3 1 1 1

End
"""
	def test1(self):
		reader = mesh.reader(StringIO.StringIO(self.strTest1), string=True)
		outputString = StringIO.StringIO()
		mesh.writer(outputString, reader, string=True)
		res = outputString.getvalue()
		outputString.close()
		self.assertEquals(res, self.strTest1)

def test_suite():
	tests = [unittest.makeSuite(meshTest)]
	return unittest.TestSuite(tests)

if __name__ == '__main__':
	unittest.main(defaultTest='test_suite')

