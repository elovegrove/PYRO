#!/usr/bin/env python

import math
import os
import sys
import getopt
import sidereal
import ephem
import datetime


# Classes

class Observatory:
    """Class to define a ground-based observatory (i.e. a location, elevation, and timezone on the Earth)"""
    def __init__(self, name):
        name = name.lower()
        self.name = name
        # Lat-long coordinates shamelessly stolen from wikipedia
        if( name=='lco'):  # In honor of FIRE
            self.full_name = "Las Campanas Observatory"
            self.timezone = Timezone(-240.0)
            self.observer = ephem.Observer()
            self.observer.lat = "-29.0146"
            self.observer.lon = "-70.6926"
            self.observer.elevation = 2282.0
                    
        else:
            print 'Bad observatory name (%s) entered.  Aborting...\n' % (name)
 

class Telescope:
    """Class to define a specific telescope at an observatory. Will eventually be used to get more accurate exposure times, slew constraints, etc. For now, unused."""

class Timezone(datetime.tzinfo):
    """Class to provide timezone information to datetime."""
    def __init__(self, offset):
        print "Offset:", offset
        self.offset = datetime.timedelta(minutes=int(offset))

    def utcoffset(self, dt):
        """Return the offset from UTC in minutes."""
        return self.offset

    def dst(self, dt):
        return datetime.timedelta(0)

class Target:
    """Class to define an observation target."""
    def __init__(self, label, name, z, mag, body, weight, exp):
        self.label = label
        self.name = name
        self.z = z
        self.mag = mag
        self.mag_band = None
        self.mag2 = -1.0
        self.mag_band2 = None
        self.weight = weight
        self.exposure = exp
        
        self.body = body

        # Special scheduling properties
        self.priority = False # Is the object a major priority? (input with -P) 
        self.exclude = False # Exclude source from schedule (for example, if it's too close to the Moon)
        self.excl_reason = "N/A" # The reason for excluding this object

        # Other
        self.moon_angle = -1.0 # Angle between this target and the Moon
        self.scheduled_id = "-1"      # ID in the telescope operator's catalogue.  Not filled in until object is scheduled

    def computeNextRising(self, obs, night):
        self.rise_ephem = obs.observer.next_rising(self.body, start=night.start_ephem)
        self.set_ephem = obs.observer.next_setting(self.body, start=night.start_ephem)
        if(self.rise_ephem > self.set_ephem): # Target is already up
            self.rise_ephem = obs.observer.previous_rising(self.body, start = night.start_ephem)
        if(self.rise_ephem > night.end_ephem):
            print "WARNING: Target does not rise during night."
        else:
            if(self.rise_ephem < night.start_ephem):
                self.rise_ephem = night.start_ephem
            if(self.set_ephem > night.end_ephem):
                self.set_ephem = night.end_ephem
        self.am_rise_ephem = self.rise_ephem
        self.am_set_ephem = self.set_ephem
        #print "Target {0} rises at {1}, sets at {2}".format(self.name, self.rise_ephem, self.set_ephem)
    def computeMoonAngle(self, night):
        self.moon_angle = ephem.separation(self.body, ephem.Moon(night.start_ephem))


# Class for one observing night. Ultimately holds master schedule. For now beginning & end default to sunrise/sunset
class Night:
    def __init__(self, dt, obs):
        self.observatory = obs
        self.schedule = ()
        self.start_ephem = obs.observer.next_setting(ephem.Sun(), start=ephem.Date(dt))
        self.end_ephem = obs.observer.next_rising(ephem.Sun(), start=ephem.Date(dt))
        self.start = self.start_ephem.datetime()
        self.end = self.end_ephem.datetime()
        print "Night start {0} {1}, end {2} {3}".format(self.start_ephem, datetimeToString(self.start), self.end_ephem, datetimeToString(self.end))

# Class which controls the output/print-to-screen levels of the program
class OutputLevel:
    def __init__(self, loud_moon, loud_scheduler, loud_priority):
        self.moon = loud_moon # Boolean: print to screen information on the Moon (location, sources proximity to it) ( http://wondermark.com/302 )
        self.scheduler = loud_scheduler # Boolean: print to screen information on the scheduling
        self.priority = loud_priority # Boolean: print to screen information on priority-targets


# Utilities

def usage():
    print "halp"

# Convert a datetime object to a reasonable string.
def datetimeToString(dt):
    return "{0}.{1}.{2} {3}:{4}:{5}".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    

