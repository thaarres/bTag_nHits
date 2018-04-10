#! /usr/bin/env python

import os, multiprocessing, math, sys
import ROOT as rt

import optparse


if __name__ == "__main__":
  
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-i', '--input', action='store', type='string', dest='origin', default='ZprimeBB2000.txt')
  parser.add_option('-o', '--output', action='store', type='string', dest='target', default='/afs/cern.ch/work/t/thaarres/public/bTag_ntracks/CMSSW_9_3_2/src/bTag_nHits/HitAnalyzer/Output/')
  parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)
  parser.add_option('-m', '--multiprocess', action='store_true', dest='multiprocess', default=False)
  
  (options, args) = parser.parse_args()
  
  origin        = options.origin
  target        = options.target
  verboseout    = options.verbose
  
  jobname = "bTag"
  files = []
  loc = glob.glob(origin)   
  for f in loc:
    with open(f) as fp: 
	    line = fp.readline()
	    while line:
	      line = fp.readline()
	      if line.find(".root")==-1: continue
	      files.append(line)        
  print files
  # filelists = list(split_seq(filelists,10))
  # jobList = 'joblist_'+pattern+'.txt'
  # jobs = open(jobList, 'w')
  
  NumberOfJobs= len(files) 
  cmd='python testAnalyzer.py -i %s -o %s' %(origin,target)
  queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
  
  
  try: os.system("rm -r tmp"+jobname)
  except: print "No tmp/ directory"
  os.system("mkdir tmp"+jobname)
  try: os.stat("res"+jobname) 
  except: os.mkdir("res"+jobname)
        
    
  ##### Creating and sending jobs #####
  joblist = []
  ###### loop for creating and sending jobs #####
  path = os.getcwd()
  for i,file in enumerate(files):
     os.system("mkdir tmp"+jobname+"/"+str(file).replace(".root",""))
     os.chdir("tmp"+jobname+"/"+str(file).replace(".root",""))
     #os.system("mkdir tmp"+jobname+"/"+str(file).replace(".root",""))
     os.chdir(path+"/tmp"+jobname+"/"+str(file).replace(".root",""))
   
     with open('job_%s.sh'%file.replace(".root",""), 'w') as fout:
        fout.write("#!/bin/sh\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("echo 'WORKDIR ' ${PWD}\n")
        fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
        fout.write("cd "+str(path)+"\n")
        fout.write("cmsenv\n")
        fout.write(cmd+file+"\n")
        fout.write("echo 'STOP---------------'\n")
        fout.write("echo\n")
        fout.write("echo\n")
     os.system("chmod 755 job_%s.sh"%(file.replace(".root","")) )
     os.system("bsub -q "+queue+" -o logs job_%s.sh -J %s"%(file.replace(".root",""),jobname))
     print "job nr " + str(i+1) + " submitted"
     joblist.append("%s"%(file.replace(".root","")))
     os.chdir("../..")
   
  print
  print "your jobs:"
  os.system("bjobs")
  userName=os.environ['USER']
  
  print
  print 'Done submitting jobs!'
  print
  
