import glob
import os

def write_config_data(config_file, outfile):
    with open(config_file) as infile:
        outfile.write(infile.read())

def write_intent_data(data_dir, outfile):
    outfile.write('\n# data - this is the combined .md files\n\n')
    outfile.write('data: |')
    
    files = glob.glob('data/*.md')
    for fname in files:
        with open(fname, newline = '\n') as infile:
            outfile.write('\n')
            for line in infile.readlines():
                outfile.write('  ' + line)

def create_train_file(config_file, train_file, data_dir):
    with open(train_file, 'w') as outfile:
        write_config_data(config_file, outfile)
        write_intent_data(data_dir, outfile)   

if __name__ == '__main__':
    create_train_file('config.yml','train_md.yml', 'data_dir')
