#!/usr/bin/env python3

from glob import glob
import sys


def getFilesList(src_dir):
    glob_str = f"{src_dir}/*/*.srt"
    files = glob(glob_str)
    #files = sorted(files, key=lambda f: int(f.split()[0]))
    #files = sorted(files, key=lambda f: int(f.split('/')[-1].split()[0]))
    files = sorted(files)
    return files


def splitFiles(files):
    out = {}
    for f in files:
        dot, fd, fn = f.split('/')
        if fd not in out:
            out[fd] = []
        out[fd].append(fn)
    #for fd, fns in out.items():
    #    if len(fns) > 9:
    #        continue
    #    for n, fn in enumerate(fns):
    #        fns[n] = "0" + fn
    return out


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
    src_dir = '.'
    dst_file = './README.md'

    files = getFilesList(src_dir)
    by_dir = splitFiles(files)

    #for f in files:
    #    print(f)

    for fd, fns in by_dir.items():
        print(f"*** {fd} ***")
        for fn in fns:
            print(f"    {fn}")

    out = []
    out.append('# INDEX')
    for fd, files in by_dir.items():
        out.append(f'* {fd}')
        for fname in files:
            noext = fname.split('.')[0]
            out.append(f'  * {noext}')
    out.append('')
    out.append('# CONTENT')
    for fd, files in by_dir.items():
        if not 'CONTENT' in out[-1]:
            out[-1] += '  '
            out.append('  ')
        out.append(f'## {fd}')
        for fname in files:
            if not out[-1].startswith('##'):
                out[-1] += '  '
                out.append('  ')
            noext = fname.split('.')[0]
            fpath = f'./{fd}/{fname}'
            file_lines = open(fpath, 'r').readlines()
            file_lines = process_lines(file_lines)
            out.extend(file_lines)

    open(dst_file, 'w').write('\n'.join(out))
