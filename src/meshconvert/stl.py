#! /usr/bin/env python

# STL file format  http://local.wasp.uwa.edu.au/~pbourke/dataformats/stl/

import generic

class reader(generic.reader):
	def readElement(self):
		"Gets next element."
		while True:
			line = self.getline().strip()
			if (line.startswith("solid")):
				break
		while True:
			line = self.getline().strip()
			if (line == "endsolid"):
				return
			assert line.startswith("facet ")
			line = self.getline().strip()
			assert line == "outer loop"
			coord = []
			for i in xrange(3):
				line = self.getline().strip()
				assert line.startswith("vertex ")
				nodeList = line.split()
				nodeList.pop(0)
				coord.append(nodeList)
			line = self.getline().strip()
			assert line == "endloop"
			line = self.getline().strip()
			assert line == "endfacet"
			yield generic.element("Tri3", coord)


def writer(file, reader, string=False):
	"Reads mesh from a reader and write it into a STL file"
	if string:
		out = file
		file = ""
	else:
		out = open(file, "w")

	if reader.indexed:
		nodeCoord = {}
		nodes = reader.readNode()
		nodeCounter = 0
		try:
			while True:
				n = nodes.next()
				nodeCoord[n.label] = (n.x, n.y, n.z)
		except StopIteration:
			pass

		elements = reader.readElementIndexed()
		elementCounter = 0
		out.write("solid\n")
		try:
			while True:
				e = elements.next()
				assert e.type == "Tri3"
				out.write(" facet\n")
				out.write("  outer loop\n")
				for i in xrange(3):
					out.write("   vertex "+" ".join(nodeCoord[e.list[i]])+"\n")
				out.write("  endloop\n")
				out.write(" endfacet\n")
				elementCounter += 1
		except StopIteration:
			pass
		out.write("endsolid\n")
	else:
		elements = reader.readElement()
		out.write("solid\n")
		try:
			while True:
				e = elements.next()
				assert e.type == "Tri3"
				out.write(" facet\n")
				out.write("  outer loop\n")
				for i in xrange(3):
					out.write("   vertex "+" ".join(e.list[i])+"\n")
				out.write("  endloop\n")
				out.write(" endfacet\n")
		except StopIteration:
			pass
		out.write("endsolid\n")

	if not string:
		out.close()

