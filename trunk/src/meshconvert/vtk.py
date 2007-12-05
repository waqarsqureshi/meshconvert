#! /usr/bin/env python

# VTK polydata file format.  References?

import glob, fileinput, posix
import struct
import logging

def reader(file):
	raise ValueError, "Module "+`__name__`+" does not define a reader method"

def writer(file, reader):
	if not reader.indexed:
		raise RuntimeError, "Cannot convert from non-indexed format to indexed format"
	logger=logging.getLogger(__name__)
	#logging.basicConfig(level=logging.DEBUG)
	f = open(file+"-part3", "wb")
	nodeIndices = {}
	nodes = reader.readNode()
	nodeCounter = 0
	try:
		while True:
			n = nodes.next()
			f.write(struct.pack(">3d", float(n.x), float(n.y), float(n.z)))
			nodeIndices[n.label] = nodeCounter
			nodeCounter += 1
	except StopIteration:
		pass
	f.close()

	f = open(file+"-part2", "wb")
	f.write(struct.pack(">I", nodeCounter*8*3))
	f.close()

	f = open(file+"-part5", "wb")
	elements = reader.readElementIndexed()
	elementCounter = 0
	try:
		while True:
			e = elements.next()
			assert e.type == "Tri3"
			[f.write(struct.pack(">I", nodeIndices[i])) for i in e.list]
			elementCounter += 1
	except StopIteration:
		pass
	f.write(struct.pack(">I", elementCounter*4))
	for i in xrange(elementCounter):
		f.write(struct.pack(">I", (i+1)*3))
	f.close()

	f = open(file+"-part4", "wb")
	f.write(struct.pack(">I", elementCounter*4*3))
	f.close()

	f = open(file+"-part1", "wb")
	f.write("""<VTKFile type="PolyData" version="0.1" byte_order="BigEndian">
<PolyData>
<Piece NumberOfPoints="""+'"'+str(nodeCounter)+'" NumberOfPolys="'+str(elementCounter)+'"'+""">
<Points><DataArray type="Float64" NumberOfComponents="3" format="appended" offset="0"/></Points>
""")
	offset = 4+(nodeCounter*8*3)
	f.write('<Polys><DataArray type="Int32" Name="connectivity" format="appended" offset="'+str(offset)+'"/>\n')
	offset += 4+elementCounter*4*3
	f.write('<DataArray type="Int32" Name="offsets" format="appended" offset="'+str(offset)+'"/></Polys>\n')
	offset += 4+elementCounter*4
	f.write('</Piece></PolyData>\n')
	f.write('<AppendedData encoding="raw"> _')
	f.close()

	f = open(file+"-part6", "wb")
	f.write('</AppendedData></VTKFile>\n')
	f.close()

	list = glob.glob(file+"-part[1-6]")
	list.sort()

	f = open(file, "wb")
	for line in fileinput.input(list):
		f.write(line)
	f.close()

	map(posix.remove, list)

