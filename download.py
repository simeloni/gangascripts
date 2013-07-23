# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import os, commands, re
def download(job,min=-1,targetdir=None,force_redownload=False):
    # if no targetdir specified, don't do magic with it
    if isinstance(targetdir, str):
      # otherwise create target dir (-p = don't complain if it already exists)
      commands.getstatusoutput('mkdir -p ' + targetdir)
      # if targetdir doesn't end with / then add it
      if targetdir.endswith("/"):
       dummy = 1+1
       # nothing to do
      else:
       targetdir = targetdir + "/"

    # check if job id or job object has been given
    if isinstance (job, int) :
       thejob = jobs(job)
    else :
       thejob = job

    for sj in thejob.subjobs.select(status="completed"):
        if sj.id>min:
            for f in sj.outputfiles.get("*.root"):
                if ""==f.lfn:
                    print "no lfn for file ", f.namePattern, " from job", str(thejob.id), ".", str(sj.id)
                    continue
                if isinstance(targetdir,str):
                  f.localDir = targetdir
                  ending = re.sub(".*\.","",f.namePattern)  # the file ending is everything after the last .
                  mainpart = re.sub("\."+ending,"",f.namePattern) # the main part of the filename is everything before the ending (removing the .)
                  newmainpart = mainpart + "_" + str(sj.id)
                  targetfilename = targetdir + "/" + newmainpart + "." + ending
                  automaticname = f.localDir + "/" + f.namePattern
                else:
                  automaticname = f.outputdir + f.namePattern
                  targetfilename = f.outputdir + f.namePattern
                if (os.path.isfile(targetfilename)) :
                    print "file ", f.namePattern, " from job", str(thejob.id), ".", str(sj.id), " already loaded"
                    if force_redownload:
                        print "load it anyway"
                        f.get()
                        if automaticname!=targetfilename:
                          commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                else:
                        f.get()
                        if automaticname!=targetfilename:
                          commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                
        
