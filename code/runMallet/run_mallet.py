#! /usr/bin/python
# -*- coding: utf-8 -*-S
# ====================== UNCLASSIFIED ==================================================================================
# ======================================================================================================================
#  run_mallet.py
#  Emily M. Parrish      2 May 2019
#  Major Version:        1
#  Minor Version:        0
#
#  Last Edit: 25 Jun 2019
#
# This program performs the import and training functionalities for Mallet in the command line for use in batch runs
# of input file sets.  It also generates custom configuration files off of a base file and stores multiple sets of
# outputs as they are processed in the cluster.
#
# Python version 3.6
# ======================================================================================================================

import os
import os.path
import time
from pathlib import Path
import platform

def import_files(dir, version):
    ''' Function takes in a directory of plain text files and uses the Mallet import command to generate a .mallet
    input to be used for generating and processing batch inputs for parallelization. '''

    print("Version " + version + "of Mallet Running")

    softwarepath = Path(os.path.join('E:/', 'Mallet-' + version))

    # set path to the Mallet in the drive
    os.chdir(softwarepath)

    # define .mallet output files path
    outpath = os.path.join(Path(r'E:\subthreshold\train_LDA_mallet'),dir.split("\\")[-2])
    if outpath == Path(r'E:\subthreshold\train_LDA_date'):
        outpath = os.path.join(Path(r'E:\subthreshold\train_LDA_mallet'),dir.split("\\")[-1])

    if os.path.isdir(outpath) == False:
        os.mkdir(outpath)

    # store user information and date for naming .mallet file
    user = os.environ.get("USERNAME")
    created = time.strftime('%Y%m%d')

    # create output file name
    outfile = str(dir.split("\\")[-1]) + "_" + user + "_" + created + ".mallet"
    output = os.path.join(outpath, outfile)

    # determine operating system to Mallet command appropriate for the os
    opsys = platform.system()

    stoplist = r"E:\Mallet-2.0.8\stoplists\additional_en.txt"
    stoppath = os.path.join(str(softwarepath), stoplist)

    # generate Mallet command
    if opsys == "Windows":
        print("Creating Windows OS Mallet Command")
        import_command = "bin\mallet import-dir --input " + dir + " --output " + output + " --keep-sequence --remove-stopwords --extra-stopwords " + stoplist
        print(import_command)
    else:
        print("Creating Mac OS Mallet Command")
        import_command = "./bin/mallet import-dir --input " + dir + " --output " + output + " --keep-sequence --remove-stopwords --extra-stopwords E:/Mallet/stoplists/additional_en.txt"
        print(import_command)

    # run Mallet command in command line or terminal prompt
    print("Start " + outfile + " upload.")

    os.system(import_command)

    print("End " + outfile + " upload.")

def train_topics(dir, file, version, config_path=Path(r'E:/subthreshold/configs/train.config')):
    ''' Function that runs the train topics command in Mallet.  It takes in parameters using a .config Mallet file
    which, is manipulated by this routine for each run to place output files in the correct directories by creating a
    temporary config file. '''

    print("Version " + version + " of Mallet Running")

    softwarepath = Path(os.path.join('E:/', 'Mallet-' + version))

    filepath = os.path.join(dir,file)

    # set path to the Mallet in the drive
    os.chdir(softwarepath)

    # directory for output files named according to *.mallet file
    newdir = file.replace(".mallet","")

    # temporary config file name to change the paths for the output files
    temp_config = file.replace(".mallet", ".config")
    temp_path = os.path.join(Path(r'E:/subthreshold/configs'), temp_config)

    outdir = os.path.join(dir, newdir)

    if os.path.isdir(outdir) == False:
        os.mkdir(outdir)

    fo_config = open(temp_path, "w")

    # create custom config file with specific paths
    fi_config = open(config_path, "r")
    outcommand = ""
    for line in fi_config:
        if "output" in line:
            parameter = line.split("=")[0].replace(" ","")
            outfile = newdir + "_" + line.split("=")[1].replace(" ","")
            outcommand = outcommand + "--" + parameter + " " + os.path.join(outdir, outfile).replace("\n", " ")

        else:
            fo_config.write(line)

    opsys = platform.system()

    # generate Mallet command
    if opsys == "Windows":
        print("Creating Windows OS Mallet Command: ")
        train_command = "bin\mallet train-topics --input " + filepath + " --config " + str(config_path) + " " + outcommand
        print(train_command)
    else:
        print("Creating Mac OS Mallet Command")
        train_command = "./bin/mallet train-topics --input " + filepath + " --config " + str(config_path)
        print(train_command)

    # close base and custom config files
    fi_config.close()
    fo_config.close()

    # run Mallet command in command line or terminal prompt
    print("Start " + file + " training.")

    os.system(train_command)

    print("End " + file + " training.")

    # delete custom config file after use
    os.remove(temp_path)

def processTopics(path):
    os.chdir(path)
    outfile = open("alltopics2.txt", "w")
    outfile.write("Topic Number,Topic,Category Number, Category,Topic Details,Month,Index,Dirichlet Parameter, Topic Words\n")

    for dirpath, subdir, files in os.walk(path):
        for file in files:
            if "_keys.txt" in file:
                print(file)
                f = open(os.path.join(dirpath,file), "r")
                date = file.split("_")[0]
                for line in f:
                    newline = line.replace("\n","").replace("\t",",")
                    # filedata = line.replace("\n","").split("\t")
                    # ind = filedata[0]
                    # dp = filedata[1]
                    # words = filedata[2]

                    outfile.write(",,,,," + date + "," + newline + "\n")

                f.close()

    outfile.close


version = "2.0.8"

# srcpath = r'E:\subthreshold\train_LDA_date\nov_2017-may_2018'
# for dirpath, subdir, files in os.walk(srcpath):
#     if dirpath != srcpath:
#         import_files(dirpath, version)

#import_files(r'E:\subthreshold\train_LDA_date\nov_2017-may_2018', version)

srcpath = r'E:\subthreshold\train_LDA_mallet\traingroup_EP_08092019'
# for dirpath, subdir, files in os.walk(srcpath):
#     for file in files:
#         print(file)
#         print(file)
#         train_topics(dirpath, file, version)

processTopics(srcpath)