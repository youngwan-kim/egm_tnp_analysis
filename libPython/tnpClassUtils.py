import copy
import os

def mkdir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

class tnpSample:
    def __init__(self, paths, eventexp, fitfunction,mass_nbin,mass_min,mass_max):
        self.paths=paths
        self.eventexp=eventexp
        self.fitfunction=fitfunction
        self.histFile=None
        self.fitFile=None
        self.mass_nbin=mass_nbin
        self.mass_min=mass_min
        self.mass_max=mass_max
 
    def dump(self):
        print '  paths    : ', self.paths
        print '  eventexp  : ', self.eventexp
        print '  fitfuction  : ', self.fitfunction
        print '  histFile  : ', self.histFile
        print '  fitFile  : ', self.fitFile
        print '  mass_nbin  : ', self.mass_nbin
        print '  mass_min: ',self.mass_min
        print '  mass_max: ',self.mass_max


import ROOT as rt
class tnpVar:
    def __init__(self, var, hname = None, title = None, xmin = 0, xmax = 0, nbins = -1 ):
        self.var   = var
        if title is None :  self.title = var
        else:               self.title = title
        self.xmin  = xmin
        self.xmax  = xmax
        self.nbins = nbins
        self.hname = hname
        self.hist  = None

    def get_hist(self):
        if self.nbins > 0:
            if self.hname is None:  self.hname  = 'h_%' % var
            self.hist  = rt.TH1F( self.hname, self.title, 
                                  self.nbins, self.xmin, self.xmax )
            self.hist.GetXaxis().SetTitle(self.title)
            self.hist.SetMinimum(0)

        else:
            self.hist = None

        return self.hist

    def set_hname(self,name):
        self.hname = name


