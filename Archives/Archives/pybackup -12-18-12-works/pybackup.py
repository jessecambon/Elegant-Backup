#!/usr/bin/env python
''' 
* Currently the script does not delete folders... ever
* Also, currently only uses xcopy to copy files (would not work on linux for example)
* Does not work for file paths with crazy ASCII characters (currently 
just skips these files using try statement)
'''


import os
#import shutil

#print "Hello"
# Use '/' chars for file paths inside python
# then convert with os.path.normpath() when passing to functions

# works
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

# this is the function that does the backing up
# source = directory we want to back up
# dest = directory we are backing this file up to	
def backup(source,dest):
	command="xcopy /D /E /Y \"" + source + "\" \"" + dest + "\""
	#print command

	# this iterates through all files, same as dir /S /B
	for root, subFolders, files in os.walk(dest):
		
		# iterate through all files
		for x in files:
			filepath= os.path.join(root,os.path.normpath(x))
			source_path= os.path.join(os.path.normpath(source),os.path.relpath(filepath,dest))
			
			# deletes files in dest that are not in source
			if not os.path.exists(source_path):
				print "Deleting: " + filepath
				try:
					os.remove(os.path.normpath(filepath))
				except:
					print "Error, could not delete " + filepath
		
		 #deletes folders in dest that are not in source
			# currently causes error, directory not empty error
			# file not getting removed fast enough?
		'''
		source_folder=os.path.join(os.path.normpath(source),os.path.relpath(root,dest))
		print source_folder
		if not os.path.exists(source_folder):
			print "Delete: " + os.path.normpath(root)
			os.rmdir(os.path.normpath(root))	
		'''
	
	# this does delete folders but doesnt list all subfolders deleted
	'''
	for root, subFolders, files in os.walk(dest):
		source_folder=os.path.join(os.path.normpath(source),os.path.relpath(root,dest))
		#print "Root: " + os.path.normpath(root)
		#print "Source: " + source_folder
		if not os.path.exists(source_folder):
			print "Deleting: " + os.path.normpath(root)
			shutil.rmtree(os.path.normpath(root))
	'''

	# executes xcopy command defined above
	print "\n Copying files... "
	os.system(command)	
	
	
	
cls()

#test cases
#source="C:/Users/fatsheep/Desktop/python_backup/Source 1"
#dest="C:/Users/fatsheep/Desktop/python_backup/Backup Source 1"

#backup(source,dest)

# initalize source and dest as empty lists
source=[]
dest=[]

# read in arguments from targets file
# with statement makes sure file is closed
with open('targets.txt', 'r') as f:
	targets=f.readlines()
	
	for i in targets:
		# doesn't process lines that start with '#'
		# also doesnt process blank lines
		if i.lstrip().startswith("#") or i.lstrip().rstrip() == "":
			pass
		# a backup root variable used to avoid repetition in typing in similar paths...
		# currently this variable is not used
		elif i.lstrip().startswith("BACKUP ROOT:"):
			backup_root=i.lstrip().lstrip("BACKUP ROOT:").lstrip().rstrip()
			print "Backup root:" +backup_root + "|"
		else:
			src, bck = i.split(";")
			#
			# remove trailing and leading white space
			source.append(src.lstrip().rstrip())
			dest.append(bck.lstrip().rstrip())
			
index=0
for x in source:
	#print "Backup: " + x
	#print "dest: " + dest[index]
	backup(x,dest[index])
	index=index+1

