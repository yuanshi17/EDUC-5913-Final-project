### This Python script reads a .txt file, count things in the file, and output a new txt file
fname= "romeo-full.txt"

# Read the txt file
try:
   fhand = open(fname)
except:
   print("File cannot be opened:", fname)
   quit()

# Define variables to count things
count = 0 # count lines
ROMEO = 0
JULIET = 0
# more variables to count other things

# Loop through each line to count things
for line in fhand:
    line = line.rstrip()
    count = count + 1
    if line == "ROMEO":
       ROMEO += 1
    elif line == "JULIET":
         JULIET += 1

# Create an output.txt file
fout = open('output.txt', 'w')
fout.write(f"Lines of text: {count}\n")
fout.write(f"Romeo: {ROMEO}\n")
fout.write(f"Juliet: {JULIET}\n")

# Close the file
fout.close()
