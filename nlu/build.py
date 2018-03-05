import glob
import os

def create_vocab():
    # What is the name of the final file?
    output_filename = 'data/train.md'

    with open(output_filename, 'w') as outfile:
        print("writing data to " + output_filename)
        write_md("intent", outfile)
        write_md("synonym", outfile)
        write_md("regex", outfile)

def write_md(name, outfile):
    files = glob.glob('vocab/' + name + '/*.md')
    for fname in files:
        print("writing intent " + fname)
        with open(fname) as infile:
            outfile.write("\n\n## " + name + ":" + os.path.basename(fname)[:-3] + "\n");
            outfile.write(infile.read());

if __name__ == '__main__':
    create_vocab()