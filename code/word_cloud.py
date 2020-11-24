# ______________________________________________________________________________________________________________________
# this code is **************************************(U) UNCLASSIFIED***************************************************
# ______________________________________________________________________________________________________________________
# coding=utf-8
# ----------------------------------------------------------------------------------------------------------------------
# program name:         word_cloud
# major version:        1.1
# program purpose:      This program is written to generate word clouds for each topic in a particular month of topic
#                       modelling analysis outputs from MALLET topic-state output file.
# python version:       3.8
#
# Author:               Emily Parrish
# major version created:20200715
# last modification:    20200715 Created all data import functionality and topic sorting functionality
#                       20200717 Added word cloud generation and color mapping for each topic

# ----------------------------------------------------------------------------------------------------------------------

import sys
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from tkinter import *

def generate_word_cloud(zip_path, topic_num=10):
    ''' This function takes in a MALLET topic-state file to generate word cloud files and save them to the input
    directory.'''

    # open file
    f = open(zip_path, 'r', encoding='utf-8')

    # read header lines and store
    labels = f.readline()
    alpha = f.readline()
    beta = f.readline()

    # define dictionary with ten topic keys
    topic_dict = {}

    for i in range(0, int(topic_num)):
        topic_dict[str(i)] = []

    for line in f:
        line_split = line.replace('\n','').split(' ')
        word = line_split[4]
        topic = line_split[5]

        if 'http' in word:
            pass
        else:
            if str(topic) in list(topic_dict.keys()):
                topic_list = topic_dict[topic]
                if topic_list == None:
                    topic_list = [word]
                else:
                    topic_list.append(word)
                topic_dict[topic] = topic_list
            else:
                print('ERROR: Key does not exist.')
                sys.exit()

    color_dict = {'0': 'Reds', '1': 'Greens', '2': 'YlOrBr', '3': 'GnBu', '4': 'PuRd', '5': 'bone', '6': 'GnBu', '7': 'PuRd', '8': 'YlGn', '9': 'bone'}

    for key, val in list(topic_dict.items()):
        source_file = zip_path.split('\\')[-1]
        source_path = zip_path.replace(source_file,'')

        out_path = os.path.join(source_path, source_file.replace('.txt','') + '_wordcloud_topic' + key + '.png')

        counts = Counter(val)
        raw_words = ' '.join(val)

        # Create the wordcloud object
        wordcloud = WordCloud(background_color="white", width=700, height=300, margin=0, colormap=color_dict[key]).generate(raw_words)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.margins(x=0, y=0)
        plt.savefig(out_path)

def main():
    ''' Sprecify source path of MALLET output and topic-state file to generate word clouds from, then call word
    cloud function. '''

    # source_path = r'D:\results_3M\train_LDA_mallet\traingroup_EP_08092019'
    # source_file = r'7-2015_eparrish_20190806\7-2015_eparrish_20190806_topic-state.txt'
    # comb_path = os.path.join(source_path, source_file)

    root = Tk()
    root.filename = filedialog.askopenfilename(title="Select input file")
    print(root.filename)

    generate_word_cloud(root.filename)

if __name__ == '__main__':
    main()

# this code is **************************************(U) UNCLASSIFIED***************************************************