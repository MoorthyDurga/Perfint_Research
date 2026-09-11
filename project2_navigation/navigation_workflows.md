# Surgical Navigation Workflows for Spine Surgery

**Version:** 1.0
**Date:** September 7, 2026
**Scope:** Detailed breakdown of surgical navigation workflows, stages, and dependencies

---

## Overview

Modern spine surgical navigation systems follow a structured workflow with distinct stages. This document maps the complete journey from patient presentation to postoperative verification, identifying key dependencies, data flows, and technology touch-points.

---

## 1. Complete Surgical Navigation Pipeline

```

                   COMPLETE SURGICAL WORKFLOW                          


STAGE 1: PREOPERATIVE ASSESSMENT & PLANNING
  
STAGE 2: IMAGING ACQUISITION & PREPROCESSING
  
STAGE 3: SEGMENTATION & ANATOMICAL ANALYSIS
  
STAGE 4: SURGICAL PLANNING & TRAJECTORY DESIGN
  
STAGE 5: OPERATIVE SETUP & PATIENT PREPARATION
  
STAGE 6: IMAGE REGISTRATION & VERIFICATION
  
STAGE 7: INSTRUMENT CALIBRATION & NAVIGATION
  
STAGE 8: INTRAOPERATIVE GUIDANCE & EXECUTION
  
STAGE 9: INTRAOPERATIVE VERIFICATION
  
STAGE 10: CLOSURE & IMMEDIATE POSTOPERATIVE
  
STAGE 11: POSTOPERATIVE VERIFICATION IMAGING
```

---

## 2. Detailed Stage-by-Stage Breakdown

### STAGE 1: PREOPERATIVE ASSESSMENT & PLANNING

**Duration:** 1-7 days before surgery

**Participants:**
- Surgeon
- Radiologist
- Patient

**Key activities:**
1. Patient evaluation (clinical assessment)
2. Pathology identification (tumor, fracture, degeneration)
3. Surgical approach selection (anterior/posterior/lateral)
4. Trajectory/target selection
5. Comorbidity assessment (patient fitness)

**Imaging ordered:**
- High-resolution CT spine (MOST IMPORTANT)
- Optional: MRI for soft tissue detail
- Optional: Functional imaging (PET, SPECT)
- Consider: Patient allergies to contrast

**Decision points:**
- Is imaging adequate for planning
- Are there contraindications (metal implants)
- What approach is optimal

**Output:**
- Decision to proceed with navigation
- Imaging specifications determined
- Estimated surgery date scheduled

**Technology:**
- Electronic medical records (EMR)
- Picture Archiving and Communication System (PACS)
- Surgical scheduling system

---

### STAGE 2: IMAGING ACQUISITION & PREPROCESSING

**Duration:** Hours to days before surgery

**Location:** Radiology department

**Key activities:**

**2A. CT Acquisition:**
```
Step 1: Patient positioning
  - Position in CT gantry
  - Ensure neutral spine (no flexion/extension)
  - Note: Patient position here should match surgical position!

Step 2: Scout scan
  - Quick overview image
  - Plan acquisition limits (from occiput to sacrum typically)

Step 3: Helical acquisition
  - Slice thickness: 0.5-3mm (thin slices preferred)
  - Spacing: <1mm if possible
  - Reconstruction kernel: Bone algorithm
  - Note: Thick slices (>2mm) compromise registration accuracy

Step 4: Review & QA
  - Check image quality
  - Verify spine covered completely
  - Exclude severe artifacts (metal, motion)
```

**2B. Preprocessing:**
```
Step 1: DICOM parsing & organization
  - Extract patient identifiers
  - Verify all slices acquired
  - Sort by anatomical location

Step 2: Orientation standardization
  - Convert to RAS convention (Right-Anterior-Superior)
  - Ensures consistent coordinate system

Step 3: Intensity calibration
  - Map to Hounsfield units (HU)
  - Verify bone/soft tissue HU ranges

Step 4: Artifact assessment
  - Identify metal artifacts
  - Note beam hardening zones
  - Flag severe artifacts for surgeon review
```

**Key concerns:**
- Thick slices hide vertebral details
- Motion artifacts degrade segmentation accuracy
- Metal artifacts (from implants) degrade registration
- Mismatch between CT position and surgical position

**Output:**
- Standardized, artifact-checked CT volume
- Ready for segmentation/planning
- Metadata: slice thickness, spacing, protocol details

