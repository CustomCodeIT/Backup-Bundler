#!/usr/bin/python
import os
import sys
import zipfile
from zipfile import ZipFile
import subprocess

def bundleDir(args):

    # Build the directory structure for the archive
    if not os.path.isdir(args[0]):
        print("Could not find path! \"" + os.path.abspath(args[0]) + "\"")
    else:
        filesToCompress = []
        dirsToCompress = []
        outputFile = os.path.abspath(args[1])
        pathToCompress = os.path.basename(os.path.abspath(args[0]))

        for root, dirs, files in os.walk(os.path.abspath(args[0])):
            for d in dirs:
                dirsToCompress.append(os.path.join(root, d))

            for f in files:
                filesToCompress.append(os.path.join(root, f))


        # Compress the directories and files
        with ZipFile(outputFile, 'w', zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=9) as zip:

            for d in dirsToCompress:
                zip.write(d, os.path.join(os.path.basename(os.path.dirname(d)), os.path.basename(d)))

            for f in filesToCompress:
                # If the file is in the root directory we don't need to prepend the path name again.
                if pathToCompress == os.path.basename(os.path.dirname(f)):
                    zip.write(f, os.path.join(os.path.basename(os.path.dirname(f)), os.path.basename(f)))
                else:
                    zip.write(f, os.path.join(pathToCompress, os.path.basename(os.path.dirname(f)), os.path.basename(f)))

        # Encrypt the output
        subprocess.call(["gpg", "--output", outputFile + ".gpg", "--cipher-algo", "AES256", "--symmetric", outputFile])


def main(args):

    commandLength = len(args)
    if commandLength == 0:
        print("You didn't enter a command")
    else:
        actionCommand = args[0]

        # Print the help page
        if actionCommand.lower() == "help":
            print("This is not very helpful")

        # argv should equal 4
        if actionCommand.lower() == "bundledir":
            if commandLength < 2:
                print("Error: bundledir requires directory, outputdir")
            else:
                bundleDir(sys.argv[2:])

if __name__ == "__main__":
    main(sys.argv[1:])