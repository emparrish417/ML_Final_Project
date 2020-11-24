#! /usr/bin/python
# -*- coding: utf-8 -*-S
# ====================== UNCLASSIFIED ==================================================================================
# ======================================================================================================================
#  plot_topics.py
#  Emily M. Parrish      30 Aug 2019
#  Major Version:        1
#  Minor Version:        0
#
#  Last Edit: 25 Jun 2019
#
# This program imports Mallet produced topics (with human determined labels) and generates desired visualizations
# using Matplotlib
#
# Python version 3.6
# ======================================================================================================================

import os
import os.path
import time
from pathlib import Path
import platform
import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib.ticker import MultipleLocator
import numpy as np
import calendar

def monthToNum(shortMonth):

    return{
        "01" :'Jan',
        "02" :'Feb',
        "03" :'Mar',
        "04" :'Apr',
        "05" :'May',
        "06" :'Jun',
        "07" :'Jul',
        "08" :'Aug',
        "09" :'Sep',
        "10" :'Oct',
        "11" :'Nov',
        "12" :'Dec'
    }[shortMonth]

def getColor(indx):

    return{
        '0' : "grey",
        '1' : "red",
        '2' : "purple",
        '3' : "yellow",
        '4' : "green",
        '5' : "blue",
        '6' : "red",
        '7' : "orange",
        '8' : "brown",
        '9' : "pink",
        '10' : "yellow",
        '11' : "yellow",
        '12' : "blue"
    }[indx]

def import_topics(importfile):

    datelist = list()
    topiclist = list()
    topicexists = list()
    datasets = list()

    datelist.append("2012-2014")
    for year in range(2015, 2018):
        for month in range(1, 13):
            if month < 10:
                datelist.append("0" + str(month) + "-" + str(year))

            else:
                if month == 10:
                    datelist.append(str(month) + "-" + str(year))
                else:
                    if year == 2017:
                        pass
                    else:
                        datelist.append(str(month) + "-" + str(year))
    datelist.append("Nov-17 to May-18")

    #matrixlist = [[0] * (len(datelist))] * 73
    matrixlist = [datelist]
    matrixlist[0].insert(0, "0")

    with open(importfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        line_count = 0
        for row in csv_reader:
            if row[5] == "Nov-17 to May-18" or row[5] == "2012-2014":
                date = row[5]
            else:
                # month = monthToNum(row[5].split("-")[1])
                # date = month + "-20" + row[5].split("-")[0]
                m = row[5].split("/")[0]
                if int(m) < 10:
                    m = "0" + m
                print(m)
                month = monthToNum(m)
                date = m + "-" + row[5].split("/")[2]


            topicnum = str(int(row[0]))
            topicname = row[1]
            topicCatnum = row[2]
            topicCatname = row[3]
            topicColor = getColor(topicCatnum)
            dp = row[7]

            if topicnum in topicexists:
                for item in datasets:
                    idx = datasets.index(item)
                    if item[1][0] == topicnum:
                        datasets[idx][0].append(date)
                        datasets[idx][1].append(topicnum)

                for sublist in matrixlist:
                    if sublist[0] == topicname:
                        matin = matrixlist[0].index(date)
                        if float(sublist[matin]) > 0:
                            if float(dp) > float(sublist[matin]):
                                sublist[matin] = dp
                            else:
                                pass
                        else:
                            sublist[matin] = dp
            else:
                topicexists.append(topicnum)
                datasets.append([[date],[topicnum],topicname,topicColor,topicCatname])
                topiclist.append(topicname)

                toplist = ["0"] * (len(matrixlist[0])-1)
                toplist.insert(0, topicname)
                matin = matrixlist[0].index(date)
                toplist[matin] = dp
                matrixlist.append(toplist)

    f = open(r'C:\Users\eparrish\Desktop\Sub-Threshold Social Media\C2234_gitrepo\subthreshold\results\Mallet Runs\analysisfiles_EP_07082019\topicmatrix.txt',"w")

    for line in matrixlist:
        print(len(line))
        f.write(",".join(line) + "\n")

    f.close()

    plt.style.use('ggplot')

    # set jupyter's max row display
    pd.set_option('display.max_row', 1000)

    # set jupyter's max column width to 50
    pd.set_option('display.max_columns', 50)

    labels = list()

    fig, ax = plt.subplots()
    cats = list()
    for topic in datasets:
        x = topic[0]
        y = topic[1]
        ax.scatter(x, y, color=topic[3])
        # if topic[4] in cats:
        #     ax.plot(x, y, color=topic[3])
        # else:
        #     if "+" in topic[4]:
        #         ax.plot(x, y, color=topic[3])
        #         cats.append(topic[4])
        #     else:
        #         ax.plot(x, y, color=topic[3], label=topic[4])
        #         cats.append(topic[4])
        labels.append(topic[2])


    plt.yticks(rotation=0, fontsize=7)
    plt.xticks(rotation=90, ha="left", fontsize=7)

    spacing = 10
    minorLocator = MultipleLocator(spacing)
    # Set minor tick locations.
    ax.yaxis.set_minor_locator(minorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    # Set grid to use minor tick locations.
    ax.grid(which='minor')
    fig.canvas.draw()

    ax.set_yticklabels(labels)
    datelist.pop(0)
    print(datelist)
    ax.set_xticklabels(datelist)

    plt.legend(loc="upper left")
    #plt.setp(rotation=-45, ha="left")
    ax.set_alpha(0.8)
    ax.set_title("Topics By Month", fontsize=12)
    ax.set_ylabel("Topic Label", fontsize=12)
    ax.set_xlabel("Date", fontsize=12)

    plt.show()



srcpath = r'C:\Users\eparrish\Desktop\Sub-Threshold Social Media\C2234_gitrepo\subthreshold\results\Mallet Runs\analysisfiles_EP_07082019\alltopics.csv'
import_topics(srcpath)

