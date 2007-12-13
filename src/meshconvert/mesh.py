#! /usr/bin/env python

# Mesh file format for medit.  See file format description (French only) in
#  http://www.ann.jussieu.fr/~frey/logiciels/Docmedit.dir/Fichiers/formatmesh.pdf

import glob, fileinput, posix
import logging
import generic

class reader(generic.reader):
	indexed = True

	def _section(self, label):
		"Finds a labeled section in file"
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("Searching for section labeled '%s'" % label)
		while True:
			line = self.getline()
			if (line == label):
				return

	def readNode(self):
		"Gets next node"
		self._section("Vertices")
		number = int(self.getline())
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("Mesh contains %d vertices" % number)
		for i in xrange(number):
			line = self.getline()
			coord = line.split()
			yield generic.node(coord[0], coord[1], coord[2], label=str(i+1), color=coord[3])

	def readElementIndexed(self):
		"Gets next element."
		try:
			self._section("Triangles")
		except IOError:
			# EOF reached, reset file
			self.f.seek(0)
			self._section("Triangles")

		number = int(self.getline())
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug("Mesh contains %d triangles" % number)
		for i in xrange(number):
			line = self.getline()
			nodeList = line.split()
			last = nodeList.pop()
			yield generic.indexedElement("Tri3", nodeList, label=str(i+1), color=last)

def writer(file, reader, string=False):
	"Reads mesh from a reader and write it into a MESH file"
	if not reader.indexed:
		raise RuntimeError, "Cannot convert from non-indexed format to indexed format"
	if string:
		out = file
		file = ""
	else:
		out = open(file, "w")

	f = open(file+"-part1", "w")
	f.write("""
MeshVersionFormatted 1

Dimension
3

Geometry
"""+'"'+file+'"'+"""

""")
	f.close()

	f = open(file+"-part3", "w")
	nodeIndices = {}
	nodes = reader.readNode()
	nodeCounter = 0
	try:
		while True:
			n = nodes.next()
			nodeCounter += 1
			nodeIndices[n.label] = str(nodeCounter)
			f.write(n.x+" "+n.y+" "+n.z+" "+n.color+"\n")
	except StopIteration:
		pass
	f.close()

	f = open(file+"-part2", "w")
	f.write("""
Vertices
""")
	f.write(str(nodeCounter)+"\n")
	f.close()

	f = open(file+"-part5", "w")
	elements = reader.readElementIndexed()
	elementCounter = 0
	try:
		while True:
			e = elements.next()
			assert e.type == "Tri3"
			f.write(" ".join([nodeIndices[i] for i in e.list])+" "+e.color+"\n")
			elementCounter += 1
	except StopIteration:
		pass

	f.write("""
SubDomainFromMesh
1
3 1 1 1

End
""")
	f.close()

	f = open(file+"-part4", "w")
	f.write("""
Triangles
""")
	f.write(str(elementCounter)+"\n")
	f.close()

	list = glob.glob(file+"-part[1-5]")
	list.sort()

	for line in fileinput.input(list):
		out.write(line)
	if not string:
		out.close()

	[posix.remove(f) for f in list]

