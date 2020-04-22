### python specific import
import argparse
import os
import sys
import pickle
import shutil
import subprocess
import time
import ROOT as rt
import math
from zipfile import ZipFile

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--select'   , action='store_true'  )
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , nargs='*', type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')
parser.add_argument('--condor'     , action='store_true' )
parser.add_argument('-n','--njob'  , dest = 'njob'   , type = int,  default=1)
parser.add_argument('--ijob'       , dest = 'ijob'   , type = int,  default=0)
parser.add_argument('--fit', dest = 'fit'  , type = str, default='')
parser.add_argument('--subjob'     , action='store_true' )
parser.add_argument('--doDraw'     , action='store_true' )

args = parser.parse_args()

def condor_wait(condorjoblist):
    print 'waiting for condor jobs', condorjoblist
    finished=False
    firsttry=True
    while not finished:
        if firsttry:
            firsttry=False
        else:
            time.sleep(30)
        finished=True
        for jobid in condorjoblist:
            if not int(subprocess.check_output('condor_q '+str(jobid)+'|tail -n 1|awk \'{print $1}\'',shell=True).strip())==0:
                finished=False

def print_step(step):
    print '##############################################'
    print '########## '+step+' ##########################'
    print '##############################################'

startTime = time.time()
print 'Starts at ', time.strftime('%c', time.localtime(startTime))
print '===> settings %s <===' % args.settings
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
print importSetting
exec(importSetting)

if args.fit == 'stdin':
    print 'inside'
    stdinlist=[]
    for line in sys.stdin:
        stdinlist.append(line)
    for sample in tnpConf.flags.values():
        sample.fitfunctions['stdin']=stdinlist
        print sample.fitfunctions
    sys.stdin.flush()

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot


if not args.flag in tnpConf.flags.keys() and not args.flag is None:
    print '[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag
    print '  --> define in settings first'
    print '  In settings I found flags: '
    print tnpConf.flags.keys()
    sys.exit(1)

####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    print_step('checkBins')
    for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
        print '############'+flag+'#############'
        tnpBins = tnpBiner.createBins(tnpConf.biningDef,sample.eventexp)
        tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
        for ib in range(len(tnpBins['bins'])):
            print tnpBins['bins'][ib]['name']
            print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)

if args.createBins:
    print_step('createBins')
    for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
        print '############'+flag+'#############'
        outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,flag)
        os.makedirs( outputDirectory )
        tnpBins = tnpBiner.createBins(tnpConf.biningDef,sample.eventexp)
        tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
        pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
        print 'created dir: %s ' % outputDirectory
        print 'bining created successfully... '


####################################################################
##### Create Histograms
####################################################################
if args.createHists:
    print_step('createHists')
    if args.condor:
        waiting_list={}
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            waiting_list[flag]=[]
            for i in range(args.njob):
                waiting_list[flag].append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --createHists --flag '+flag+' --subjob --njob '+str(args.njob)+ ' --ijob '+str(i)+'" etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            condor_wait(waiting_list[flag])
            histfile='%s/%s/%s_hist.root'%(tnpConf.baseOutDir,flag,flag)
            os.system('hadd -f '+histfile+' '+histfile+'.condortmp* && rm '+histfile+'.condortmp*')
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            import libPython.histUtils as tnpHist
            print 'creating histogram for flag '+flag
            histfile='%s/%s/%s_hist.root'%(tnpConf.baseOutDir,flag,flag)
            var = { 'name' : 'mass', 'nbins' : sample.mass_nbin, 'min' : sample.mass_min, 'max': sample.mass_max }
            if 'mc_altsig2' in flag:
                var = { 'name' : 'mcMass', 'nbins' : sample.mass_nbin, 'min' : sample.mass_min, 'max': sample.mass_max }
            tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
            tnpHist.makePassFailHistograms( sample.paths, 'tpTree/fitter_tree', histfile+ ('.condortmp'+str(args.ijob) if args.subjob else ''),tnpConf.passcondition, tnpBins, var,None,args.njob,args.ijob)
            
