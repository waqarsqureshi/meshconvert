#! /usr/bin/env python

# Mesh file format for medit.  See file format description (French only) in
#  http://www.ann.jussieu.fr/~frey/logiciels/Docmedit.dir/Fichiers/formatmesh.pdf

import string, glob, fileinput, posix

def reader(file):
	raise ValueError, "Module "+`__name__`+" does not define a reader method"

def writer(file, reader):
	if not reader.indexed:
		raise RuntimeError, "Cannot convert from non-indexed format to indexed format"
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
			f.write(string.join([nodeIndices[i] for i in e.list])+" "+e.color+"\n")
			elementCounter += 1
	except StopIteration:
		pass

	f.write("""
SubDomainFromMesh
1
3 1 1 1
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

	f = open(file, "w")
	for line in fileinput.input(list):
		f.write(line)
	f.close()

	[posix.remove(f) for f in list]