def get_marker_dict():
    
    index_dict = { 'LABEL': None, 'NAME_COL': None, 'REDSHIFT_COL': None, 'RA_COL': None, 'DEC_COL': None, 'MAG_COL': None, 'MAG_COL2': None, 'MAG_BAND': None, 'MAG_BAND2': None,  'MAG_UNKNOWN': None, 'EXP_COL': None, 'COMMENT_COL': None, 'WEIGHT_COL': None, 'RA_DEC_TYPE': None, 'SPEC_COL': None, 'FILTER_COL': None, 'FILTER_VAL': None }
    
    return index_dict

def reset_index_dict( index_dict, targetfile ):
    index_dict['LABEL'] = targetfile
    # Default: Magellan observing catalog
    index_dict['NAME_COL'] = 1
    index_dict['RA_COL'] = 2
    index_dict['DEC_COL'] = 3
    return index_dict

# Determines if the input (vals) line is a "marker" line for the target list; ie, one that contains info on the data stored in each column
def is_marker_line(vals):
    if len(vals) != 0: #make sure line is not empty
        if vals[0] == '###':
            return True
    return False

# Determines if the input (split) line is an empty or comment line (returns False) or not (returns True)
def good_input_line( split_line ):
    if( len(split_line)==0 ): # empty line
        return False
    else:
        if( (split_line[0])[0] == '#' ): # comment line
            return False
        else:
            return True

def read_dict( obj_info, index_dict, marker_name, datatype ):
    col_num = index_dict[marker_name]
    if col_num is None:
        return None
    else:
        col_num = int(col_num)
        return cast(obj_info[col_num], datatype)

def read_dict_maybe_comment( obj_info, index_dict, marker_name, prefix, comment_col, comment, unknown_val, datatype ):
    
    col = index_dict[marker_name]
    if col is not None:
        col = int(col)
        if col != comment_col:
            temp = obj_info[col]
        elif prefix is not None:
            temp = (obj_info[col].split(prefix+"=")[1]).split(";")[0] 
        else:
            print "read_dict_maybe_comment:  Error prefix not set, yet value is supposed to be taken from comment column.  Look at your input file.  Does MAG_COL or MAG_COL2 have the same value as COMMENT_COL?  If so, MAG_BAND or MAG_BAND2 must be set, and the comment column must contain these strings + \'=\' + value"
            return None
        if unknown_val is None:
            return cast(temp,datatype)
        elif unknown_val==temp:
            return None
        else:
            return cast(temp,datatype)
    else:
        return None

def cast( input, datatype ):
    
    if datatype=='f':
        return float(input)
    elif datatype=='i':
        return int(input)
    elif datatype=='s':
        return str(input)



# Calculates the weight to assign the object in the scheduler
def weightTargets(label, z, mag, weight_opt):
    if label=="MG_II":
        if z < 4.7:
            z_weight = 0.25
        elif z >= 4.9:
            z_weight = 0.1
        else:
            z_weight = 0.17
        weight = -1 * (mag - 16.5)/0.1 + (z - 4.4)/z_weight
    elif label=="MG_II_NONSDSS":
        if z < 4.7:
            z_weight = 0.25
        elif z >= 4.9:
            z_weight = 0.1
        else:
            z_weight = 0.17
        weight = -1 * (mag - 18.0)/0.1 + (z - 4.4)/z_weight
    elif label == "Z6_QSO":
        weight = 1 - float(mag)/100
    else: # label == "STD":
        weight = .5
    
    if weight_opt is not None:
        if "M" in weight_opt:
            weight = -1.0*mag
    
    return weight

# Calculate the effective magnitude of a source given the seeing
def adjustMagForSeeing(seeing, mag):
    correlation = {0.4: 0.0769264, 0.5: 0.165862, 0.6: 0.265631, 0.7: 0.414951, 0.8: 0.515353, 0.9: 0.638783, 1.0: 0.638779, 1.1: 0.792101, 1.2: 0.986105, 1.3: 0.986105, 1.4: 0.986101, 1.5: 1.23955, 1.6: 1.23954}
    print mag
    return mag + correlation[seeing]

# Calculate required exposure time based on magnitude of source
def getExpTime(seeing, mag):
    zero_point = 17.0 # Zero point for FIRE
    mag = adjustMagForSeeing(seeing, mag) # mag in Johnson J
    return 100./10.**(-0.4*((mag + 0.95) - zero_point))