####################################################################
##### Actual Fitter
####################################################################
iBinlist='--iBin '
if args.binNumber == -1 or args.binNumber == []:
    iBinlist = ''
else:
    for ib in args.binNumber:
        iBinlist += str(ib)
        iBinlist += ' '
    print 'Input iBin is ', iBinlist

if  args.doFit:
    print_step('doFit')
    if args.condor:
        waiting_list=[]
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            ###### Sysetmatic (data_altsig) should be fitted after (mc_altsig) step is done
            if 'data_altsig' in flag:
                continue 
            fitfile='%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag)
            rootfile=rt.TFile(fitfile,"update")
            rootfile.Close()
            print 'submit ',flag
            waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --doFit --flag '+flag+' '+iBinlist+' --subjob " etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        condor_wait(waiting_list)

        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            if 'data_altsig'  not in flag:
                continue
            waiting_list=[]
            print 'Other sysetmatics are done'
            fitfile='%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag)
            rootfile=rt.TFile(fitfile,"update")
            rootfile.Close()
            print 'Now submit ',flag
            waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --doFit --flag '+flag+' '+iBinlist+' --subjob " etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
            condor_wait(waiting_list)
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
            for ib in range(len(tnpBins['bins'])) if args.binNumber<0 else args.binNumber:
                histfile='%s/%s/%s_hist.root'%(tnpConf.baseOutDir,flag,flag)
                fitfile='%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag)
                tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
                tnpRoot.histFitter_Norminal(histfile,fitfile,tnpBins['bins'][ib],sample.mass_min,sample.mass_max,sample.fitfunction,args.doDraw)
                '''
                if 'altsig' not in flag:
                    tnpRoot.histFitter_Norminal(histfile,fitfile,tnpBins['bins'][ib],sample.mass_min,sample.mass_max,sample.fitfunction,args.doDraw)
                else:
                    tnpRoot.histFitter_AltSig(histfile,fitfile,tnpBins['bins'][ib],sample.mass_min,sample.mass_max,sample.fitfunction,args.doDraw)
                '''

####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    print_step('doPlot')
    if args.condor:
        waiting_list=[]
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --doPlot --flag '+flag+' '+iBinlist+' --subjob " etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        condor_wait(waiting_list)
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            fitfile = '%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag)
            plottingDir = '%s/%s/plots' % (tnpConf.baseOutDir,flag)
            tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
            if not os.path.exists( plottingDir ):
                os.makedirs( plottingDir )
            shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

            fitzip = '%s/%s/fitCanvas.zip'%(tnpConf.baseOutDir,flag)
            with ZipFile(fitzip, 'w') as pngzip:
                for ib in range(len(tnpBins['bins'])) if args.binNumber<0 else args.binNumber:
                    tnpRoot.histPlotter( fitfile, tnpBins['bins'][ib], plottingDir )
                    pngzip.write('%s/%s.png' %(plottingDir,tnpBins['bins'][ib]['name']))

                    os.remove('%s/%s.png' %(plottingDir,tnpBins['bins'][ib]['name'])) # To save fitcanvas only in zip file. (They are too many to view on web)
                pngzip.write('%s/index.php' % plottingDir)
                os.remove('%s/index.php' % plottingDir)
                os.rmdir('%s/' %plottingDir)
            print ' ===> Plots saved in <======='
            print fitzip

