import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

from RecoTracker.TkSeedingLayers.seedingLayersEDProducer_cfi import *

from RecoTracker.ConversionSeedGenerators.PhotonConversionTrajectorySeedProducerFromSingleLeg_cfi import *
from RecoTracker.ConversionSeedGenerators.ConversionStep2_cff import *

from RecoLocalTracker.SubCollectionProducers.trackClusterRemover_cfi import trackClusterRemover as _trackClusterRemover
_convClustersBase = _trackClusterRemover.clone(
  maxChi2               = cms.double(30.0),
  trajectories          = cms.InputTag("tobTecStepTracks"),
  pixelClusters         = cms.InputTag("siPixelClusters"),
  stripClusters         = cms.InputTag("siStripClusters"),
  oldClusterRemovalInfo = cms.InputTag("tobTecStepClusters"),
  TrackQuality          = cms.string('highPurity'),
)
convClusters = _convClustersBase.clone(
  trackClassifier       = cms.InputTag('tobTecStep',"QualityMasks"),
)
eras.trackingPhase1PU70.toReplaceWith(convClusters, _convClustersBase.clone(
  overrideTrkQuals      = "tobTecStepSelector:tobTecStep",
))

#Phase2 : configuring the phase2 track Cluster Remover
from RecoLocalTracker.SubCollectionProducers.phase2trackClusterRemover_cfi import phase2trackClusterRemover as _phase2trackClusterRemover
eras.trackingPhase2PU140.toReplaceWith(convClusters, _phase2trackClusterRemover.clone(
    maxChi2                                  = 30.0,
    phase2pixelClusters                      = "siPixelClusters",
    phase2OTClusters                         = "siPhase2Clusters",
    TrackQuality                             = 'highPurity',
    minNumberOfLayersWithMeasBeforeFiltering = 0,
    trajectories                             = cms.InputTag("pixelPairStepTracks"),
    oldClusterRemovalInfo                    = cms.InputTag("pixelPairStepClusters"),
    overrideTrkQuals                         = cms.InputTag("pixelPairStepSelector","pixelPairStep"),
    )
)

