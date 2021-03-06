#!/usr/bin/env python

'''
image_diversity.py
Written by Jeff Berry on Dec 21 2010

purpose:
    This script measures the distance from average for each image in the
    input set, and copies the specified number of highest scoring images
    to a new folder called 'diverse'. If ROI_config.txt is present in the 
    same folder as the input images, the ROI in that file will be used to 
    do the measurement. If not present, it will use a hard-coded default ROI.

usage:
    python image_diversity.py <num_images> <num_testset> <num_batches>
    
parameters:
    <num_images>: The number of images to use in the diverse set. This number
            represents the most diverse images. The script will automatically 
            add the 50 least diverse images to the set.
    <num_testset>: The number of images to save out of the diverse set as a 
            test set. These images will be stored in 'diverse-test'.
    <num_batches>: The number of groups to organize the remaining images into
            
example:
    python image_diversity.py 300 100 5
    #This command will result in 250 images in 'diverse' and 100 test images
    #in 'diverse-test'. The remaining images will be split into 5 groups in
    #'batch1', 'batch2', etc.
    
---------------------------------------------
Modified by Jeff Berry on Feb 18 2011
reason:
    Updated the script to use ROI_config.txt. This made the initial ROI selection
    window unnecessary. ROI is now selected using SelectROI.py
---------------------------------------------
Modified by Jeff Berry on Feb 25 2011
reason:
    added support for unique tracer codes on .traced.txt files
---------------------------------------------
Modified by Jeff Berry on Jan 26 2012
reason:
    added support for splitting diverse images into train and test sets. The script
    is no longer interactive due to problems with the raw_input() function interacting 
    with GTK. Instead, the numbers of train and test images are passed to the script
    as arguments (see usage above). 
'''

import cv
import os, sys
import operator
import subprocess
from numpy import *
import matplotlib.pyplot as plot
import gtk
import multiprocessing

CopyQueue = multiprocessing.Queue()
FinishQueue = multiprocessing.Queue()

class CopyThread(multiprocessing.Process):        
    def run(self):
        flag = 'ok'
        while (flag != 'stop'):
            cmd = CopyQueue.get()
            if cmd == None:
                flag = 'stop'
            else:
                #print ' '.join(cmd)
                p = subprocess.Popen(cmd)
                p.wait()
                FinishQueue.put(cmd)
        #print "CopyThread stopped"