# Inputs the name of a target file (or an array of names) and its (their) format(s) (run usage() for more info on file formate), and outputs an initial list of targets
def analyzeSourceList(targetfile, prilist, seeing, Moon, loud, weight_opt):
    
    func_name = "  analyzeSourceList()"
    print "%s: extracting targets from target file = " %(func_name), targetfile
    
    # set minimum exposure time
    exp_min = 60.0
    
    # set the initial maximum scheduling weight
    weight_max = -9999999.9
    
    # ra and dec calculation functions
    #ra_dec_funcs = { 'get_ra_dec_from_SDSS_name': get_ra_dec_from_SDSS_name, 'convert_ra_dec': convert_ra_dec, 'radec_str2float': radec_str2float }
    
    pinds = list()
    
    # check if the file exists
    if os.path.isfile(targetfile)==False:
        print "***** pyro.py: Target file does not exist!  Target file name:", targetfile, "*****"
        print "(You might want to try inputting the target file name with command line argument --target)"
        sys.exit(4)
    # Open the target file
    obj_file = open(targetfile, "r")
    
    # set defaults for column indexing (stored in dictionary)
    index_dict = get_marker_dict()
    
    index_dict = reset_index_dict( index_dict, targetfile )
    
    targets = list()
    
    # Cycle through lines in file
    for line in obj_file:
        print "AnalyzeSourceList:", line
        obj_info = line.split()
        
        if is_marker_line(obj_info): # check if this is a "marker line" (defines what columns are which).  is so, update the appropriate index
            #print "Marker found: ", obj_info
            if obj_info[1] == 'RESET':
                index_dict = get_marker_dict()
                index_dict = reset_index_dict( index_dict, targetfile )
            else:
                index_dict[obj_info[1]] = obj_info[2]
        elif good_input_line(obj_info): # check if this is an object line (ie, neither an empty line nor comment line)
            #print "Object found: ", obj_info
            
            # Determine the target name
            name = read_dict( obj_info, index_dict, 'NAME_COL', 's' )
            
            # Determine the target label
            label = index_dict['LABEL']
            
            # Determine the comment column and comment
            comment_col = index_dict['COMMENT_COL']
            if comment_col is not None:
                comment_col = int(comment_col)
            comment = read_dict( obj_info, index_dict, 'COMMENT_COL' ,'s' )
            
            # Determine the object redshift
            z = read_dict_maybe_comment( obj_info, index_dict, 'REDSHIFT_COL', 'z', comment_col, comment, None, 'f' )
            
            # Determine the magnitude(s)
            mag_band = index_dict['MAG_BAND']
            mag = read_dict_maybe_comment( obj_info, index_dict, 'MAG_COL', mag_band, comment_col, comment, index_dict['MAG_UNKNOWN'], 'f' )
            mag_band2 = index_dict['MAG_BAND2']
            mag2 = read_dict_maybe_comment( obj_info, index_dict, 'MAG_COL2', mag_band2, comment_col, comment, index_dict['MAG_UNKNOWN'], 'f' )
            
            # Determine the spectral type
            sptype = read_dict( obj_info, index_dict, 'SPEC_COL', 's')
            
            # Determine the weight (needed for scheduling priority)
            weight = read_dict(obj_info, index_dict, 'WEIGHT_COL', 'f')
            if weight is None:
                weight = weightTargets(label, z, mag, weight_opt)
            if weight > weight_max:
                weight_max = weight
            
            # Determine the exposure time
            exposure = read_dict(obj_info, index_dict, 'EXP_COL', 'f')
            if exposure is None:
                if label=='STD':
                    exposure = 300.0
                else:
                    exposure = getExpTime(seeing, mag)
            
            if exposure < exp_min and (label=='MG_II' or label=='MG_II_NOSDSS'):
                #print "Increasing exposure for %s from %f to %f" % (name, exposure, exp_min)
                exposure = exp_min
            
            # Determine the RA/Dec
            ra_dec_type = int(index_dict['RA_DEC_TYPE'])
            if ra_dec_type != 2:
                ra = read_dict(obj_info, index_dict, 'RA_COL', 's')
                dec = read_dict(obj_info, index_dict, 'DEC_COL', 's')
                #coords = coordinates.ICRSCoordinates(ra=ra, dec=dec, unit=("hour", "degree"))
            else:
                coord_string = name.replace('SDSSJ', '')
                coord_string = coord_string.replace('SDSS', '')
                ra = coord_string[0:2] + ":" + coord_string[2:4] + ":" + coord_string[4:9]
                dec = coord_string[9:12] + ":" + coord_string[12:14] + ":" + coord_string[14:16]

            body = ephem.FixedBody()
            body._ra = ra
            body._dec = dec
            
            # Add the target to the list
            target = Target(label, name, z, mag, body, weight, exposure)
            
            target.mag_band = index_dict['MAG_BAND']
            target.mag_band2 = index_dict['MAG_BAND2']               
            target.mag2 = mag2
            
            if prilist is not None:
                # Check if this object is one of the highest priority objects
                is_priority = False
                for priority in prilist:
                    if name.find(priority) != -1:
                        is_priority = True
                if is_priority == True:
                    target.priority = True
                    pinds.append(len(targets))
                       
            targets.append(target)
    
    # Close the object file
    obj_file.close()
    
    return [ weight_max, targets ]