**Technology involved:**
- CT scanner
- DICOM viewer
- Preprocessing software (SimpleITK, MONAI, commercial systems)

---

### STAGE 3: SEGMENTATION & ANATOMICAL ANALYSIS

**Duration:** 30 minutes to 2 hours

**Location:** Surgeon's workstation or planning station

**Key activities:**

**3A. Vertebral Segmentation:**
```
Current standard (manual/semi-auto):
  1. Surgeon or technician opens planning software
  2. Loads CT volume
  3. Semi-automatically segments spine (atlas-based)
  4. Manual editing to correct errors
  5. Verify each vertebra segmented correctly

What current systems do:
  - Template matching (align spine template to CT)
  - Edge detection (find vertebra boundaries)
  - Morphological operations (clean up segmentation)
  - Manual override (surgeon corrects errors)

Time required:
  - Fully manual: 60+ minutes (tedious)
  - Semi-automatic: 15-30 minutes (practical)
  - Fully automatic (research): <1 minute (goal)
```

**3B. Vertebral Labeling:**
```
Current standard (manual):
  1. Identify superior anatomical landmark (C1 or T1)
  2. Count vertebrae distally
  3. Assign labels (C1, C2, ..., L5)
  4. Note any variations (fusion, missing vertebrae, etc.)

Challenges:
  - Partial field-of-view (can't see all vertebrae)
  - Similar appearance between thoracic/lumbar transition
  - Anatomical variations (transitional, fusion, missing)
  - Easy to make off-by-one errors

Current error rate:
  - Manual labeling: 2-5% errors
  - Auto+ manual verification: <1% errors

OPPORTUNITY FOR IMPROVEMENT:
  - Automatic labeling could reduce errors to <0.5%
  - Provide confidence estimates
  - Flag anatomical variations
```

**3C. Pathology Detection:**
```
Identify and mark:
  1. Fractures (compression, burst, rotation)
  2. Instrumentation (rods, screws from prior surgery)
  3. Severe degenerative changes
  4. Tumors or lesions
  5. Unusual anatomy

Why important:
  - Affects trajectory planning
  - Influences screw insertion angles
  - Alerts surgeon to challenges
```

**3D. 3D Reconstruction:**
```
Generate 3D spine model:
  1. Volumetric reconstruction
  2. Surface extraction (cortical bone)
  3. Color-code by vertebra
  4. Can rotate/inspect from any angle

Benefit:
  - Better visualization of complex anatomy
  - Easier to spot errors in segmentation
  - Facilitates trajectory planning
```

**Output:**
- Segmented and labeled spine
- 3D reconstruction model
- Pathology annotations
- Verification that labeling is correct

**Time bottleneck:** Segmentation + labeling can take 30+ minutes

**RESEARCH OPPORTUNITY:** Automatic segmentation + labeling  Project 1!

**Technology involved:**
- Navigation planning software (proprietary to each system)
- 3D visualization tools
- DEEP LEARNING could replace manual steps here

---

### STAGE 4: SURGICAL PLANNING & TRAJECTORY DESIGN

**Duration:** 30 minutes to 2 hours

**Location:** Surgeon's workstation

**Key activities:**

**4A. Target Identification:**
```
Determine surgical objective:
  - Pedicle screw insertion targets
  - Vertebral body approach for tumor
  - Kyphoplasty balloon placement
  - Decompression levels

Mark target(s) on 3D model:
  - Vertebra identification
  - Side (left/right) selection
  - Entry point on spine
```

**4B. Trajectory Planning:**
```
For each target:
  1. Define entry point (skin surface)
  2. Define target point (within vertebra)
  3. Compute optimal trajectory
     - Angle relative to vertebral axis
     - Angle relative to surgical approach
     - Considerations: vessel avoidance, nerve avoidance
  4. Visualize trajectory in 3D
  5. Check for collisions with anatomy

Typical constraints:
  - Pedicle screw: Trajectory through pedicle into vertebral body
  - Angle limits: Usually 20-40 depending on procedure
  - Nerve/vessel avoidance: Ensure trajectory doesn't cross
```

**4C. Robotic Parameters (if using robotic system):**
```
For robotic-assisted surgery (e.g., ExcelsiusGPS):
  1. Define robotic arm position
  2. Compute drill angle, depth, speed
  3. Simulate trajectory
  4. Export parameters to robot
```