convLayerPairs = cms.EDProducer("SeedingLayersEDProducer",
                                layerList = cms.vstring('BPix1+BPix2', 

                                                        'BPix2+BPix3', 
                                                        'BPix2+FPix1_pos', 
                                                        'BPix2+FPix1_neg', 
                                                        'BPix2+FPix2_pos', 
                                                        'BPix2+FPix2_neg', 

                                                        'FPix1_pos+FPix2_pos', 
                                                        'FPix1_neg+FPix2_neg',

                                                        'BPix3+TIB1', 
                                                        'BPix3+TIB2',
                                                        
                                                        'TIB1+TID1_pos', 
                                                        'TIB1+TID1_neg', 
                                                        'TIB1+TID2_pos', 
                                                        'TIB1+TID2_neg',
                                                        'TIB1+TIB2',
                                                        'TIB1+TIB3',

                                                        'TIB2+TID1_pos', 
                                                        'TIB2+TID1_neg', 
                                                        'TIB2+TID2_pos', 
                                                        'TIB2+TID2_neg', 
                                                        'TIB2+TIB3',
                                                        'TIB2+TIB4', 

                                                        'TIB3+TIB4', 
                                                        'TIB3+TOB1', 
                                                        'TIB3+TID1_pos', 
                                                        'TIB3+TID1_neg', 

                                                        'TIB4+TOB1',
                                                        'TIB4+TOB2',

                                                        'TOB1+TOB2', 
                                                        'TOB1+TOB3', 
                                                        'TOB1+TEC1_pos', 
                                                        'TOB1+TEC1_neg', 

                                                        'TOB2+TOB3',  
                                                        'TOB2+TOB4',
                                                        'TOB2+TEC1_pos', 
                                                        'TOB2+TEC1_neg', 

                                                        #NB: re-introduce these combinations when large displaced
                                                        #    tracks, reconstructed only in TOB will be available
                                                        #    For instance think at the OutIn Ecal Seeded tracks
                                                        #'TOB3+TOB4', 
                                                        #'TOB3+TOB5',
                                                        #'TOB3+TEC1_pos', 
                                                        #'TOB3+TEC1_neg', 
                                                        #
                                                        #'TOB4+TOB5',
                                                        #'TOB4+TOB6',
                                                        #
                                                        #'TOB5+TOB6',

                                                        'TID1_pos+TID2_pos', 
                                                        'TID2_pos+TID3_pos', 
                                                        'TID3_pos+TEC1_pos', 

                                                        'TID1_neg+TID2_neg', 
                                                        'TID2_neg+TID3_neg', 
                                                        'TID3_neg+TEC1_neg', 

                                                        'TEC1_pos+TEC2_pos', 
                                                        'TEC2_pos+TEC3_pos', 
                                                        'TEC3_pos+TEC4_pos',
                                                        'TEC4_pos+TEC5_pos',
                                                        'TEC5_pos+TEC6_pos',
                                                        'TEC6_pos+TEC7_pos',
                                                        'TEC7_pos+TEC8_pos',

                                                        'TEC1_neg+TEC2_neg', 
                                                        'TEC2_neg+TEC3_neg', 
                                                        'TEC3_neg+TEC4_neg',
                                                        'TEC4_neg+TEC5_neg',
                                                        'TEC5_neg+TEC6_neg',
                                                        'TEC6_neg+TEC7_neg',
                                                        'TEC7_neg+TEC8_neg'
                                                        #other combinations could be added
                                                        ),

                                BPix = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'),
                                    HitProducer = cms.string('siPixelRecHits'),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                FPix = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'),
                                    HitProducer = cms.string('siPixelRecHits'),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TIB1 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TIB2 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TIB3 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TIB4 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TID1 = cms.PSet(
                                    useSimpleRphiHitsCleaner = cms.bool(False),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    useRingSlector = cms.bool(True),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    maxRing = cms.int32(2),
                                    minRing = cms.int32(1),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TID2 = cms.PSet(
                                    useSimpleRphiHitsCleaner = cms.bool(False),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    useRingSlector = cms.bool(True),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    maxRing = cms.int32(2),
                                    minRing = cms.int32(1),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TID3 = cms.PSet(
                                    useSimpleRphiHitsCleaner = cms.bool(False),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    useRingSlector = cms.bool(True),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    maxRing = cms.int32(2),
                                    minRing = cms.int32(1),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TEC = cms.PSet(
                                    useSimpleRphiHitsCleaner = cms.bool(False),
                                    minRing = cms.int32(1),
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    useRingSlector = cms.bool(True),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHitUnmatched"),
                                    maxRing = cms.int32(7),
                                    stereoRecHits = cms.InputTag("siStripMatchedRecHits","stereoRecHitUnmatched"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB1 = cms.PSet(
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB2 = cms.PSet(
                                    matchedRecHits = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB3 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB4 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB5 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                TOB6 = cms.PSet(
                                    TTRHBuilder = cms.string('WithTrackAngle'), clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight')),
                                    rphiRecHits = cms.InputTag("siStripMatchedRecHits","rphiRecHit"),
                                    skipClusters = cms.InputTag('convClusters'),
                                    )
                                )
eras.trackingPhase1PU70.toModify(convLayerPairs,
    layerList = [
        'BPix1+BPix2',

        'BPix2+BPix3',
        'BPix2+FPix1_pos',
        'BPix2+FPix1_neg',
        'BPix2+FPix2_pos',
        'BPix2+FPix2_neg',

        'FPix1_pos+FPix2_pos',
        'FPix1_neg+FPix2_neg',

        'BPix3+TIB1',
        'BPix3+TIB2',

        'TIB1+TID1_pos',
        'TIB1+TID1_neg',
        'TIB1+TID2_pos',
        'TIB1+TID2_neg',
        'TIB1+TIB2',
        'TIB1+TIB3',

        'TIB2+TID1_pos',
        'TIB2+TID1_neg',
        'TIB2+TID2_pos',
        'TIB2+TID2_neg',
        'TIB2+TIB3',
        'TIB2+TIB4',

        'TIB3+TIB4',
        'TIB3+TOB1',
        'TIB3+TID1_pos',
        'TIB3+TID1_neg',

        'TIB4+TOB1',
        'TIB4+TOB2',

        'TOB1+TOB2',
        'TOB1+TOB3',
        'TOB1+TEC1_pos',
        'TOB1+TEC1_neg',

        'TOB2+TOB3',
        'TOB2+TOB4',
        'TOB2+TEC1_pos',
        'TOB2+TEC1_neg',

        #NB: re-introduce these combinations when large displaced
        #    tracks, reconstructed only in TOB will be available
        #    For instance think at the OutIn Ecal Seeded tracks
        #'TOB3+TOB4',
        #'TOB3+TOB5',
        #'TOB3+TEC1_pos',
        #'TOB3+TEC1_neg',
        #
        #'TOB4+TOB5',
        #'TOB4+TOB6',
        #
        #'TOB5+TOB6',

        'TID1_pos+TID2_pos',
        'TID2_pos+TID3_pos',
        'TID3_pos+TEC1_pos',

        'TID1_neg+TID2_neg',
        'TID2_neg+TID3_neg',
        'TID3_neg+TEC1_neg',

        'TEC1_pos+TEC2_pos',
        'TEC2_pos+TEC3_pos',
        'TEC3_pos+TEC4_pos',
        'TEC4_pos+TEC5_pos',
        'TEC5_pos+TEC6_pos',
        'TEC6_pos+TEC7_pos',
        'TEC7_pos+TEC8_pos',

        'TEC1_neg+TEC2_neg',
        'TEC2_neg+TEC3_neg',
        'TEC3_neg+TEC4_neg',
        'TEC4_neg+TEC5_neg',
        'TEC5_neg+TEC6_neg',
        'TEC6_neg+TEC7_neg',
        'TEC7_neg+TEC8_neg'
        #other combinations could be added
    ],
    BPix = dict(TTRHBuilder = "TTRHBuilderWithoutAngle4PixelPairs"),
    FPix = dict(TTRHBuilder = "TTRHBuilderWithoutAngle4PixelPairs"),
    TIB1 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TIB2 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TIB3 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TIB4 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TID1 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TID2 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TID3 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TEC  = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB1 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB2 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB3 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB4 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB5 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
    TOB6 = dict(clusterChargeCut = dict(refToPSet_ = "SiStripClusterChargeCutNone")),
)
eras.trackingPhase2PU140.toReplaceWith(convLayerPairs, cms.EDProducer("SeedingLayersEDProducer",
                                layerList = cms.vstring('BPix1+BPix2',
                                                        'BPix2+BPix3',
                                                        'BPix3+BPix4',

                                                        'BPix1+FPix1_pos',
                                                        'BPix1+FPix1_neg',
                                                        'BPix2+FPix1_pos',
                                                        'BPix2+FPix1_neg',
                                                        'BPix3+FPix1_pos',
                                                        'BPix3+FPix1_neg',

                                                        'FPix1_pos+FPix2_pos',
                                                        'FPix1_neg+FPix2_neg',
                                                        'FPix2_pos+FPix3_pos',
                                                        'FPix2_neg+FPix3_neg'
                                                        ),

                                BPix = cms.PSet(
                                    hitErrorRZ = cms.double(0.006),
                                    hitErrorRPhi = cms.double(0.0027),
                                    TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
                                    HitProducer = cms.string('siPixelRecHits'),
                                    useErrorsFromParam = cms.bool(True),
                                    skipClusters = cms.InputTag('convClusters'),
                                    ),
                                FPix = cms.PSet(
                                    hitErrorRZ = cms.double(0.0036),
                                    hitErrorRPhi = cms.double(0.0051),
                                    TTRHBuilder = cms.string('TTRHBuilderWithoutAngle4PixelPairs'),
                                    HitProducer = cms.string('siPixelRecHits'),
                                    useErrorsFromParam = cms.bool(True),
                                    skipClusters = cms.InputTag('convClusters'),
                                    )
    )
)

photonConvTrajSeedFromSingleLeg.TrackRefitter = cms.InputTag('generalTracks')
photonConvTrajSeedFromSingleLeg.primaryVerticesTag = cms.InputTag('firstStepPrimaryVertices')
#photonConvTrajSeedFromQuadruplets.TrackRefitter = cms.InputTag('generalTracks')
#photonConvTrajSeedFromQuadruplets.primaryVerticesTag = cms.InputTag('pixelVertices')
eras.trackingLowPU.toModify(photonConvTrajSeedFromSingleLeg, primaryVerticesTag   = "pixelVertices")
eras.trackingPhase1PU70.toModify(photonConvTrajSeedFromSingleLeg, primaryVerticesTag = "pixelVertices")
eras.trackingPhase2PU140.toModify(photonConvTrajSeedFromSingleLeg, primaryVerticesTag = "pixelVertices")

# TRACKER DATA CONTROL

# QUALITY CUTS DURING TRACK BUILDING
import TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff
convCkfTrajectoryFilter = TrackingTools.TrajectoryFiltering.TrajectoryFilter_cff.CkfBaseTrajectoryFilter_block.clone(
        maxLostHits = 1,
        minimumNumberOfHits = 3,
        minPt = 0.1
    )


import RecoTracker.MeasurementDet.Chi2ChargeMeasurementEstimator_cfi
convStepChi2Est = RecoTracker.MeasurementDet.Chi2ChargeMeasurementEstimator_cfi.Chi2ChargeMeasurementEstimator.clone(
    ComponentName = cms.string('convStepChi2Est'),
    nSigma = cms.double(3.0),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(100),
    MaxSagitta = cms.double(-1.),
    clusterChargeCut = cms.PSet(refToPSet_ = cms.string('SiStripClusterChargeCutTight'))
)


# TRACK BUILDING
import RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi
_convCkfTrajectoryBuilderBase = RecoTracker.CkfPattern.GroupedCkfTrajectoryBuilder_cfi.GroupedCkfTrajectoryBuilder.clone(
    trajectoryFilter = cms.PSet(refToPSet_ = cms.string('convCkfTrajectoryFilter')),
    minNrOfHitsForRebuild = 3,
    maxCand = 1,
)
convCkfTrajectoryBuilder = _convCkfTrajectoryBuilderBase.clone(
    estimator = cms.string('convStepChi2Est')
    )
eras.trackingPhase1PU70.toReplaceWith(convCkfTrajectoryBuilder, _convCkfTrajectoryBuilderBase.clone(
    maxCand = 2,
))
eras.trackingPhase2PU140.toReplaceWith(convCkfTrajectoryBuilder, _convCkfTrajectoryBuilderBase.clone(
    maxCand = 2,
))

# MAKING OF TRACK CANDIDATES
import RecoTracker.CkfPattern.CkfTrackCandidates_cfi
convTrackCandidates = RecoTracker.CkfPattern.CkfTrackCandidates_cfi.ckfTrackCandidates.clone(
    src = cms.InputTag('photonConvTrajSeedFromSingleLeg:convSeedCandidates'),
    clustersToSkip = cms.InputTag('convClusters'),
    TrajectoryBuilderPSet = cms.PSet(refToPSet_ = cms.string('convCkfTrajectoryBuilder'))
)
eras.trackingPhase2PU140.toModify(convTrackCandidates,
    clustersToSkip = None,
    phase2clustersToSkip = cms.InputTag("convClusters")
)

import TrackingTools.TrackFitters.RungeKuttaFitters_cff
convStepFitterSmoother = TrackingTools.TrackFitters.RungeKuttaFitters_cff.KFFittingSmootherWithOutliersRejectionAndRK.clone(
    ComponentName = 'convStepFitterSmoother',
    EstimateCut = 30,
    Smoother = cms.string('convStepRKSmoother')
    )
    
convStepRKTrajectorySmoother = TrackingTools.TrackFitters.RungeKuttaFitters_cff.RKTrajectorySmoother.clone(
    ComponentName = cms.string('convStepRKSmoother'),
    errorRescaling = 10.0
    )

        
# TRACK FITTING
import RecoTracker.TrackProducer.TrackProducer_cfi
convStepTracks = RecoTracker.TrackProducer.TrackProducer_cfi.TrackProducer.clone(
    src = 'convTrackCandidates',
    AlgorithmName = cms.string('conversionStep'),
    Fitter = 'convStepFitterSmoother',
    )


import RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi
convStepSelector = RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi.multiTrackSelector.clone(
    src='convStepTracks',
    trackSelectors= cms.VPSet(
        RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi.looseMTS.clone(
            name = 'convStepLoose',
            applyAdaptedPVCuts = False,
            chi2n_par = 3.0,
            res_par = ( 0.003, 0.001 ),
            minNumberLayers = 3,
            maxNumberLostLayers = 1,
            minNumber3DLayers = 1,
            d0_par1 = ( 5., 8.0 ), # not sure these values are sane....
            dz_par1 = ( 5., 8.0 ),
            d0_par2 = ( 5., 8.0 ),
            dz_par2 = ( 5., 8.0 )
            ),
        RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi.tightMTS.clone(
            name = 'convStepTight',
            preFilterName = 'convStepLoose',
            chi2n_par = 2.5,
            res_par = ( 0.003, 0.001 ),
            minNumberLayers = 3,
            maxNumberLostLayers = 1,
            minNumber3DLayers = 1,
            d0_par1 = ( 5., 8.0 ),
            dz_par1 = ( 5., 8.0 ),
            d0_par2 = ( 5., 8.0 ),
            dz_par2 = ( 5., 8.0 )
            ),
        RecoTracker.FinalTrackSelectors.multiTrackSelector_cfi.highpurityMTS.clone(
            name = 'convStep',
            preFilterName = 'convStepTight',
            chi2n_par = 2.0,
            res_par = ( 0.003, 0.001 ),
            minNumberLayers = 3,
            maxNumberLostLayers = 1,
            minNumber3DLayers = 1,
            d0_par1 = ( 5., 8.0 ),
            dz_par1 = ( 5., 8.0 ),
            d0_par2 = ( 5., 8.0 ),
            dz_par2 = ( 5., 8.0 )
            ),
        ) #end of vpset
    ) #end of clone

ConvStep = cms.Sequence( convClusters 
                         + convLayerPairs
                         + photonConvTrajSeedFromSingleLeg 
                         + convTrackCandidates
                         + convStepTracks
                         + convStepSelector
                         #+ Conv2Step #full quad-seeding sequence
                         )


### Quad-seeding sequence disabled (#+ Conv2Step)
# if enabled, the quad-seeded tracks have to be merged with the single-leg seeded tracks
# in RecoTracker.FinalTrackSelectors.MergeTrackCollections_cff change:
###
#conversionStepTracks = RecoTracker.FinalTrackSelectors.trackListMerger_cfi.trackListMerger.clone(
#    TrackProducers = cms.VInputTag(cms.InputTag('convStepTracks')),
#    hasSelector=cms.vint32(1),
#    selectedTrackQuals = cms.VInputTag(cms.InputTag("convStepSelector","convStep")
#                                       ),
#    setsToMerge = cms.VPSet( cms.PSet( tLists=cms.vint32(1), pQual=cms.bool(True) )
#                             ),
#    copyExtras = True,
#    makeReKeyedSeeds = cms.untracked.bool(False)
#    )
###
# TO this:
###
#conversionStepTracks = RecoTracker.FinalTrackSelectors.trackListMerger_cfi.trackListMerger.clone(
#    TrackProducers = cms.VInputTag(
#                                   cms.InputTag('convStepTracks'),
#                                   cms.InputTag('conv2StepTracks')
#                                   ),
#    hasSelector=cms.vint32(1,1),
#    selectedTrackQuals = cms.VInputTag(
#                                       cms.InputTag("convStepSelector","convStep"),
#                                       cms.InputTag("conv2StepSelector","conv2Step")
#                                       ),
#    setsToMerge = cms.VPSet( cms.PSet( tLists=cms.vint32(0,1), pQual=cms.bool(True) )
#                             ),
#    copyExtras = True,
#    makeReKeyedSeeds = cms.untracked.bool(False)
#    )
###