####################################################################
##### dumping egamma txt file 
####################################################################
#tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )
#outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)
#flag.histFile='%s/%s_hist.root' % ( outputDirectory , args.flag )
#flag=tnpConf.flags[args.flag]
#flag.fitFile='%s/%s_fit.root' % ( outputDirectory,args.flag )
if args.sumUp:
    print_step('sumUp')
    for centralflag,syss in tnpConf.systematicDef.items():
        effFileName ='%s/muonEffi_%s.txt' % (tnpConf.baseOutDir,centralflag)
        fOut = open( effFileName,'w')
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,centralflag),'rb') )
        erroravg_stat=[]  #### For printing average of errors on bottom line
        erroravg_sys=[]
        erroravg_total=[]
        for ib in range(len(tnpBins['bins'])):
            if ib == 0 :
                fOut.write('ibin\tCentral\tStaterr\tSysterr\tTotalerr  [MassRange]\t[MassBin]\t[TagIso]\t[AltSig]   Syst/Stat\n')
            line=[]
            line.append(str(ib))
            centralval,centralerr = tnpRoot.GetEffi( '%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,centralflag,centralflag),tnpBins['bins'][ib]['name'])
            line+=['%.4f '%centralval,'%.4f '%centralerr]
            erroravg_stat.append(centralerr)
            totalsys=0
            totalerr=0
            for sys in syss:
                maxdiff=0
                for flag in sys:
                    thisval,thiserr = tnpRoot.GetEffi('%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag),tnpBins['bins'][ib]['name'])
                    diff=thisval-centralval
                    line.append('%+.4f'%diff)
                    if abs(maxdiff)<abs(diff): maxdiff=diff
                totalsys+=maxdiff*maxdiff
            totalerr+=(centralerr*centralerr+totalsys)
            line.insert(3,'%.4f'%math.sqrt(totalsys))
            line.insert(4,'%.4f'%math.sqrt(totalerr))
            line.append('    ')
            if centralerr != 0:
                line.append('%.2f'%(math.sqrt(totalsys)/centralerr)) ## Ratio of syst/stat, if this value is significantly large, maybe you need to check.
            erroravg_sys.append(math.sqrt(totalsys))
            erroravg_total.append(math.sqrt(totalerr))
            fOut.write("\t".join(line)+"\n")

            if ib == len(tnpBins['bins'])-1:   #### Print average of errors
                line_last=['Average', 'error:']
                line_last+=['%.6f (stat)'%(sum(erroravg_stat)/len(erroravg_stat)),'%.6f (syst)'%(sum(erroravg_sys)/len(erroravg_sys)),'%.6f (total)'%(sum(erroravg_total)/len(erroravg_total))]
                fOut.write("\t".join(line_last)+'\n')
        fOut.close()
        print 'Eff is saved in file : ',  effFileName

    fOut=rt.TFile('%s/result.root'%(tnpConf.baseOutDir),'recreate')
    effihists=[]
    for centralflag,syss in tnpConf.systematicDef.items():
        effFileName ='%s/muonEffi_%s.txt' % (tnpConf.baseOutDir,centralflag)
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,centralflag),'rb') )
        effihist=tnpRoot.GetEffiHist(effFileName,tnpBins)
        effihist.Write()
        for ib in range(effihist.GetXaxis().GetNbins()):
            effihist.ProjectionY('%s_eta%.2fto%.2f'%(centralflag,effihist.GetXaxis().GetBinLowEdge(ib+1),effihist.GetXaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        for ib in range(effihist.GetYaxis().GetNbins()):
            effihist.ProjectionX('%s_pt%dto%d'%(centralflag,effihist.GetYaxis().GetBinLowEdge(ib+1),effihist.GetYaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        effihists.append(effihist)
    
    if len(effihists)==2:
        sfhist=effihists[0].Clone()
        sfhist.Divide(effihists[1])
        sfhist.SetNameTitle('SF_eta_pt','SF_eta_pt')
        sfhist.Write()
    fOut.Close()
    print '%s/result.root'%(tnpConf.baseOutDir) + ' is saved'

##### Won added. To draw rootfiles only including Statistical error or Systematic error. #####
    fOut_stat=rt.TFile('%s/result_stat.root'%(tnpConf.baseOutDir),'recreate')
    effihists_stat=[]
    for centralflag,syss in tnpConf.systematicDef.items():
        effFileName ='%s/muonEffi_%s.txt' % (tnpConf.baseOutDir,centralflag)
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,centralflag),'rb') )
        effihist=tnpRoot.GetEffiHist(effFileName,tnpBins,"stat") ## Only Staterr
        effihist.Write()
        for ib in range(effihist.GetXaxis().GetNbins()):
            effihist.ProjectionY('%s_eta%.2fto%.2f'%(centralflag,effihist.GetXaxis().GetBinLowEdge(ib+1),effihist.GetXaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        for ib in range(effihist.GetYaxis().GetNbins()):
            effihist.ProjectionX('%s_pt%dto%d'%(centralflag,effihist.GetYaxis().GetBinLowEdge(ib+1),effihist.GetYaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        effihists_stat.append(effihist)

    if len(effihists_stat)==2:
        sfhist=effihists_stat[0].Clone()
        sfhist.Divide(effihists_stat[1])
        sfhist.SetNameTitle('SF_eta_pt','SF_eta_pt')
        sfhist.Write()
    fOut_stat.Close()
    print '%s/result_stat.root'%(tnpConf.baseOutDir) + ' is saved'

    fOut_syst=rt.TFile('%s/result_syst.root'%(tnpConf.baseOutDir),'recreate')
    effihists_syst=[]
    for centralflag,syss in tnpConf.systematicDef.items():
        effFileName ='%s/muonEffi_%s.txt' % (tnpConf.baseOutDir,centralflag)
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,centralflag),'rb') )
        effihist=tnpRoot.GetEffiHist(effFileName,tnpBins,"syst") ## Only Systerr
        effihist.Write()
        for ib in range(effihist.GetXaxis().GetNbins()):
            effihist.ProjectionY('%s_eta%.2fto%.2f'%(centralflag,effihist.GetXaxis().GetBinLowEdge(ib+1),effihist.GetXaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        for ib in range(effihist.GetYaxis().GetNbins()):
            effihist.ProjectionX('%s_pt%dto%d'%(centralflag,effihist.GetYaxis().GetBinLowEdge(ib+1),effihist.GetYaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        effihists_syst.append(effihist)

    if len(effihists_syst)==2:
        sfhist=effihists_syst[0].Clone()
        sfhist.Divide(effihists_syst[1])
        sfhist.SetNameTitle('SF_eta_pt','SF_eta_pt')
        sfhist.Write()
    fOut_syst.Close()
    print '%s/result_syst.root'%(tnpConf.baseOutDir) + ' is saved'

##### Won added. To draw rootfiles per each systematics. -> Later, these will used in systematic study.
    for flag,sample in tnpConf.flags.items():
        effReport = open('%s/%s/report.txt'%(tnpConf.baseOutDir,flag), 'w')
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,centralflag),'rb') )
        effReport.write('ibin\t'+'Eff\tErr\n')
        for ib in range(len(tnpBins['bins'])):
            thisval,thiserr = tnpRoot.GetEffi('%s/%s/%s_fitresult.root'%(tnpConf.baseOutDir,flag,flag),tnpBins['bins'][ib]['name'])
            effReport.write('%d\t%.4f\t%.4f\t\n'%(ib,thisval,thiserr))
        effReport.close()

    for flag,sample in tnpConf.flags.items():
        fOut_stat=rt.TFile('%s/%s/result_stat.root'%(tnpConf.baseOutDir,flag),'recreate')
        effReport ='%s/%s/report.txt' % (tnpConf.baseOutDir,flag)
        tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
        effihist=tnpRoot.GetEffiHist(effReport,tnpBins,"stat") ## Only Staterr
        effihist.Write()
        for ib in range(effihist.GetXaxis().GetNbins()):
            effihist.ProjectionY('%s_eta%.2fto%.2f'%(flag,effihist.GetXaxis().GetBinLowEdge(ib+1),effihist.GetXaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        for ib in range(effihist.GetYaxis().GetNbins()):
            effihist.ProjectionX('%s_pt%dto%d'%(flag,effihist.GetYaxis().GetBinLowEdge(ib+1),effihist.GetYaxis().GetBinLowEdge(ib+2)),ib+1,ib+1).Write()
        fOut_stat.Close()
        print '%s/%s/result_stat.root'%(tnpConf.baseOutDir,flag) + ' is saved'

#    import libPython.EGammaID_scaleFactors as egm_sf
#    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)

endTime=time.time()
print 'Ends at ', time.strftime('%c',time.localtime(endTime))
print 'Time took', endTime-startTime,'seconds.'