**Output:**
- Planned trajectory(ies)
- Entry point(s) identified
- Target point(s) identified
- Robotic parameters (if applicable)
- Exported to OR planning station

**Technology involved:**
- 3D visualization software
- Trajectory planning algorithms
- Optional: biomechanical simulation

---

### STAGE 5: OPERATIVE SETUP & PATIENT PREPARATION

**Duration:** 30 minutes to 1 hour

**Location:** Operating room

**Participants:**
- Surgeon
- Surgical staff
- Anesthesia
- Navigation technician

**Key activities:**

**5A. Patient Positioning:**
```
Position patient on operating table:
  - Prone or supine (depends on approach)
  - Head support/positioning
  - Arm positioning
  - Padding at pressure points
  - CRITICAL: Match position to CT planning!
```

**5B. Draping & Surgical Field Preparation:**
```
1. Sterilize surgical site
2. Drape patient (standard surgical draping)
3. Place surface landmarks (fiducials or palpation points)
4. Mark skin entry points (if using navigation)
5. Expose surgical field (skin incision typically minimal for navigation)
```

**5C. Reference Frame Application:**
```
For systems requiring reference frame (StealthStation, Stryker):

  1. Determine frame location (typically sacrum or pelvis)
  2. Secure reference array to patient
     - Percutaneous pins (invasive; StealthStation, Stryker)
     - Adhesive markers (non-invasive; ExcelsiusGPS surface)
  3. Verify frame rigidly attached
  4. Verify clear line-of-sight to OR cameras

For markerless systems (7D Surgical):
  - No reference frame needed
  - Faster setup
```

**5D. Navigation System Positioning:**
```
1. Position OR camera(s) for tracking
2. Verify optimal camera coverage
3. Test camera line-of-sight
4. Boot up navigation computer
5. Verify software connectivity
```

**Output:**
- Patient properly positioned
- Reference frame secure
- Navigation system ready
- Surgical field prepped

**Time consideration:** Takes 15-30 minutes typically

---

### STAGE 6: IMAGE REGISTRATION & VERIFICATION

**Duration:** 10-20 minutes

**Location:** Operating room (patient and navigator workstation)

**Key activities:**

**6A. Registration Procedure:**

```
Goal: Map from CT coordinate system to OR coordinate system

Method 1: Point-based registration (most common)
  1. Identify corresponding points in CT and patient
     - Example: Spinous process tips (palpable via surgical field)
     - Example: Anatomical landmarks visible in CT and surgically accessible
  2. Identify 4-6 corresponding points
  3. Software computes rigid transformation
  4. Result: Alignment between CT and patient anatomy

  Issues:
  - Requires accessible anatomical landmarks
  - Surgeon skill-dependent (accuracy of palpation)
  - Minimum 4 points; more = better accuracy
  - Typical error: 2-4mm

Method 2: Surface-based registration
  1. Acquire intraop imaging (CT, fluoro, or 3D)
  2. Segment spine surface from intraop image
  3. Automatically align with preop CT surface
  4. Software computes alignment

  Advantages:
  - Less operator-dependent
  - Can use more information (entire surface)
  - Better accuracy potential

  Disadvantages:
  - Requires intraop imaging
  - More computationally intensive

Method 3: Fiducial-based registration
  1. Place fiducials (markers) on patient (typically on skin)
  2. Mark fiducial locations in CT during planning
  3. Locate fiducials intraop
  4. Software maps fiducials to registration

  Advantages:
  - Very accurate (if fiducials placed well)
  - Automated detection possible

  Disadvantages:
  - Requires fiducial placement (invasive)
  - May shift during surgery
```

**6B. Registration Verification:**
```
After registration computed:
  1. Overlay CT anatomy on OR imaging (fluoroscopy)
  2. Visually verify alignment
  3. Surgeon checks key points match
     - Pedicles aligned
     - Vertebral bodies aligned
     - Facets in correct position

  If misalignment detected:
  - Repeat registration (add more points)
  - Check patient position (may have moved)
  - Verify reference frame stability

Typical accuracy targets:
  - Registration error <2mm (good)
  - Registration error 2-5mm (acceptable)
  - Registration error >5mm (problematic; redo)
```