class ImageWindow:
    def __init__(self, n, n_test, n_batches, add_lower50='y', make_testset='y'):
        self.onOpen()
        self.makeDest()
        self.get_tracenames()

        # get an image and open it to see the size
        img = cv.LoadImageM(self.datafiles[0], iscolor=False)
        self.csize = shape(img)
        self.img = asarray(img)
        
        #open up the ROI_config.txt and parse
        self.pathtofiles = '/'.join(self.datafiles[0].split('/')[:-1]) + '/'
        self.config = self.pathtofiles + 'ROI_config.txt'
        if (os.path.isfile(self.config)):
            print "Found ROI_config.txt"
            c = open(self.config, 'r').readlines()
            self.top = int(c[1][:-1].split('\t')[1])
            self.bottom = int(c[2][:-1].split('\t')[1])
            self.left = int(c[3][:-1].split('\t')[1])
            self.right = int(c[4][:-1].split('\t')[1])
            print "using ROI: [%d:%d, %d:%d]" % (self.top, self.bottom, self.left, self.right)
        else:
            print "ROI_config.txt not found"
            self.top = 140 #default settings for the Sonosite Titan
            self.bottom = 320
            self.left = 250
            self.right = 580
            print "using ROI: [%d:%d, %d:%d]" % (self.top, self.bottom, self.left, self.right)
        
        roi = img[self.top:self.bottom, self.left:self.right]
        self.roisize = shape(roi)
        
        self.get_diverse(n, n_test, n_batches, add_lower50, make_testset)
   
    def onOpen(self):
        fc = gtk.FileChooserDialog(title='Open Image Files', parent=None, 
            action=gtk.FILE_CHOOSER_ACTION_OPEN, 
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        g_directory = fc.get_current_folder() if fc.get_current_folder() else os.path.expanduser("~")
        fc.set_current_folder(g_directory)
        fc.set_default_response(gtk.RESPONSE_OK)
        fc.set_select_multiple(True)
        ffilter = gtk.FileFilter()
        ffilter.set_name('Image Files')
        ffilter.add_pattern('*.jpg')
        ffilter.add_pattern('*.png')
        fc.add_filter(ffilter)
        response = fc.run()
        if response == gtk.RESPONSE_OK:
            self.datafiles = fc.get_filenames()
            g_directory = fc.get_current_folder()
        fc.destroy()

    def makeDest(self):
        s = self.datafiles[0].split('/')
        self.rootdir = '/'.join(s[:-1]) + '/'
        self.destpath = '/'.join(s[:-1]) + '/diverse/'
        print "images will be saved in", self.destpath
        if not os.path.isdir(self.destpath):
            os.mkdir(self.destpath)
            print "created directory", self.destpath

    def get_tracenames(self):
        '''This method will look for existing trace files and create a dictionary to corresponding
        image files. It will only work if all image files are in the same directory
        '''
        self.tracenames = {}
        tracedir = '/'.join(self.datafiles[0].split('/')[:-1])+ '/'
        files = os.listdir(tracedir)
        traces = []
        for i in files:
            if ('traced.txt' in i):
                traces.append(tracedir+i)

        for i in self.datafiles:
            for j in traces:
                if i in j:
                    self.tracenames[i] = j


    def get_average_image(self):
        files = self.datafiles        
        ave_img = zeros(self.roisize)
        for i in range(len(files)):
            img = cv.LoadImageM(files[i], iscolor=False)
            roi = img[self.top:self.bottom, self.left:self.right]
            roi = asarray(roi)/255.
            ave_img += roi
        ave_img /= len(files)    
    
        return ave_img, files
    
    def get_diverse(self, n, n_test, n_batches, add_lower50='y', make_testset='y'):
        '''gets the n most diverse images from the data set and copies them into path_to_save'''
        if os.path.isdir(self.destpath):
            print "calculating average image"
            ave_img, files = self.get_average_image()
        
            print "measuring distances from average"
            results = {}
            for i in range(len(files)):
                img = cv.LoadImageM(files[i], iscolor=False)
                roi = img[self.top:self.bottom, self.left:self.right]
                roi = asarray(roi)/255.
                dif_img = abs(roi - ave_img)
                results[files[i]] = sum(sum(dif_img))
        
            sorted_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)

            #show rank vs. energy plot
            count = 1
            for (i,j) in sorted_results:
                plot.plot(count, j, 'b.')
                count += 1
            plot.savefig(self.destpath+'rankVenergy.png')
            #plot.show()
            
            #cmd = ['open', self.destpath+'rankVenergy.png']
            #p = subprocess.Popen(cmd)

            #n = int(raw_input("Enter number of images to move: "))
            #print n # for some reason, these raw_input calls don't work anymore
        
            #add_lower50 = raw_input("Should I also add the 50 least different images? [Y/n]: ")
        
            #make_testset = raw_input("Should I save out some images as a test set? [Y/n]: ")
            if (make_testset == '') or (make_testset.lower() == 'y'):
                TESTSET = True
                #n_test = int(raw_input("Enter the number of test images to save out: "))
                self.testdir = self.destpath[:-1]+'-test/'
                if not os.path.isdir(self.testdir):
                    os.mkdir(self.testdir)
            else:
                TESTSET = False
                #n_test = 0
            
            numThreads = 4
            for i in range(numThreads):
                thread = CopyThread()
                thread.start()
            
            filenames = []
            for (i,j) in sorted_results[:n]:
                filenames.append(i)

            if (add_lower50 == '') or (add_lower50.lower() == 'y'):
                for (i,j) in sorted_results[-50:]:
                    filenames.append(i)
            filenames = array(filenames)    
            if TESTSET:
                inds = arange(len(filenames))    
                random.shuffle(inds)
                testinds = inds[:n_test]
                traininds = inds[n_test:]
                trainfiles = filenames[traininds]
                testfiles = filenames[testinds]
            else:
                trainfiles = filenames
            
            count = 0   
            print "saving most diverse images to:", self.destpath
            for i in trainfiles:
                fname = i.split('/')[-1]
                cmd = ['mv', i, self.destpath+fname]
                #print count
                count += 1
                CopyQueue.put(cmd)
                if self.tracenames.has_key(i):
                    cmd2 = ['mv', self.tracenames[i], self.destpath]
                    count += 1
                    CopyQueue.put(cmd2)
                    
            if TESTSET:
                for i in testfiles:
                    fname = i.split('/')[-1]
                    cmd = ['mv', i, self.testdir+fname]
                    CopyQueue.put(cmd)
                    #print count
                    count += 1
                    if self.tracenames.has_key(i):
                        cmd2 = ['mv', self.tracenames[i], self.testdir]
                        count += 1
                        CopyQueue.put(cmd2)
                 
            remaining = []
            for (i,j) in sorted_results[n:-50]:
                remaining.append(i)
            remaining = array(remaining)
            inds = arange(len(remaining))
            random.shuffle(inds)
            breaks = linspace(0, len(remaining), n_batches+1).astype(integer)
            for i in range(n_batches):
                batch_inds = inds[breaks[i]:breaks[i+1]]
                batch_files = remaining[batch_inds]
                batch_dir = "batch%03d" % (i+1)
                dest = os.path.join(self.rootdir, batch_dir)
                if not os.path.isdir(dest):
                    os.mkdir(dest)
                for j in batch_files:
                    fname = j.split('/')[-1]   
                    cmd = ['mv', j, os.path.join(dest, fname)]
                    count += 1
                    CopyQueue.put(cmd)
                    if self.tracenames.has_key(j):
                        cmd2 = ['mv', self.tracenames[j], dest]
                        count += 1
                        CopyQueue.put(cmd2)

            # stop the threads
            for i in range(numThreads):               
                CopyQueue.put(None)               

            # write sorted_results to a .txt file for future reference
            # added Mar 10 2011 by Jeff Berry
            o = open(self.destpath+'SortedResults.txt', 'w')
            for (i,j) in sorted_results:
                o.write("%s\t%.4f\n" %(i, j))
            o.close()

        for i in range(count):
            Fcmd = FinishQueue.get()
            print ' '.join(Fcmd)    

    
        print "done"
        roifile = '/'.join(self.datafiles[0].split('/')[:-1]) + '/ROI_config.txt'
        if os.path.isfile(roifile):
            p = subprocess.Popen(['cp', roifile, self.destpath])
            p.wait()
        #p = subprocess.Popen(['rm', self.destpath+'/rankVenergy.png'])
        #p.wait()
 
        try:    
            gtk.main_quit() #for some reason this is not exiting gracefully
        except RuntimeError:
            #print "press ctrl+c to quit"
            p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['grep', '-i', 'image_diversity'], stdin=p1.stdout, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(['awk', "{print $2}"], stdin=p2.stdout, stdout=subprocess.PIPE)
            pid = p3.communicate()[0][:-1]
            print pid
            p = subprocess.Popen(['kill', pid])

            
if __name__ == "__main__":
    ImageWindow(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    gtk.main()
    