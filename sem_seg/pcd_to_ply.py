import os
import re
import numpy as np
import argparse
import sys

'''
script to convert a pcd file into ply

inputs:
 - pcd file

outputs:
 - ply file

execution example:
 - python3 pcd_to_ply.py --path_in "/home/miguel/Escritorio/extract_3d/pointclouds/18_11_2019_all_painted/1_45/pcd" --path_out "/home/miguel/Escritorio/extract_3d/pointclouds/18_11_2019_all_painted/1_45/ply"
'''

def get_header(file):

    header = []
    while True:
        ln = file.readline().strip()
        header.append(ln)
        if ln.startswith(b'DATA'):
            break

    metadata = {}
    for ln in header:
        if ln.startswith(b'#') or len(ln) < 2:
            continue
        match = re.match(b'(\w+)\s+([\w\s\.]+)', ln)
        if not match:
            print("warning: can't understand line: %s" % ln)
            continue
        key, value = match.group(1).lower(), match.group(2)
        if key == b'version':
            metadata[key] = value
        elif key in (b'fields', b'type'):
            metadata[key] = value.split()
        elif key in (b'size', b'count'):
            metadata[key] = map(int, value.split())
        elif key in (b'width', b'height', b'points'):
            metadata[key] = int(value)
        elif key == b'viewpoint':
            metadata[key] = map(float, value.split())
        elif key == b'data':
            metadata[key] = value.strip().lower()

    if b'count' not in metadata:
        metadata[b'count'] = [1] * len(metadata['fields'])
    if b'viewpoint' not in metadata:
        metadata[b'viewpoint'] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    if b'version' not in metadata:
        metadata[b'version'] = b'.7'
    return metadata

def get_data(file):

    data = np.loadtxt(file, delimiter=' ')
    i_del = np.where(np.isnan(data[...,0]))
    data_del = np.delete(data, i_del, 0)
    return data_del



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', help='path to the folder.')
    parser.add_argument('--path_out', help='path to the folder.')
    parsed_args = parser.parse_args(sys.argv[1:])
    
    path_in = parsed_args.path_in  # get prediction folder
    path_out = parsed_args.path_out  # get prediction folder


    for file in sorted(os.listdir(path_in)):

        file_path_in = os.path.join(path_in, file)
        with open(file_path_in, 'rb') as f:

            header = get_header(f)
            data = get_data(f)

        rgb = data[..., 3].astype(int)
        r = (rgb >> 16) & 0x0000ff
        g = (rgb >> 8) & 0x0000ff
        b = (rgb) & 0x0000ff

        r_g_b = np.array([r,g,b]).T

        data = np.delete(data, 3, axis=1)
        data[:, 2] *= -1  # invert z axis

        # create ply
        file_name, file_extension = os.path.splitext(file)
        file_path_out = os.path.join(path_out, file_name + ".ply")
        f = open(file_path_out, 'w')

        f.write("ply" + '\n')
        f.write("format ascii 1.0" + '\n')
        f.write("comment VCGLIB generated" + '\n')
        f.write("element vertex " + str(data.shape[0]) + '\n')
        f.write("property float x" + '\n')
        f.write("property float y" + '\n')
        f.write("property float z" + '\n')
        f.write("property uchar red" + '\n')
        f.write("property uchar green" + '\n')
        f.write("property uchar blue" + '\n')
        f.write("element face 0" + '\n')
        f.write("property list uchar int vertex_indices" + '\n')
        f.write("end_header" + '\n')

        for row in range(data.shape[0]):
            line = ' '.join(map(str, data[row, ...])) + ' ' + ' '.join(map(str, r_g_b[row, ...])) + '\n'
            f.write(line)

        f.close()


if __name__ == "__main__":
    main()
