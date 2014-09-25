#!/usr/bin/python

import os
import re
import sys
import fnmatch

class Ensure:

	##- Settings -##

	## Values
	filePath      = None
	outputFile    = None
	wherePattern  = None
	containString = None
	lineValue     = None
        newValue      = None

	## Options
	invertResult  = False
	noop          = False
	verbose       = False
	force         = False
	dedup         = False


	##- Methods  -##

	## Init method
	def __init__(self):
		self.argParse()
		self.sanity()
		self.operateOnFile()

	## Sanity check
	def sanity(self):
		if self.verbose: print('\t[S] File:\t\t\t"%s"'%(self.filePath))
                if self.verbose: print('\t[S] Where:\t\t\t"%s"'%(self.wherePattern))
                if self.verbose: print('\t[S] Containing:\t\t\t"%s"'%(self.containString))
                if self.verbose: print('\t[S] Setting String:\t\t"%s"'%(self.lineValue))
                if self.verbose: print('\t[S] Inverting Selection:\t"%s"'%(self.invertResult))
                if self.verbose: print('\t[S] Non-destructive:\t\t"%s"'%(self.noop))
                if self.verbose: print('\t[S] Verbose:\t\t\t"%s"'%(self.verbose))
		fail = False
		if not os.path.isfile(self.filePath):
			fail = '\t[E] The file "%s" not found.'%(self.filePath)
		if not self.containString == None and not self.wherePattern == None:
			fail = '\t[E] The "contains" directive and the "where" directive cannot be used at the same time.'
		if self.lineValue == None:
			fail = '\t[E] The "line" directive must be set with "--line"'
		if self.outputFile and os.path.isdir(self.outputFile):
			fail = '\t[E] "%s" is a directory.'%(self.outputFile)
		if fail:
			print(fail)
			exit(1)

	## Performs the operation
	def operateOnFile(self):
		with open(self.filePath,"r") as f:
			self.newValue = f.read()
			for line in self.getSelectedLine():
				if not line == '':
					if self.verbose: print('\t[I] Replacing "%s" with "%s"...'%(line,self.lineValue))
					self.newValue = self.newValue.replace(line,self.lineValue)
		if self.dedup:
			self.dedupText()
		if self.outputFile == None:
			print(self.newValue)
		else:
			writeFile = True
			if os.path.isfile(self.outputFile) and not self.force:
				ask = raw_input('The file "%s" exists.  Overwrite? [y/N] '%(self.outputFile))
				if ask.lower() == "y" or ask.lower() == "yes":
					writeFile = True
				else:
					writeFile = False
			if writeFile:
				with open(self.outputFile,"w") as f:
					if self.noop and not self.newValue == "":
						print('\t[N] The file "%s" would have been written to.'%(self.outputFile))
					else:
						f.write(self.newValue)

	## Parse args
	def argParse(self,args = sys.argv):
		i = 0
		while i < len(args):
			arg = args[i]

			## Test for "file"
			if os.path.isfile(arg) and not arg == os.path.basename(__file__):
				self.filePath = arg
			if arg.lower() == "--file" or arg.lower() == "-f":
				self.filePath = args[i+1]

			## Test for output file
			if arg.lower() == "--output" or arg.lower() == "-o":
				self.outputFile = args[i+1]

			## Test for "where"
                        if arg.lower() == "--where" or arg.lower() == "-w":
                                self.wherePattern = args[i+1]

			## Test for "contain"
			if arg.lower() == "--contains" or arg.lower() == "-c" or arg.lower() == "--contain" or arg.lower() == "--has" or arg.lower() == "--with":
				self.containString = args[i+1]

                        ## Test for "line"
                        if arg.lower() == "--line" or arg.lower() == "-l":
                                self.lineValue = args[i+1]

                        ## Test for "noop"
                        if arg.lower() == "--noop" or arg.lower() == "-n" or arg.lower() == "--read-only" or arg.lower() == "-r" or arg.lower() == "--safe" or arg.lower() == "-s":
                                self.noop = True

			## Test for "invert"
			if arg.lower() == "--invert" or arg.lower() == "-i":
				self.invertResult = True

			## Test for verbose
			if arg.lower() == "--verbose" or arg.lower() == "-v":
				self.verbose = True

			## Test for "force"
			if arg.lower() == "--force":
				self.force = True

			## Test for dedup
			if arg.lower() == "--dedup" or arg.lower() == "-d":
				self.dedup = True

			## Increments the iterater
			i += 1

	## Returns line in file where line matches
	def getSelectedLine(self):
		matching = []
		with open(self.filePath, "r") as f:
			lines = f.read().split("\n")
		for line in lines:
			if not self.wherePattern == None:
				if fnmatch.fnmatch(line,self.wherePattern):
					matching.append(line)
			if not self.containString == None:
				if self.containString in line:
					if self.verbose: print('\t[I] Found "%s"'%(line))
					matching.append(line)
		if self.invertResult:
			if self.verbose: print("\t[I] Inverting selection")
			for match in matching:
				lines.remove(match)
			matching = lines
		return(matching)

	## Deduplicates subustitutions
	def dedupText(self):
		#print "Checking target '%s'"%(target)
		target = self.lineValue
		dual = "%s\n%s"%(target,target)
		if dual in self.newValue:
			self.newValue = self.newValue.replace(dual,target)
				


##- Performs the operation -##
e = Ensure()