**6C. Instrument Calibration:**
```
1. Calibrate navigation probe/instruments
   - Place probe at known point
   - Verify display shows correct coordinates
   - Check orientation registration

2. Test instrument tracking
   - Move instrument; verify tracking smooth
   - Check for jumps or noise

3. Verify probe tip calibration
   - Touch probe tip to known landmarks
   - Verify registration shows correct coordinates
```

**Output:**
- Registration complete and verified
- Instruments calibrated
- Navigation system ready for guidance

**Critical point:** Registration accuracy directly impacts surgical outcome!

---

### STAGE 7: INSTRUMENT CALIBRATION & NAVIGATION SETUP

**Duration:** 5-10 minutes

**Key activities:**

**7A. Probe/Instrument Calibration:**
```
For pointer/probe instruments:
  1. Define probe tip location
  2. Establish pointer axis
  3. Verify calibration accuracy
  4. Practice touching landmarks to verify

For drill guides (ExcelsiusGPS, robotic):
  1. Mount drill guide to robotic arm
  2. Calibrate orientation relative to arm
  3. Verify angle measurements
  4. Test tracking
```

**7B. Navigation Display Setup:**
```
Configure OR monitors:
  1. Display planned trajectory
  2. Display current instrument location
  3. Display anatomy (CT rendered or live imaging)
  4. Display alerts/guidance cues
  5. Brightness/contrast for OR viewing
```

**Output:**
- Navigation system fully configured
- All instruments calibrated
- Surgeon can see real-time guidance

---

### STAGE 8: INTRAOPERATIVE GUIDANCE & EXECUTION

**Duration:** Variable (depends on number of levels)

**This is where the actual surgery happens!**

**Workflow per target:**

```
For each planned trajectory:

STEP 1: Display guidance
  - Show planned trajectory on screen
  - Show current instrument position
  - Show deviation from plan (usually color-coded)

STEP 2: Navigate to start point
  - Move drill guide to entry point
  - Use guidance display to adjust position
  - Verify alignment before drilling

STEP 3: Execute trajectory
  - Drill along planned trajectory
  - Real-time feedback shows deviation
  - Stop drilling at target depth

STEP 4: Insertion
  - Switch to screw/implant insertion
  - Track insertion instrument
  - Verify proper orientation
  - Advance screw to target depth

STEP 5: Repeat for next target
  - Move to next planned trajectory
  - Repeat above steps

Total time per level: 5-15 minutes
  - Robotic assistance: 5-8 minutes faster
  - Manual navigation: Standard surgical timing
```

**Error scenarios & responses:**

```
Scenario 1: Instrument drifts off trajectory
  Response:
  - Navigation shows deviation
  - Surgeon adjusts trajectory
  - Real-time correction before implant placed

Scenario 2: Patient movement during surgery
  Response:
  - Reference frame movement detected
  - Navigation recomputes transformation
  - May require re-registration if shift significant

Scenario 3: Unexpected anatomy (e.g., tumor, vessel)
  Response:
  - Surgeon notes on intraop imaging
  - May modify trajectory slightly
  - Update plan on navigation system
  - Verify new trajectory

Scenario 4: Loss of tracking (markers obscured)
  Response:
  - Navigation alerts loss of tracking
  - Hybrid systems switch to EM tracking
  - If critical: Re-register and resume
```

**Key capabilities enabled by navigation:**
- More consistent screw placement
- Reduced revision surgery
- Smaller incisions possible (more precision)
- Shorter operative time (with practice)
- Improved safety (especially near vessels/nerves)

---

### STAGE 9: INTRAOPERATIVE VERIFICATION

**Duration:** 5-15 minutes

**Key activities:**

**9A. Verification Imaging:**
```
After implants placed, verify positioning:

Option 1: Fluoroscopy (traditional)
  - 2-3 images (AP, lateral, oblique)
  - Quick verification
  - Real-time capability
  - Radiation exposure: Moderate
  - Cost: Low

Option 2: Cone-beam CT (Stryker O-arm, Brainlab iCT)
  - Full 3D volumetric imaging
  - Best assessment of screw position
  - Radiation exposure: Moderate-high
  - Cost: High
  - Time: 2-3 minutes for acquisition/reconstruction

Option 3: Intraop imaging (7D Surgical)
  - Real-time 3D imaging
  - Markerless updating of guidance
  - Best on-the-fly verification
  - Radiation: Variable (can use non-ionizing)

Option 4: No verification (risky)
  - Only if navigation accuracy very high
  - Generally not recommended
```

