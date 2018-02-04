#!/usr/bin/env python

from glob import glob


def getFilesList(src_dir):
    glob_str = '{}/*.srt'.format(src_dir)
    files = glob(glob_str)
    #files = sorted(files, key=lambda f: int(f.split()[0]))
    files = sorted(files, key=lambda f: int(f.split('/')[-1].split()[0]))
    return files


def process_lines(lines):
    out = []
    state = 'start'
    for n, line in enumerate(lines):
        line = line.strip()
        if line.isdigit():
            continue
        if not line:
            continue
        if ' --> ' in line:
            continue
            
        if state == 'start':
            out.append(line)
        elif state == 'newline':
            out[-1] += '  '
            out.append('  ')
            out.append(line)
        elif state == 'append':
            out[-1] += ' '
            out[-1] += line
        
        if line.endswith('.'):
            state = 'newline'
        else:
            state = 'append'
    return out


if __name__ == '__main__':
    src_dir = './transcripts'
    dst_file = './README.md'

    files = getFilesList(src_dir)

    out = []
    out.append('# INDEX')
    for fname in files:
        noext = fname.split('/')[-1].split('.')[0]
        out.append('* {}'.format(noext))
    out.append('')
    out.append('# CONTENT')
    for fname in files:
        if not 'CONTENT' in out[-1]:
            out[-1] += '  '
            out.append('  ')
        noext = fname.split('/')[-1].split('.')[0]
        out.append('## {}'.format(noext))
        file_lines = open(fname, 'r').readlines()
        file_lines = process_lines(file_lines)
        out.extend(file_lines)

    open(dst_file, 'w').write('\n'.join(out))
