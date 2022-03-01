#!/usr/bin/env python

### python specific import
import argparse
import os
import sys
import pickle
import shutil
from datetime import datetime

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--njob', '-n' , default=-1,type = int, help = 'condor njob')
parser.add_argument('--nmax', '-m' , default=-1,type = int, help = 'condor nmax job (concurrency limits)')
parser.add_argument('--fitlog'     , action='store_true'  , help = 'save fitting log')
parser.add_argument('--jobIndex'   , default=-1,type = int, help = 'condor job index (for internal)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')


args = parser.parse_args()

print '===> settings %s <===' % args.settings
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
print importSetting
exec(importSetting)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot


if args.flag is None:
    print '[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py'
    sys.exit(0)
    
if not args.flag in tnpConf.flags.keys() :
    print '[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag
    print '  --> define in settings first'
    print '  In settings I found flags: '
    print tnpConf.flags.keys()
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print '===>  Output directory: '
print outputDirectory


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    if not tnpConf.additionalCutBase is None:
        if args.flag in tnpConf.additionalCutBase:
            tnpConf.cutBase+=' && '+tnpConf.additionalCutBase[args.flag]
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print tnpBins['bins'][ib]['name']
        print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)
    
if args.createBins:
    if not tnpConf.additionalCutBase is None:
        if args.flag in tnpConf.additionalCutBase:
            tnpConf.cutBase+=' && '+tnpConf.additionalCutBase[args.flag]
    if os.path.exists( outputDirectory ):
            shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print 'created dir: %s ' % outputDirectory
    print 'bining created successfully... '
    print 'Note than any additional call to createBins will overwrite directory %s' % outputDirectory
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )

if args.createHists:

    import libPython.histUtils as tnpHist

    for sampleType in tnpConf.samplesDef.keys():
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : continue
        if sampleType == args.sample or args.sample == 'all' :
            print 'creating histogram for sample '
            sample.dump()
            var = { 'nbins' : 80, 'min' : 50, 'max': 130 }
            newpath=[]
            for p in sample.path:
                if p.endswith('.root'): 
                    newpath.append(p)
                else:
                    newpath.extend(os.popen('find '+p+' -type f -name \'*.root\' | sort -V').read().split('\n'))
                    if newpath[-1]=='': newpath=newpath[:-1]
            sample.path=newpath
            if args.njob>0:
                if args.jobIndex<0:
                    print 'submitting', args.njob, 'jobs, nmax=', args.nmax
                    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
                    jobbatchname='createHists_%s_%s_%s'%(os.path.splitext(os.path.basename(args.settings))[0],args.flag,sampleType)
                    working_dir='log/'+timestamp+'_'+jobbatchname
                    os.system('mkdir '+working_dir)
                    with open(working_dir+'/condor.jds','w') as f:
                        f.write(
'''
executable = tnpEGM_fitter.py
arguments = {0} --flag {1} --sample {2} --createHists --njob {3} --jobIndex $(Process)
output = {4}/job$(Process).out
error = {4}/job$(Process).err
log = {4}/condor.log
{5}
jobbatchname = {6}
getenv = True
queue {3}
'''.format(args.settings,args.flag,sampleType,str(args.njob),working_dir,'concurrency_limits = n'+str(args.nmax)+'.'+os.getenv("USER") if args.nmax>0 else '',jobbatchname))
                    os.system('condor_submit '+working_dir+'/condor.jds')                        
                    print 'Waiting jobs...'
                    os.system('condor_wait '+working_dir+'/condor.log')
                    outfiles=[]
                    for i in range(args.njob): outfiles.append('%s_job%d.root'%(os.path.splitext(sample.histFile)[0],i))
                    os.system('hadd -f %s %s'%(sample.histFile,' '.join(outfiles)))
                    os.system('rm %s'%(os.path.splitext(sample.histFile)[0]+'_job*.root'))
                else:
                    if len(sample.path) >= args.njob:
                        stepsize=len(sample.path)/args.njob+1
                        sample.path=sample.path[stepsize*args.jobIndex:stepsize*(args.jobIndex+1)]
                        sample.histFile=os.path.splitext(sample.histFile)[0]+'_job%d.root'%args.jobIndex
                    
                        if len(sample.path):print 'Using %d files from %s to %s'%(len(sample.path),sample.path[0],sample.path[-1])
                        tnpHist.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )
                    else:
                        sample.histFile=os.path.splitext(sample.histFile)[0]+'_job%d.root'%args.jobIndex                    
                        if len(sample.path):print 'Using %d files from %s to %s'%(len(sample.path),sample.path[0],sample.path[-1])
                        print 'Loop from %d/%d to %d/%d'%(args.jobIndex,args.njob,args.jobIndex+1,args.njob)
                        var['njob']=args.njob
                        var['jobIndex']=args.jobIndex
                        tnpHist.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )
                        
            else:
                tnpHist.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )

    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