**9B. Problem Resolution:**
```
If verification shows misplaced implant:
  1. Screw revision needed
  2. May require:
     - Backing out and repositioning screw
     - Larger screw if adjusting position
     - In rare cases: removal and restart
  3. Re-image to verify correction
```

**Output:**
- Verification imaging shows correct placement
- Implants documented
- Radiographic record for follow-up

---

### STAGE 10: CLOSURE & IMMEDIATE POSTOPERATIVE

**Duration:** 15-30 minutes

**Key activities:**

**10A. Final Inspection:**
```
1. Inspect surgical bed for hemostasis
2. Check for retained instruments/materials
3. Verify implant stability
4. Remove reference frame (if used)
5. Evacuate/drain if needed
```

**10B. Closure:**
```
1. Close fascia (if accessed)
2. Close soft tissues in layers
3. Skin closure (sutures, staples, or adhesive)
4. Dressing application
5. Reposition patient if needed
```

**10C. Disconnect Navigation:**
```
1. Remove tracking markers/instruments
2. Shut down navigation system
3. Clean and store equipment
```

**10D. Recovery Area Transfer:**
```
1. Transfer to recovery
2. Monitor for complications
3. Pain management
4. Neurological assessment
```

---

### STAGE 11: POSTOPERATIVE VERIFICATION IMAGING

**Duration:** Hours to days after surgery

**Location:** Radiology department

**Key activities:**

**11A. Follow-up Imaging:**
```
Typical protocol:

Timing 1: Same-day or next-day imaging
  - Verify no immediate complications
  - Check screw positioning
  - Assess for hematoma/infection signs

Timing 2: 6-week follow-up
  - Assess fusion progress (if fusion surgery)
  - Check for implant subsidence
  - Verify stable positioning

Timing 3: 3-month follow-up (if applicable)
  - Assess bone healing
  - Check for complications
```

**11B. Imaging modalities:**
```
- Plain radiographs (X-ray): Quick, minimal radiation
- CT: Best visualization of hardware/bone detail
- MRI: Soft tissue assessment (if no ferromagnetic hardware)
```

**11C. Complication Detection:**
```
Look for:
- Screw position (too medial/lateral can be neurological risk)
- Fracture (iatrogenic or underlying)
- Hematoma (may need drainage)
- Infection signs
- Implant loosening
- Bony union progress
```

**Output:**
- Documentation of successful implantation
- Early complication detection
- Baseline for long-term follow-up

---

## 3. Data Flow Diagram

```

 Preop CT scan    Slice thickness: 0.5-1mm
 Isotropic or nearly isotropic
         
         
    
     Preprocessing & Standardization     
     - Orientation (RAS convention)      
     - Intensity normalization (HU)      
     - Artifact assessment              
    
         
         
    
     SEGMENTATION & LABELING  PROJECT 1
     - Vertebral segmentation           
     - Per-vertebra classification      
     - Pathology detection              
     - [Current: 30+ min manual]         
     - [Goal: <1 min automatic]          
    
         
         
    
     3D Reconstruction & Planning        
     - Generate 3D model                
     - Identify targets                  
     - Plan trajectories                 
     - Export to OR system              
    
         
         
    
     Operative Setup (OR)                
     - Patient positioning              
     - Reference frame/markers          
     - Navigation system boot           
    
         
         
    
     Registration & Verification         
     - Point-based or surface-based    
     - Verify <2mm accuracy             
     - Instrument calibration           
    
         
         
    
     Intraoperative Navigation           
     - Real-time instrument tracking    
     - Trajectory guidance              
     - Position updates                 
     - Error detection/correction       
    
         
         
    
     Intraoperative Verification        
     - Fluoroscopy / cone-beam CT       
     - Confirm screw placement          
    
         
         
    
     Closure & Postoperative             
     - Wound closure                    
     - Initial monitoring               
    
         
         
    
     Postoperative Imaging               
     - Follow-up X-ray, CT, MRI        
     - Complication assessment          
     - Long-term fusion assessment      
    
```

---

## 4. Key Workflow Dependencies

### Critical Success Factors

1. **Image Quality**
   - Thin slices (<1mm)
   - Minimal artifact
   - Complete spine coverage
   - Proper orientation in scanner

2. **Accurate Segmentation**
   - Each vertebra correctly identified
   - Per-vertebra labeling correct
   - No missed vertebrae