# Inputs the name of a target file (or an array of names) and its (their) format(s) (run usage() for more info on file formate), and outputs an initial list of targets
def getTargets(targetfiles, priorities, seeing, Moon, loud, weight_opt):
    func_name = "  getTargets()"
    print "%s: extracting targets from these input target files = " % (func_name), targetfiles
    targets = list()
    pinds = list()
    weight_max = -99999.9
    # Determine the list of priorities
    if priorities is not None:
        if priorities.find(".txt") != -1:  # If this string ends in .txt, then a priority list was entered
            prilist = list()
            prifile = open(priorities, "r")
            for pline in prifile:
                pline = pline.split(" ")
                if good_input_line(pline):
                    # Strip off \n
                    pline = (pline[0].split("\n"))[0]
                    prilist.append(pline)
        else:
            prilist = priorities.split(";")
        if loud.priority==True:
            print "%s: priorities determined to be %s", (func_name, prilist)
    else:
        prilist = None
        if loud.priority==True:
            print "%s: no priority objects found.  use -P or --Priority to enter priority objects." % (func_name)
    # Cycle through all object lists and grab the objects
    for index in range( len(targetfiles) ):
        targetfile = targetfiles[index]
        # Grab all targets from this target file
        [ max1,  targs1 ] = analyzeSourceList(targetfile, prilist, seeing, Moon, loud, weight_opt)
        # Append new targets to the total list
        for target in targs1:
            targets.append(target)
        if max1 > weight_max:
            weight_max = max1
    # Cycle through the absolute highest priority objects (input with -P), and make sure their weights are the highest
    # Determine a weight higher than all the others
    if weight_max <= 0:
        weight_max=10
    else:
        weight_max = weight_max*10.0 
    # Give highest priority objects this weight
    for index, target in enumerate(targets):
        if target.priority == True:
            targets[index].weight = weight_max
            print "%s: Preferred star %s now has a weight = %f" % (func_name, target.name, target.weight)
    return targets



