#!/usr/bin/env python

'''
Jesse Cambon
12/20/2012
First backs up all files and folders in source directory specified
(only copies files if they are not the same as determined by filecmp)
then deletes all files and folders in dest not present in source
'''

import os
import shutil
import filecmp
import datetime

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

# backs up file only but only if sourcefile and destfile are different files
# as determined by filecmp.cmp()
def backupfile(sourcefile,destfile):
	if not os.path.exists(destfile) or not filecmp.cmp(sourcefile, destfile):
		try:
			shutil.copy2(sourcefile,destfile)
			print "Copying file: " + sourcefile
			print "To: " + destfile
			log("Copied file " + sourcefile + " to " + destfile, logfile)
		except:
			print "Could not copy file: " + sourcefile
			print "to: " + destfile
			log("ERROR: Could NOT copy file " + sourcefile + " to " + destfile, logfile)
				
	
# backs up files and folders
# uses backupfile function to backup files
def build(source,dest):
	source=os.path.normpath(source)
	dest=os.path.normpath(dest)
	# if source path given is a file, just backup the file
	if os.path.isfile(source):
		backupfile(source,dest)
	
	# if the source specified is the directory then we need to create
	# folders and files
	if os.path.isdir(source):	
		for root, subFolders, files in os.walk(source):
			destpath=os.path.normpath(os.path.join(dest,os.path.relpath(root,source)))
			if not os.path.exists(destpath):
				try:
					os.mkdir(destpath)
					print "Folder created: " + destpath
					log("Folder created: " + destpath, logfile)
				except:
					print "ERROR, folder could not be created: " + destpath
					log("ERROR, folder could not be created: " + destpath, logfile)
			# now copying files in the dir
			for file in files:
				sourcefile=os.path.normpath(os.path.join(root,file))
				destfile=os.path.normpath(os.path.join(dest,os.path.relpath(sourcefile,source)))
				backupfile(sourcefile,destfile)
			
					
# deletes files and folders in backup that shouldn't be there recursively
# iterates through folders from bottom up (longest paths to shortest paths)
# deletes files first and then folders
def destroy(source, dest):
	# only delete stuff if the source is a folder, not a file
	if os.path.isdir(source):
		# False => lists directories bottom up so we can delete them
		for root, subFolders, files in os.walk(dest, False):
			# path for source folder
			sourcepath=os.path.normpath(os.path.join(source,os.path.relpath(root,dest)))
			# path for current dest folder being analyzed
			root=os.path.normpath(root)
			
			# delete files that don't exist in source
			for file in files:
				# path of destination file
				destpath=os.path.normpath(os.path.join(root,file))
				# path of coresponding source file
				sourcefile=os.path.normpath(os.path.join(source,os.path.relpath(destpath,dest)))
				if not os.path.exists(sourcefile):
					try:
						os.remove(destpath)
						print "Deleted file: " + destpath
						log("Deleted file: " + destpath, logfile)
					except:
						print "ERROR: file could not be deleted: " + destpath
						log("ERROR, file could not be deleted: " + destpath, logfile)
			
			# delete the folder if it doesn't exist in source
			if not os.path.exists(sourcepath):
				try:
					os.rmdir(root)
					print "Deleted directory: " + root
					log("Deleted directory: " + root, logfile)
				except:
					print "ERROR, folder could not be deleted: " + root
					log("ERROR, folder could not be deleted: " + root, logfile)

# appends a string (line) to the log file
# as a single line
# works even if log file doesn't originally exist
def log(line,filename):
	log.has_been_called=True
	with open(filename, "a") as f:
		f.write(line + "\n")


# parses the 'targetsfile' and returns the
# source and dest variables in zipped form
def parsefile(targetsfile):
	source=[]
	dest=[]
	with open(targetsfile, 'r') as f:
		filecontent=f.readlines()
		for i in filecontent:
			# doesn't process blank lines or lines that start with '#'
			if not i.lstrip().startswith("#") and not i.lstrip().rstrip() == "":
				src, bck = i.split(";")
				# remove trailing and leading white space
				source.append(src.lstrip().rstrip())
				dest.append(bck.lstrip().rstrip())
	return zip(source,dest)
	
print "Starting backup!"	
log.has_been_called=False

# if copying files, must specify a FILE path for dest, not just folder
#source="C:/Users/fatsheep/Desktop/python_backup/source folder"
#dest="C:/Users/fatsheep/Desktop/python_backup/dest folder"

now = datetime.datetime.now()
logfile="logfile-%d-%d-%d-%d-%d-%d.txt" % (now.month,now.day,now.year,now.hour,now.minute,now.second) 

# Intialize logfile
with open(logfile,"w") as f:
	f.write("PYTHON BACKUP LOGFILE\n")
	f.write("Backup started at: %d/%d/%d %d:%d:%d\n" % (now.month,now.day,now.year,now.hour,now.minute,now.second))
	f.write("The deleting,creation, or copying of any files or folders will be logged below\n")
	f.write("---------------------------------------------\n\n")


cls()
targetsfile="targets.txt"
targets=parsefile(targetsfile)

for source,dest in targets:
	print "source: " + source
	print "dest: " + dest
	build(source,dest)
	destroy(source,dest)


if not log.has_been_called:
	print "No actions taken."
	log("No actions taken.", logfile)

print "\nBackup complete!  View %s for details." %logfile

now=datetime.datetime.now()
log("\nBackup completed successfully on %d/%d/%d at %d:%d:%d" % (now.month,now.day,now.year,now.hour,now.minute,now.second),logfile)