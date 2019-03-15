import os
import sys
from os.path import isdir, isfile, join
import numpy as np
import re


pathdir = '/var/data/Re265_Eivind_Mesh'
n       = [120,70] # grid size


def read_file_prefix(time, field):
    resultFile = open(join(pathdir, time, field))
    content = resultFile.readlines() # read entire file into memory
    resultFile.close()
    return content[:22]


def read_file_postfix(time, field):
    resultFile = open(join(pathdir, time, field))
    content = resultFile.readlines() # read entire file into memory
    resultFile.close()
    npt     = int(content[20])       # number of result points hardcoded to line 21
    return content[22+npt:]


if __name__ == '__main__':
    list_of_number_folders = [d for d in os.listdir('CNN_predictions') if re.match('\d', d)]
    time_steps = sorted(list_of_number_folders, key=lambda x: float(x))
    prefix_u  = read_file_prefix( str(time_steps[15]), 'U')
    postfix_u = read_file_postfix(str(time_steps[15]), 'U')
    prefix_p  = read_file_prefix( str(time_steps[15]), 'p')
    postfix_p = read_file_postfix(str(time_steps[15]), 'p')


    for k,t0 in enumerate(time_steps):
        # print progress info
        print(t0)

        folder = join('CNN_predictions', str(t0))


        U  = np.zeros((120,70,3)) # INPUT YOUR VELOCITY RESULTS ARRAY HERE
        P  = np.zeros((120,70,1)) # INPUT YOUR PRESSURE RESULTS ARRAY HERE


        # write velocity predictions (time series)
        resultFile = open(join(folder, 'V'), 'w')
        resultFile.writelines(prefix_u)
        for j in range(n[1]):
            for i in range(n[0]):
                resultFile.write('('+' '.join(map(str,U[i,j,:]))+')\n')
        resultFile.writelines(postfix_u)
        resultFile.close()

        # write pressure predictions (time series)
        resultFile = open(join(folder, 'q'), 'w')
        resultFile.writelines(prefix_p)
        for j in range(n[1]):
            for i in range(n[0]):
                resultFile.write(str(P[i,j,0])+'\n')
        resultFile.writelines(postfix_p)
        resultFile.close()
