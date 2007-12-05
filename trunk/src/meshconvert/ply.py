#! /usr/bin/env python

# PLY file format  http://www.cs.unc.edu/~geom/Powerplant/Ply.doc

import generic
import string

class reader(generic.reader):
	indexed = True

	def __init__(self, file):
		"Opens PLY file for reading"
		generic.reader.__init__(self, file)
		#  Read number of nodes and elements
		line = self.getline()
		assert line == "ply"
		line = self.getline()
		assert line == "format ascii 1.0"
		line = self.getline()
		fields = line.split()
		assert fields[0] == "element" and fields[1] == "vertex"
		self.nrNodes = int(fields[2])
		line = self.getline()
		assert line == "property float x"
		line = self.getline()
		assert line == "property float y"
		line = self.getline()
		assert line == "property float z"
		line = self.getline()
		fields = line.split()
		assert fields[0] == "element" and fields[1] == "face"
		self.nrElements = int(fields[2])
		line = self.getline()
		assert line == "property list uchar int vertex_indices"
		line = self.getline()
		assert line == "end_header"
		self.counterNodes = 0
		self.counterElements = 0
		#logging.basicConfig(level=logging.DEBUG)

	def getline(self):
		"Reads a line from file"
		line = generic.reader.getline(self)
		while line.startswith("comment "):
			line = generic.reader.getline(self)
		return line

	def readNode(self):
		"Gets next node."
		while self.counterNodes < self.nrNodes:
			line = self.getline()
			coord = line.split()
			self.counterNodes += 1
			yield generic.node(coord[0], coord[1], coord[2], label=str(self.counterNodes))

	def readElementIndexed(self):
		"Gets next element"
		while self.counterElements < self.nrElements:
			line = self.getline()
			fields = line.split()
			assert fields[0] == '3'
			fields.pop(0)
			nodeList = [str(string.atoi(i)+1) for i in fields]
			self.counterElements += 1
			yield generic.indexedElement("Tri3", nodeList, label=str(self.counterElements))

def writer(file, reader):
	raise ValueError, "Module "+`__name__`+" does not define a writer method"

