
### python specific import
import argparse
import os
import sys
import pickle
import shutil
import subprocess
import time
import ROOT as rt

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--select'   , action='store_true'  )
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
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
    print 'wainting for condor jobs', condorjoblist
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
    sys.exit(0)



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
            tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
            tnpHist.makePassFailHistograms( sample.paths, 'tpTree/fitter_tree', histfile+ ('.condortmp'+str(args.ijob) if args.subjob else ''),tnpConf.passcondition, tnpBins, var,None,args.njob,args.ijob)
            
    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
#tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )
#outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)
#flag.histFile='%s/%s_hist.root' % ( outputDirectory , args.flag )
#flag=tnpConf.flags[args.flag]
#flag.fitFile='%s/%s_fit.root' % ( outputDirectory,args.flag )
if  args.doFit:
    print_step('doFit')
    if args.condor:
        waiting_list=[]
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            for ifit in sample.fitfunctions.keys() if args.fit=='' else [args.fit,]:
                fitfile='%s/%s/%s_fit_%s.root'%(tnpConf.baseOutDir,flag,flag,ifit)
                rootfile=rt.TFile(fitfile,"recreate")
                rootfile.Close()
                print 'submit ',flag, ifit
                waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --doFit --flag '+flag+' --subjob --fit '+ifit+'" etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        condor_wait(waiting_list)
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            for ifit in sample.fitfunctions.keys() if args.fit=='' else [args.fit,]:
                tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
                for ib in range(len(tnpBins['bins'])) if args.binNumber<0 else [args.binNumber,]:
                    histfile='%s/%s/%s_hist.root'%(tnpConf.baseOutDir,flag,flag)
                    fitfile='%s/%s/%s_fit_%s.root'%(tnpConf.baseOutDir,flag,flag,ifit)
                    tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
                    tnpRoot.histFitter(histfile,fitfile,tnpBins['bins'][ib],sample.mass_min,sample.mass_max,sample.fitfunctions[ifit],args.doDraw)

####################################################################
##### select
####################################################################
if args.select:
    print_step('select')
    if args.condor:
        waiting_list=[]
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --select --flag '+flag+' --subjob" etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        condor_wait(waiting_list)
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            print flag
            fitfile='%s/%s/%s_fit.root'%(tnpConf.baseOutDir,flag,flag)
            tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
            rootfile=rt.TFile(fitfile.replace('.root','_best.root'),"recreate")
            rootfile.Close()
            report=open('%s/%s/report'%(tnpConf.baseOutDir,flag),'w')
            report.write('ibin\t'+'\t'.join(sample.fitfunctions.keys())+'\tbestfit\n')
            for ib in range(len(tnpBins['bins'])):
                report.write(str(ib)+'\t')
                bestfit=''
                bestval=0
                tempfit=''
                tempval=99999
                for ifit in sample.fitfunctions.keys() if args.fit=='' else [args.fit,]: 
                    scorePass,scoreFail=tnpRoot.GetScorePassFail(fitfile.replace('.root','_'+ifit+'.root'),tnpBins['bins'][ib]['name'])
                    nBkgPass=tnpRoot.GetRooFitPar(fitfile.replace('.root','_'+ifit+'.root'),tnpBins['bins'][ib]['name']+'_resP','nBkgP')
                    nBkgFail=tnpRoot.GetRooFitPar(fitfile.replace('.root','_'+ifit+'.root'),tnpBins['bins'][ib]['name']+'_resF','nBkgF')
                    thisval=nBkgPass+nBkgFail
                    thistempval=scorePass+scoreFail
                    report.write('%.1f\t'%thisval)
                    if thisval>bestval and scorePass<4 and scoreFail<4:
                        bestval=thisval
                        bestfit=ifit
                    if thistempval<tempval:
                        tempval=thistempval
                        tempfit=ifit
                if bestfit=='':
                    print tnpBins['bins'][ib]['name'],' fail to find good result, use second option'
                    bestfit=tempfit
                report.write(bestfit+'\n')
                tnpRoot.MoveTObject(fitfile.replace('.root','_'+bestfit+'.root'),fitfile.replace('.root','_best.root'),tnpBins['bins'][ib]['name']+'_resP')
                tnpRoot.MoveTObject(fitfile.replace('.root','_'+bestfit+'.root'),fitfile.replace('.root','_best.root'),tnpBins['bins'][ib]['name']+'_resF')
                tnpRoot.MoveTObject(fitfile.replace('.root','_'+bestfit+'.root'),fitfile.replace('.root','_best.root'),tnpBins['bins'][ib]['name']+'_Canv')
            report.close()
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    print_step('doPlot')
    if args.condor:
        waiting_list=[]
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            for ifit in ['best']+sample.fitfunctions.keys() if args.fit=='' else [args.fit,]:
                waiting_list.append(subprocess.check_output('condor_submit ARGU="'+args.settings+' --doPlot --flag '+flag+' --subjob --fit '+ifit+'" etc/scripts/condor.jds -queue 1|tail -n 1|awk \'{print $NF}\'|sed "s/[^0-9]//g"',shell=True).strip())
        condor_wait(waiting_list)
    else:
        for flag,sample in tnpConf.flags.items() if args.flag is None else [(args.flag,tnpConf.flags[args.flag])]:
            for ifit in ['best']+sample.fitfunctions.keys() if args.fit=='' else [args.fit,]:
                fitfile = '%s/%s/%s_fit_%s.root'%(tnpConf.baseOutDir,flag,flag,ifit)
                plottingDir = '%s/%s/plots/%s' % (tnpConf.baseOutDir,flag,ifit)
                tnpBins = pickle.load( open( '%s/%s/bining.pkl'%(tnpConf.baseOutDir,flag),'rb') )
                if not os.path.exists( plottingDir ):
                    os.makedirs( plottingDir )
                shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)
                for ib in range(len(tnpBins['bins'])) if args.binNumber<0 else [args.binNumber,]:
                    tnpRoot.histPlotter( fitfile, tnpBins['bins'][ib], plottingDir )

                print ' ===> Plots saved in <======='
                print plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        'dataNominal' : sampleToFit.nominalFit,
        'dataAltSig'  : sampleToFit.altSigFit ,
        'dataAltBkg'  : sampleToFit.altBkgFit ,
        'mcNominal'   : sampleToFit.mcRef.histFile,
        'mcAlt'       : None,
        'tagSel'      : None
        }

    if not tnpConf.samplesDef['mcAlt' ] is None:
        info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    if not tnpConf.samplesDef['tagSel'] is None:
        info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print astr
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print astr
            fOut.write( astr + '\n' )
            
        astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltBkg' ][0],
            effis['dataAltSig' ][0],
            effis['mcAlt' ][0],
            effis['tagSel'][0],
            )
        print astr
        fOut.write( astr + '\n' )
    fOut.close()

    print 'Effis saved in file : ',  effFileName
    import libPython.EGammaID_scaleFactors as egm_sf
    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)


