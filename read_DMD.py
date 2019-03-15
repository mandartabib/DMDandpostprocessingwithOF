import os
import sys
from os.path import isdir, isfile, join
import numpy as np
import re

pathdir = '/media/mandart/C/OMAE_2016_2_CYLINDER/Re265_Eivind_Mesh'
n       = [120,70] # grid size


def read_field_from_file(time, field):
    resultFile = open(join(pathdir, time, field))
    content = resultFile.readlines() # read entire file into memory
    resultFile.close()
    npt     = int(content[20])       # number of result points hardcoded to line 21

    # if results are within (), then they are vector values
    if content[22][0] == '(':
        return np.array([np.fromstring(value[1:-1], sep=' ') for value in content[22:22+npt]])
    # else scalar values
    else:
        return np.array([float(value)                        for value in content[22:22+npt]])


def read_input_case(path):
    list_of_number_folders = [d for d in os.listdir(path) if re.match('\d', d)]
    time_steps = sorted(list_of_number_folders, key=lambda x: float(x))

    U   = np.zeros((len(time_steps)-1, n[0], n[1], 3))
    P   = np.zeros((len(time_steps)-1, n[0], n[1], 1))
    ncase = len(time_steps)-2
    print('Reading example ', path, ':[                    ]', end='', flush=True)
    # sys.stdout.flush()
    for i,t in enumerate(time_steps[1:]): # skip t=0 since this only contains meta information
        u = read_field_from_file(t, 'U')
        p = read_field_from_file(t, 'p')
        U[i,:,:,:] = np.reshape(u, (n[0],n[1],3), order='F')
        P[i,:,:,:] = np.reshape(p, (n[0],n[1],1), order='F')
        j = int(i/ncase*20)
        print(''.join(['\b']*21 + ['#']*j + [' ']*(20-j) + [']']), end='', flush=True)
    print()

    t = [float(t) for t in time_steps[1:]]

    return (U,P,t)


if __name__ == '__main__':
    # read the test data from file
    (U,P,t) = read_input_case(pathdir)

    # append the pressure as a solution field
    U = np.append(U, P, axis=3)

    # flatten input so all variables are mashed together (as a vector) for every timestep
    U = np.reshape(U, (len(t), n[0]*n[1]*4))

    # transpose so time is your second axis
    U = U.transpose()

    # check that the dimensions are (33600, 195)
    print(U.shape)