3. **Registration Accuracy**
   - Must be <2mm for safety
   - Requires good anatomical landmarks
   - Depends on patient positioning consistency

4. **Real-time Tracking**
   - Requires clear line-of-sight (optical)
   - Reference frame must not move
   - Instruments properly calibrated

5. **Surgeon Skill**
   - Following navigation guidance
   - Recognizing navigation errors
   - Manual trajectory correction if needed

### Common Bottlenecks

1. **Preoperative planning time:** Segmentation + labeling (30-60 min)
   - SOLUTION: Automatic segmentation (Project 1)

2. **Registration errors:** Manual point selection can be inaccurate
   - SOLUTION: Better registration methods; multimodal integration

3. **OR setup time:** Reference frame application, calibration
   - SOLUTION: Markerless tracking; faster setup

4. **Verification time:** Multiple fluoro images for confirmation
   - SOLUTION: Better predictive models; reduce imaging

---

## 5. Workflow Variations by System

### ExcelsiusGPS Workflow (Robot-Centric)

```
Enhanced stages:
  - Robotic trajectory planning (software optimizes)
  - Robotic positioning (arms positions drill guide)
  - Robotic-assisted drilling (surgeon supervises)
  - Real-time trajectory verification

Benefits:
  - More consistent angles/depths
  - No manual drilling (less fatigue)
  - Faster for multiple levels
```

### Stryker + Fluoro Workflow (Fluoroscopy-Integrated)

```
Enhanced stages:
  - C-arm mounted to navigation reference
  - Fluoroscopy overlay on planning
  - Real-time fluoro verification
  - Intraoperative imaging guides corrections

Benefits:
  - Immediate visual feedback
  - Can adjust trajectory before inserting screw
  - Intraoperative imaging as verification
```

### Brainlab Multimodal Workflow (Imaging-Rich)

```
Enhanced stages:
  - Multi-modal registration (CT + MRI fusion in planning)
  - Real-time iCT imaging during procedure
  - Dynamic update of navigation (new images  new coordinates)
  - Most versatile workflow

Benefits:
  - Best verification imaging
  - Multi-modal guidance
  - Most anatomical information
```

### 7D Surgical Workflow (Markerless)

```
Enhanced stages:
  - No reference frame setup
  - Intraoperative 3D imaging as registration source
  - Markerless tracking via deep learning
  - Continuous real-time verification imaging

Benefits:
  - Fastest setup
  - Best real-time verification
  - No line-of-sight camera requirements
```

---

## 6. Research Opportunities Within Workflows

### Opportunity 1: Faster Segmentation & Labeling
- **Current:** 30-60 min manual segmentation + labeling
- **Research goal:** Automatic in <1 min
- **Impact:** 30-60 min time savings per case
- **Implementation:** Project 1 directly addresses this

### Opportunity 2: Better Registration
- **Current:** Point-based registration, ~2-3mm error
- **Research goal:** Automatic registration, <1mm error
- **Impact:** Better surgical accuracy
- **Implementation:** Deep learning-based multimodal registration

### Opportunity 3: Real-Time Navigation Verification
- **Current:** Discrete intraoperative imaging (fluoro, CT)
- **Research goal:** Continuous real-time guidance verification
- **Impact:** Catch errors immediately; fewer corrections
- **Implementation:** 7D approach with continuous imaging

### Opportunity 4: Automatic Complication Detection
- **Current:** Surgeon visually inspects images
- **Research goal:** AI detects complications automatically
- **Impact:** Catches problems early; reduces revision surgery
- **Implementation:** Deep learning on intraoperative images

### Opportunity 5: Markerless Tracking Robustness
- **Current:** 7D pioneering; tracking can fail if anatomy obscured
- **Research goal:** Robust markerless tracking in all scenarios
- **Impact:** Eliminates reference frame setup
- **Implementation:** Improved deep learning pose estimation

---

## Conclusion

Modern surgical navigation systems support a highly structured workflow with distinct stages, clear data dependencies, and multiple technology touch-points.

**Key workflow bottleneck:** Preoperative segmentation/labeling (30-60 minutes)
**Solution:** Project 1 automatic vertebral segmentation & labeling

This workflow mapping demonstrates how vertebral segmentation/labeling represents a critical enabling technology for efficient surgical navigation.

---

**Document prepared:** September 7, 2026
**Status:** Surgical workflow mapping complete
**Next step:** Instrument taxonomy + opportunity analysis
