import os
import re
import argparse
import sys


def get_header(file):
    header = []
    while True:
        ln = file.readline().strip()
        header.append(ln)
        if ln.startswith(b'end'):
            break
    return header


def get_data(file):
    data = []
    while True:
        ln = file.readline()
        if ln == b'':
            break
        data.append(ln)
    return data


def main():

    # python ply_to_txt.py --path_ply ../data_test2/ply/ --path_out ../data_test2/txt #

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_ply', default = 'C:/Users/manue/Desktop/Universidad/DOCTORADO/TEORIA/Point Cloud/pointnet-tuberias/data/data_ply', help='path to the ply dataset folder.')
    parser.add_argument('--path_out', default = 'C:/Users/manue/Desktop/Universidad/DOCTORADO/TEORIA/Point Cloud/pointnet-tuberias/data/data_txt',help='path to the out dataset folder.')
    parsed_args = parser.parse_args(sys.argv[1:])

    path_ply = parsed_args.path_ply
    path_out = parsed_args.path_out

    if not os.path.exists(path_out):
        os.makedirs(path_out)

    for folder in sorted(os.listdir(path_ply)):

        if not os.path.exists(os.path.join(path_out, folder)):
            os.makedirs(os.path.join(path_out, folder))

        for file in sorted(os.listdir(os.path.join(path_ply, folder))):

            if re.search("\.(ply)$", file):  # if the file is a ply

                file_in = os.path.join(path_ply, folder, file)
                name = os.path.splitext(file)[0]
                file_out = os.path.join(path_out, folder, name + '.txt')

                with open(file_in, 'rb') as f:
                    header = get_header(f)
                    data = get_data(f)

                f = open(file_out, 'w')

                for row in data:
                    row = row.decode("utf-8")
                    f.write(row)

        for file in sorted(os.listdir(os.path.join(path_ply, folder, "annotations"))):

            if not os.path.exists(os.path.join(path_out, folder, "annotations")):
                os.makedirs(os.path.join(path_out, folder, "annotations"))

            if re.search("\.(ply)$", file):  # if the file is a ply

                file_in = os.path.join(path_ply, folder, "annotations", file)
                name = os.path.splitext(file)[0]
                file_out = os.path.join(path_out, folder, "annotations", name + '.txt')

                with open(file_in, 'rb') as f:
                    header = get_header(f)
                    data = get_data(f)

                f = open(file_out, 'w')

                for row in data:
                    row = row.decode("utf-8")
                    f.write(row)


if __name__ == "__main__":
    main()
