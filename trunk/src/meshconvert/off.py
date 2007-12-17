#! /usr/bin/env python

# OFF file format  http://shape.cs.princeton.edu/benchmark/documentation/off_format.html

import tempfile

def reader(file):
	raise ValueError, "Module "+`__name__`+" does not define a reader method"

def writer(file, reader, string=False):
	"Reads mesh from a reader and write it into a OFF file"
	if not reader.indexed:
		raise RuntimeError, "Cannot convert from non-indexed format to indexed format"
	if string:
		out = file
		file = ""
	else:
		out = open(file, "w")

	tempFiles = [tempfile.TemporaryFile(mode='w+') for i in range(2)]
	tempFiles[0].write("OFF\n")

	nodeIndices = {}
	nodes = reader.readNode()
	nodeCounter = 0
	try:
		while True:
			n = nodes.next()
			nodeIndices[n.label] = str(nodeCounter)
			tempFiles[1].write(n.x+" "+n.y+" "+n.z+"\n")
			nodeCounter += 1
	except StopIteration:
		pass

	tempFiles[0].write(str(nodeCounter)+" ")

	elements = reader.readElementIndexed()
	elementCounter = 0
	try:
		while True:
			e = elements.next()
			tempFiles[1].write(str(len(e.list))+" "+" ".join([nodeIndices[i] for i in e.list])+"\n")
			elementCounter += 1
	except StopIteration:
		pass

	tempFiles[0].write(str(elementCounter)+" 0\n")

	for f in tempFiles:
		f.seek(0)
		while True:
			line = f.readline()
			if line == "":
				break
			out.write(line)
		f.close

	if not string:
		out.close()