def main(argv):

    #main_window = PyroApp(0)
    #main_window.MainLoop()

    try:
        opts, args = getopt.getopt(argv, "b:e:t:g:a:s:n:P:hcfMl:q:v:w:d:U:", ["start=", "end=", "targetlist=", "granularity=", "airmass=", "seeing=", "nights=", "Priority=", "help", "catalog", "tellurics=", "eaf", "majordome", "Moon", "loud=", "quiet=", "verbose=", "NoMoon", "weight=", "day=", "UToff=", "tmin=", "tmax=", "pureA0V="])
    except getopt.GetoptError:
        print "pyro: Incorrect command line argument fed!  Printing usage() message and exiting..."
        sys.exit(2)


    # Default settings
    prog_name = "  pyro"
    granularity = 5  # Minutes
    airmass = 1.5    # Worst airmass at which to observe
    seeing = 0.6
    nights = 1
    telluric_files = ['Hipparcus_Astars.txt']
    tell_slots = 3 # number of time slots to set aside for tellurics
    eaf = False
    majordome = False
    targetlist = ["z4.cat", "z6.cat"]
    priorities = None
    useMoon = True
    loud_objects = None
    loud = OutputLevel( False, False, False ) 
    weight_opt = ""
    first_day = None
    UToffset = None
    make_catalog = False
    start_time = "1900"
    end_time = "0700"
    tell_min = 8.0
    tell_max = 11.0
    pure_A0V_only = 1 # if 1, then use only stars labeled as A0V (no A0V+'s, etc)

    # Cycle through input command line arguments and update values
    for opt, arg in opts:
        if opt in ("-b", "--start"):
            start_time = int(arg)
        elif opt in ("-e", "--end"):
            end_time = int(arg)
        elif opt in ("-t", "--targetlist"):
            targetlist = arg.split(";")
        elif opt in ("-g", "--granularity"):
            granularity = float(arg)
        elif opt in ("-a", "--airmass"):
            airmass = float(arg)
        elif opt in ("-P", "--Priority"):
            priorities = arg
        elif opt in ("-c", "--catalog"):
            make_catalog = True  # Produce a catalog for the telescope operator
        elif opt in ("-s", "--seeing"):
            seeing = float(arg)
        elif opt in ("-n", "--nights"):
            nights = int(arg)
        elif opt in ("--tellurics"):
            telluric_files = arg.split(";")
        elif opt in ("--eaf"):        # Schedule using an Earliest Arrival First alg.  This usually produces schedules with less slack but may miss high-value targets
            eaf = True
        elif opt in ("-f"):
            explain_file_formats()
            sys.exit(1)
        elif opt in ("-M", "--Moon"):
            useMoon = True
        elif opt in ("--NoMoon"):
            useMoon = False
        elif opt in ("-d", "--day"):
            temp = arg.split("-")
            first_day = [ int(temp[0]), int(temp[1]), int(temp[2]) ]
        elif opt in ("-l", "--loud"):
            if (arg.find("M") != -1):
                loud.Moon = True
            if (arg.find("s") != -1):
                loud.scheduler = True
            if (arg.find("p") != -1):
                loud.priority = True
            if (arg.find("a") != -1):
                loud.Moon = True
                loud.scheduler = True
                loud.priority = True
        elif opt in ("-U", "--UToff"):
            UToffset = float(arg)
        elif opt in("-q", "--quiet"):
            if (arg.find("M") != -1):
                loud.Moon = False
            if (arg.find("s") != -1):
                loud.scheduler = False
            if (arg.find("p") != -1):
                loud.priority = False
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif opt in ("-v", "--verbose"):
            loud_objects = arg.split(";")
        elif opt in ("--tmin"):
            tell_min = float(arg)
        elif opt in ("--tmax"):
            tell_max = float(arg)
        elif opt in ("--pureA0V"):
            pure_A0V_only = int(arg)
        elif opt in ("-w", "--weight"):
            weight_opt = arg
        elif opt in ("--majordome"):
            majordome = True
            eaf = True

    # Grab today's date (Gregorian calendar)
    if first_day is None:
        today = (str(datetime.date.today())).split("-")
        utc = str(datetime.datetime.utcnow())
        first_day = [ int(today[0]), int(today[1]), int(today[2]) ]



    obs = Observatory('LCO')
    start = datetime.datetime(year=2013, month = 6, day = 1, hour = 19, minute=0, tzinfo = obs.timezone)
    end = datetime.datetime(year=2013, month = 6, day = 2, hour = 7, minute=0, tzinfo = obs.timezone)

    night = Night(start, obs)

    # If desired, create the Moon
    if useMoon == True:
        Moon = makeMoon(obs, start, loud)
    else:
        Moon = None

    # Read in the targets and initialize their structures
    targets = getTargets(targetlist, priorities, seeing, Moon, loud, weight_opt)

    # Prepare targets: do airmass calcs, exposure time calcs, and scientific value calcs
    for target in targets:
        #target.night_start = start
        #target.night_end = end
        #getAirmassRange(target, airmass, obs, loud)
        target.computeNextRising(obs, night)
        target.computeMoonAngle(night)
        print "Target %s rise/set (%s, %s) AM rise/set (%s, %s), visible for %f minutes" % (target.name, target.rise_ephem, target.set_ephem, target.am_rise_ephem, target.am_set_ephem, (target.am_set_ephem - target.am_rise_ephem)*24.0*60.0)#            target.moon_angle = target.coordinates.separation(Moon.coordinates)
        #print "Angular distance from Moon:", float(target.moon_angle)
        min_moon_angle = 40.0 * math.pi/180.0
        if target.moon_angle < min_moon_angle:
            print "Warning! Target", target.name, "too close to Moon!"
            target.exclude = True
            target.excl_reason = "Too close to Moon."
        print "Target {0} has weight {1} and requires exposure time {2}.".format(target.name, target.weight, target.exposure)
        if((target.am_set_ephem - target.am_rise_ephem)*24.0*60.0*60.0 < target.exposure):
            print "Warning! Target", target.name, "not visible for longer than required exposure time."
            target.exclude = True
            target.excl_reason = "Not visible long enough to observe."
 





if __name__ == "__main__":
    main(sys.argv[1:])