if sampleToFit is None:
    print '[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings'
    sys.exit(1)

sampleMC = tnpConf.samplesDef['mcNom']

if sampleMC is None:
    print '[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings'
    sys.exit(1)
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'mcRef'     , sampleMC )
    fitType  = 'nominalFit'
    if args.altSig : 
        fitType  = 'altSigFit'
    if args.altBkg : 
        fitType  = 'altBkgFit'
    fitFile='%s/%s_%s.%s.root'  % ( outputDirectory , sample.name, args.flag,fitType )
    setattr( sample, 'fitType' , fitType )
    setattr( sample, 'fitFile' , fitFile )


### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = tnpConf.samplesDef['mcNom']

if  args.doFit:    
    sampleToFit.dump()
    if args.njob>0 or args.nmax>0:
        if args.nmax==-1: args.nmax=args.njob
        if args.jobIndex<0:
            if os.path.exists(os.path.splitext(sampleToFit.fitFile)[0]):
                shutil.rmtree(os.path.splitext(sampleToFit.fitFile)[0])
            os.makedirs(os.path.splitext(sampleToFit.fitFile)[0])
            timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
            arguments='%s --flag %s --doFit -n %d --jobIndex=$(Process)'%(args.settings,args.flag,args.njob)
            jobbatchname='doFit_%s_%s'%(os.path.splitext(os.path.basename(args.settings))[0],args.flag)
            priority=''
            if args.mcSig :
                jobbatchname+='_mcSig'
                arguments+=' --mcSig'
            if args.altSig:
                jobbatchname+='_altSig'
                arguments+=' --altSig'
                priority='priority = 1'
            elif args.altBkg:
                jobbatchname+='_altBkg'
                arguments+=' --altBkg'
            working_dir='log/'+timestamp+'_'+jobbatchname
            os.system('mkdir '+working_dir)
            with open(working_dir+'/condor.jds','w') as f:
                f.write(
'''
executable = tnpEGM_fitter.py
arguments = {0}
output = {1}/job$(Process).out
error = {1}/job$(Process).err
log = {1}/condor.log
{2}
jobbatchname = {3}
getenv = True
{4}
queue {5}
'''.format(arguments,working_dir,'concurrency_limits = n'+str(args.nmax)+'.'+os.getenv("USER") if args.nmax>0 else '',jobbatchname,priority,str(len(tnpBins['bins']))))
            #if args.fitlog: pythoncmd+=' &> log/'+logname
            #else: pythoncmd+=' &> /dev/null'                

            os.system('condor_submit '+working_dir+'/condor.jds')                        
            print 'Waiting jobs...'
            os.system('condor_wait '+working_dir+'/condor.log')

            outfiles=[]
            for ib in range(len(tnpBins['bins'])): outfiles.append('%s/bin%d.root'%(os.path.splitext(sampleToFit.fitFile)[0],ib))
            os.system('hadd -f %s %s'%(sampleToFit.fitFile,' '.join(outfiles)))
            args.doPlot=True
            
        else: 
            subsample=sampleToFit.clone()
            subsample.fitFile=os.path.splitext(subsample.fitFile)[0]+'/bin%d.root'%args.jobIndex
            if args.altSig:
                tnpRoot.histFitterAltSig(  subsample, tnpBins['bins'][args.jobIndex], tnpConf.tnpParAltSigFit )
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  subsample, tnpBins['bins'][args.jobIndex], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( subsample, tnpBins['bins'][args.jobIndex], tnpConf.tnpParNomFit )

    else:
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            if args.altSig:                 
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
        outfiles=[]
        for ib in range(len(tnpBins['bins'])): outfiles.append('%s/bin%d.root'%(os.path.splitext(sampleToFit.fitFile)[0],ib))
        os.system('hadd -f %s %s'%(sampleToFit.fitFile,' '.join(outfiles)))
        args.doPlot=True


    #sys.exit(0)

####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,sampleToFit.fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( sampleToFit.fitFile, tnpBins['bins'][ib], plottingDir )

    print ' ===> Plots saved in <======='
    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        'dataNominal' : '%s/%s_%s.nominalFit.root'  % ( outputDirectory , sampleToFit.name, args.flag ),
        'dataAltSig'  : '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sampleToFit.name, args.flag ),
        'dataAltBkg'  : '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sampleToFit.name, args.flag ) ,
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
