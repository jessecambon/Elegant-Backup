# Elegant Backup

A cross-platform backup script written in python 3 that
mirrors specified folders to a backup destination.
Only files that have been changed since the last backup
will be copied and any files in the destination directory
that do not exist in the source directory are deleted.
A text log is written to document which file operations were
undertaken.