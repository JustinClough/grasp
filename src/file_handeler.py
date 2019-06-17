import os
import sys

# This class wraps features of file input/output.
# It stores a line by line copy of a file in memory.
class File_Handeler:
    # The full path and name of the file
    full_file_name = ""

    # A list of lines in the file;
    # each line is a string
    file_lines = None

    # Read the file from disk
    # Throws error if it fails
    def read_file( self, dir, name):
        found_file = os.path.isfile( name)
        if not found_file:
            msg = "Cannot find file: " + dir + name + "\n"
            msg+= "Exiting...\n"
            sys.exit( msg)

        file = open( name, "r")
        self.file_lines = file.readlines()
        file.close()

        self.full_file_name  = os.path.join( dir, name)
        return None

    # Get the index of the line with `line_conent`
    def get_index_with( self, line_conent):
        index = self.file_lines.find( line_conent)
        return index

    # Insert content after a given index
    def insert_after( self, index, content):
        self.file_lines.insert( index, content)
        return None

    # Replace the text `look_for` with `replace_with`
    def replace( self, look_for, replace_with):
        counter = 0
        for line in  self.file_lines:
            line = line.replace( look_for, replace_with)
            self.file_lines[counter] = line
            counter += 1
        return None

    # Write the edited file to disk with the same
    # name it was read in from
    def write_file( self):
        file = open( self.full_file_name, "w")
        file.writelines( self.file_lines)
        file.close()
        return None

