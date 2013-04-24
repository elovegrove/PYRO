#!/usr/bin/env python

import math
import os
import sys
import getopt
import pickle
import datetime
import astropy
from astropy import coordinates
import sidereal
#import wx

# Classes for the objects

class Observatory:
    """Class to define a ground-based observatory (i.e. a location, elevation, and timezone on the Earth)"""
    def __init__(self, name):
        name = name.lower()
        self.name = name
        # Lat-long coordinates shamelessly stolen from wikipedia
        if( name=='lco'):  # In honor of FIRE
            self.full_name = "Las Campanas Observatory"
            self.lat = coordinates.angles.Angle(-29.0146, unit="degree") # in decimal degrees, - is S, + is N
            self.long = coordinates.angles.Angle(-70.6926, unit="degree") # in decimal degrees, + is E, - is W
            self.timezone = Timezone(-240.0)
            #self.long = 4.0 + 42.0/60.0 + 47.9/3600.0 # in decimal hours (positive is West)
            #self.lst2curr = 4.0 + 16.0/60.0 + 7.0/3600.0  # value added to lst to get current local time (hrs)
            self.altitude = 2282.0
        elif(name=='kpno' or name=="kittpeak"):
            self.full_name = "Kitt Peak National Observatory"
            self.lat = 31.9583
            self.long = 111.5967
            self.altitude = 2120.0
        elif(name=='ctio'):
            self.full_name = "Cerro Tololo Interamerican Observatory"
            self.lat = 30.1652
            self.long = 70.815
            self.altitude = 2215.0
        elif(name=='eso' or name=='lso'):
            self.full_name = "European Southern Observatory - La Silla"
            self.lat = -29.2612
            self.long = 70.7313
            self.altitude = 2347.0
        elif(name=='lick'): # Try not to throw up on your way up to Mt. Hamilton.
            self.full_name = "Lick Observatory"
            self.lat = 37.3414
            self.long = 121.6428
            self.altitude = 1290.0
        elif(name=='mmto'):
            self.full_name = "MMT Observatory"
            self.lat = 31.9583
            self.long = 111.5967
            self.altitude = 2600.0
        ## elif(name=='cfht'):
        ## elif(name=='lapalma'):
        ## elif(name=='mso'):
        ## elif(name=='sso'):
        ## elif(name=='aao'):
        ## elif(name=='mcdonald'):
        ## elif(name=='mtbigelow'):
        ## elif(name=='dao'):
        ## elif(name=='spm'):
        ## elif(name=='tona'):
        ## elif(name=='palomar'):
        ## elif(name=='mdm'):
        ## elif(name=='nov'):
        ## elif(name=='bmo'):
        ## elif(name=='bao'):
        ## elif(name=='keck'):
        ## elif(name=='ekar'):
        ## elif(name=='apo'):
        ## elif(name=='lowell'):
        ## elif(name=='vbo'):
        ## elif(name=='flwo'):
        ## elif(name=='oro'):
        ## elif(name=='lna'):
        ## elif(name=='saao'):
        ## elif(name=='casleo'):
        ## elif(name=='bosque'):
        ## elif(name=='rozhen'):
        ## elif(name=='irtf'):
        ## elif(name=='bgsuo'):
        ## elif(name=='ca'):
        ## elif(name=='holi'):
        ## elif(name=='lmo'):
        ## elif(name=='fmo'):
        ## elif(name=='whitin'):
        ## elif(name=='mgio'):    
            
        else:
            print 'Bad observatory name (%s) entered.  Aborting...\n' % (name)
            sys.exit(2)
#self.timezone = Timezone(self.long.degrees * 4.0)
#self.sidereal = SiderealTime(self.long.degrees * 4.0)
           
 #           if UToffset is not None:
 #               self.UT2curr = float(UToffset)
 #           else:
 #               self.UT2curr = calc_UToff( day[0], day[1], day[2] ) # value added to UT to get current local time (hrs)             #   
 #               print "  pyro.py() Offset between UT and local time not given with -U or --UToff.  Assuming that UT + (%d hrs) = local time." % ( self.UT2curr )
 #           self.ut2lst = calc_UT2lst( day[0], day[1], day[2], 0.0, self.long ) # value added to UT to get lst
 #           self.lst2curr = calc_lst2curr( day[0], day[1], day[2], 0.0, self.UT2curr, self.long )
 
    def details(self):
        print '  Observatory details:\n\tName = %s\n\tLat (decimal degrees) = %f\n\tLong (decimal degrees) = %f\n\tTimezone:%s\n' % (self.full_name, self.lat, self.long, self.timezone.utcoffset())


class Telescope:
    """Class to define a specific telescope at an observatory. Will eventually be used to get more accurate exposure times, slew constraints, etc. For now, unused."""


class Timezone(datetime.tzinfo):
    """Class to provide timezone information to datetime."""
    def __init__(self, offset):
        print "Offset:", offset
        self.offset = datetime.timedelta(seconds=int(offset)*60.0)

    def utcoffset(self, dt):
        """Return the offset from UTC in minutes."""
        return self.offset

    def dst(self, dt):
        return datetime.timedelta(0)


#class SiderealTime(datetime.tzinfo):
#    """Converts between sidereal and solar times at a given location. Abstracts sidereal time as a new 'timezone' for the datetime object."""
#    def __init__(self, offset):
#        self.utcoff = datetime.timedelta(seconds=int(offset)*60.0)
#
#    def utcoffset(self, dt):
#        print "Hour:", dt.hour
#        """Return the offset from UTC in minutes."""
#        julian_date = 367*dt.year - int(7.0*(dt.year+int((dt.month+9)/12))/4) + int(275*dt.month/9) + dt.day + 1721013.5 + dt.hour/24.0 # Assumes UTC date
#        d = julian_date - 2451545.0 # Decimal days since J2000.0
#        
#  # Calculate the Greenwich Mean Sidereal Time in degrees
#        GMST_deg = (280.46061837 + 360.98564736629*d) % 360.0
#        GMST = datetime.timedelta(seconds=GMST_deg*4.0*60.0)
#        #LST = GMST/15.0 * 60.0 - self.utcoff
#        #delta = datetime.timedelta(seconds = datetimeint(GMST*4.0)*60.0 - self.utcoff.seconds)
#        delta = dt - GMST
#        print "Sidereal:", julian_date, d, GMST, GMST_deg, delta
#        return delta
#        #return self.utcoff+self.dst(dt)
#
#    
#    def dst(self, dt):
#        return datetime.timedelta(0)

#    def dst(self, dt):  # This is actually the conversion from solar to sidereal time.
#        #correction = dt.timetuple().tm_yday * 0.98333333 # Number of degrees sidereal lags solar on this date
#        #delta = timedelta(seconds=correction/15.0 * 3600.0)
#        julian_date = 367*dt.year - int(7.0*(dt.year+int((dt.month+9)/12))/4) + int(275*dt.month/9) + dt.day + 1721013.5 + dt.hour/24.0 # Assumes UTC date
#        d = julian_date - 2451545.0 # Decimal days since J2000.0
#        
#  # Calculate the Greenwich Mean Sidereal Time in degrees
#        GMST = (280.46061837 + 360.98564736629*d) % 360.0
#        LST = GMST/15.0 * 60.0 - self.utcoff
#        delta = datetime.timedelta(seconds = int(LST)*60.0)
#         ## d0 = jd0 - 2451545.0
        ## t = d/36525.0
        ## LST_deg = dt.hour*15.0 + dt.minute*0.25 + dt.second*(0.25/60.0)
    
        ## gmst = 6.697374558 + 0.06570982441908*d + 1.00273790935*(d.utcoffset()/60.0) + 0.000026*t

        ## correction_deg = (280.46061837 + 360.98564736629*d) % 360.0
        ## correction = correction_deg/15.0 * 60.0
        ## hours, min_sec = divmod(correction, 60.0)
        ## minutes, seconds = divmod(correction, 1.0)
        ## seconds = seconds * 60.0
        ## delta = timedelta(seconds=correction*60.0)
## return delta
    
    ## def fromutc(self, dt):
    ##     julian_date = 367*dt.year - int(7.0*(dt.year+int((dt.month+9)/12))/4) + int(275*dt.month/9) + dt.day + 1721013.5 + dt.hour/24.0 # Assumes UTC date
    ##     d = julian_date - 2451545.0 # Decimal days since J2000.0
        
    ##     # Calculate the Greenwich Mean Sidereal Time in degrees
    ##     GMST = (280.46061837 + 360.98564736629*d) % 360.0
    ##     LST = GMST/15.0 * 60.0 - self.utcoffset
    ##     hours, min_sec = divmod(LST, 60.0)
    ##     minutes, seconds = divmod(min_sec, 1.0)
    ##     seconds = seconds * 60.0
    ##     dt.replace(hour=hours, minute=minutes, second=seconds)
        
    ##     return dt
        

class Target:
    """Class to define an observation target."""
    def __init__(self, label, name, z, mag, coordinates, weight, exp):
        self.label = label
        self.name = name
        self.z = z
        self.mag = mag
        self.mag_band = None
        self.mag2 = -1.0
        self.mag_band2 = None
        self.coordinates = coordinates
        #self.ra = ra
        #self.dec = dec
        self.sptype = None
        self.weight = weight

        # Absolute rising and setting properties of the source (not modified for the observation window)
        self.rise_time = datetime.datetime.today()
        self.set_time = datetime.datetime.today()
        self.real_used = -1.0

        # Rise and set times modified for airmass constraints
        self.am_rise_time = datetime.datetime.today()
        self.am_set_time = datetime.datetime.today()
        self.am_vis = 0

        self.exp = exp # seconds
        self.start_observation = datetime.datetime.today()  # Elapsed time (in minutes) when observation starts.  To be filled in by scheduler
        self.end_observation = datetime.datetime.today()    # Elapsed time (in minutes) when observation finishes.  To be filled in by scheduler
        self.night_start = datetime.datetime.today() # Local time (hhmm) of the start of the full night's observation run (not just this source)
        self.night_end = datetime.datetime.today() #  Local time (hhmm) of the end of the full night's observation run (not just this source)
        self.airmass = -1 # Estimated airmass at the central scan time.

        # Special scheduling properties
        self.priority = False # Is the object a major priority? (input with -P) 
        self.exclude = False # Exclude source from schedule (for example, if it's too close to the Moon)
        self.excl_reason = "N/A" # The reason for excluding this object

        # Telluric properties
        self.num_tells = 0 # Number of tellurics found for this source
        self.tell_slots = 0 # Number of time slots to devote to tellurics
        self.tellurics = list()     # List of nearby telluric stars.  Don't fill this in until object is scheduled (time matters)
        self.tell_comp_vals = 0 # If this object is a target (ie, not a telluric), these describe how well its tellurics match it

        # Other
        self.moon_angle = -1.0 # Angle between this target and the Moon

        self.scheduled_id = "-1"      # ID in the telescope operator's catalogue.  Not filled in until object is scheduled

        # Prints out the details of all the information stored in the target structure
    def details(self):
        output = "\n  Details for source %s (object type = %s)\n" % ( self.name, self.label )
        output += "  ****************************************************\n"

        output += "  General Properties:"
        output += "    Right Ascension = %f hrs\n" % ( self.ra )
        output += "    Declination = %f degrees\n" % ( self.dec )
        output += "    Angular distance from Moon (in degrees) = "
        if self.moon_angle < 0.0:
            output += " unknown (use -M or --Moon to turn on Moon option)\n"
        else:
            output += "%2.2f degrees\n" % (self.moon_angle)
        output += "    Redshift = "
        if self.z < 0.0:
            output += "unknown\n"
        else:
            output += "%2.2f\n" % ( self.z )
        output += "    Magnitude = "
        if self.mag <= 0.0:
            output += "unknown\n"
        else:
            output += "%2.2f (band = " % ( self.mag )
        if self.mag_band is None:
            output += "unknown)\n"
        else:
            output += "%s)\n" % ( self.mag_band )
        output += "    Magnitude (2nd band) = "
        if self.mag2 <= 0.0:
            output += "unknown\n"
        else:
            output += "%2.2f (band = " % ( self.mag2 )
        if self.mag_band2 is None:
            output += "unknown)\n"
        else:
            output += "%s)\n" % ( self.mag_band2 )
        output += "    Required exposure time = %3.2f secs\n" % ( self.exp )

        output += "  Airmass properties:\n"
        output += "    Airmass used for rising/setting times = "
        if self.real_am_used < 0.0:
            output += "unknown\n"
        else:
            output += "%2.2f\n" % ( self.real_am_used )
        output += "    Rising time = "
        if self.real_am_rise < 0:
            output += "unknown\n"
        else:
            output += "%d (hhmm)\n" % ( self.real_am_rise )
        output += "    Setting time = "
        if self.real_am_set < 0:
            output += "unknown\n"
        else:
            output += "%d (hhmm)\n" % ( self.real_am_set )

        output += "  Observation details (general):\n"
        output += "    Start of night's observation = %d (hhmm)\n" % ( self.night_start )
        output += "    End of night's observation = %d (hhmm)\n" % ( self.night_end )

        output += "  Observation details (specific to target):\n"
        output += "    Target's scheduling weight: %4.3f\n" % ( self.weight )
        output += "    Is this target a priority (ie, input with -P or --Priority flag)? %s\n" % ( boolean2yesno( self.priority ) )
        output += "    Is this target automatically excluded? %s (Reason: %s)\n" % ( boolean2yesno( self.exclude ), self.excl_reason )
        output += "    Airmass rise time (modified by observation window) = %d (hhmm)\n" % ( self.am_rise )
        output += "    Airmass set time (modified by observation window) = %d (hhmm)\n" % ( self.am_set )
        output += "    Total time up within observation window = "
        if self.am_vis==-1:
            output += "never up\n"
        else:
            output += "%d\n" % ( self.am_vis )
        output += "    Number of time slots set aside for telluric observation = %d\n" % ( self.tell_slots )
        output += "    Scheduled observation start time = %d (hhmm after observation start)\n" % ( self.start_observation )
        output += "    Scheduled observation end time = %d (hhmm after observation start)\n" % ( self.end_observation )

        output += "  Properties of matched tellurics:\n"
        output += "    Number of tellurics found for this source = %d\n" % ( self.num_tells )
        if self.num_tells > 0:
            output += "    Information on best  matched tellurics (and comparison values):\n"
         #for tell_num in range(0,self.num_tells):
         #    output += self.telluric_catalog_entry(tell_num)
        output += "    ****************************************************"
        output += self.tell_details()
        output += "    ****************************************************\n"

        return output

    def tell_details(self):

        if self.num_tells==0:
            output = "\n %s: Didn't try to find tellurics for this object.\n" % (self.name)
        else:
            tcv = self.tell_comp_vals[0]
        output = "\n  %s:  RA= %s, Dec= %s  airmass= %4.3f at lst %s\n" % (self.name, dechrs2hhmmss(self.ra,True), deg2degmmss(self.dec,True), tcv.src_am, dechrs2hhmmss(tcv.src_time, True))
        output += "    Best telluric matches:\n"
        for tell_num in range(0, len(self.tellurics)):
            output += self.tell_details1(tell_num)

        return output

    def tell_details1(self, tell_num):
        tell = self.tellurics[tell_num]
        tcv = self.tell_comp_vals[tell_num]
        output  = "      (%d): %s\n" % ( tell_num+1, tell.name )
        ra = dechrs2hhmmss(tell.ra, True)
        dec = deg2degmmss(tell.dec, True)
        output += "          Mag= %3.2f " % ( tell.mag )
        if tell.mag_band is not None:
            output += "(Band= %s)" % ( tell.mag_band )
        else:
            output += "(Band = Unknown)"
        output += "  RA= %s  Dec= %s  Anguler Offset= %2.2f deg\n" % (ra, dec, tcv.dphi)
        output += "          This telluric: airmass = %4.3f at lst %s    airmass diff from source = %4.3f.  Match rating = %4.2f\n" % (tcv.tell_am, dechrs2hhmmss(tcv.tell_time, True), tcv.da, tcv.rating)

        return output

# Return a string containing a line formatted for a Magellan telescope operator's catalog.  comment=Boolean: write a comment column?
    def catalog_entry(self, comment):
        seconds = (self.ra % 1) * 3600.0
        ra = "%02d:%02d:%04.1f" % (int(math.floor(self.ra)), int(math.floor(seconds/60)), seconds % 60)

        if str(self.dec)[0] == "-":
            sign = "-"
        else:
            sign = "+"
        seconds = (abs(self.dec) % 1) * 3600.0
        dec = sign + "%02d:%02d:%04.1f" % (int(math.floor(abs(self.dec))), int(math.floor(seconds/60)), seconds % 60)

        entry = self.scheduled_id + "    "
        entry += str(self.name).ljust(25, " ")
        entry += ra + "    "
        entry += dec + "    "
        entry += "2000.0 0.0 0.0 -0.2 HRZ 00:00:00 00:00:00 2000.0 00:00:00 00:00:00 2000.0	"
        if comment == True:
            if self.z is None:
                z_str = "N/A"
            else:
                z_str = "%4.2f" % self.z
            comment = "%s;z=%s;weight=%5.3f;exp=%5.1f\n" % (self.label,z_str,self.weight,self.exp)
            entry += comment
        return entry

    def telluric_catalog_entry(self, tell_num):

        tcv = self.tell_comp_vals[tell_num]
        entry = self.tellurics[tell_num].catalog_entry(False)
        if self.tellurics[tell_num].mag_band2 is not None:
                if self.tellurics[tell_num].mag2 is not None:
                        comment = "Tell;da=%4.2f;dphi=%4.2f;%s=%3.2f;%s=%3.2f;score=%4.2f\n" % (tcv.da, tcv.dphi, self.tellurics[tell_num].mag_band, self.tellurics[tell_num].mag, self.tellurics[tell_num].mag_band2, self.tellurics[tell_num].mag2, tcv.rating)
                else:
                        comment = "Tell;da=%4.2f;dphi=%4.2f;%s=%3.2f;%s=?;score=%4.2f\n" % (tcv.da, tcv.dphi, self.tellurics[tell_num].mag_band, self.tellurics[tell_num].mag, self.tellurics[tell_num].mag_band2, tcv.rating)
        else:
                comment = "Tell;da=%4.2f;dphi=%4.2f;%s=%3.2f;score=%4.2f\n" % (tcv.da, tcv.dphi, self.tellurics[tell_num].mag_band, self.tellurics[tell_num].mag, tcv.rating)
        entry += comment

        return entry


# Class for comparing tellurics to targets
class tell_comp_vals:
    def __init__(self, index, src, src_time, src_am, tell_time, tell_am, da, dphi):
        self.index = index # The index of the telluric before sorting
        self.src = src # The name of the source that the below comp values correspond to
        self.src_time = src_time # The time at which the airmass of the source was evaluated
        self.src_am = src_am
        self.tell_time = tell_time # The time at which the airmass of the telluric was evaluated
        self.tell_am = tell_am
        self.da = da # The difference in airmass between this telluric and the above source at the above times
        self.dphi = dphi # The angular difference (in degrees) on the sky between this telluric and the above source
        self.rating = rate_tell(da,dphi) # The rating

    def details(self):
        print 'index=%d, src=%s, src_time=%2.2f, tell_time=%2.2f, src_am=%2.2f, tell_am=%2.2f, am_diff=%2.2f ang_diff=%2.2fdeg match_rating=%2.2f' % (self.index, self.src, self.src_time, self.tell_time, self.src_am, self.tell_am, self.da, self.dphi, self.rating)


# Class which controls the output/print-to-screen levels of the program
class OutputLevel:
    def __init__(self, loud_moon, loud_scheduler, loud_priority):
        self.moon = loud_moon # Boolean: print to screen information on the Moon (location, sources proximity to it) ( http://wondermark.com/302 )
        self.scheduler = loud_scheduler # Boolean: print to screen information on the scheduling
        self.priority = loud_priority # Boolean: print to screen information on priority-targets



# Classes for the GUI

## class MainWindow(wx.Frame):

##     def __init__(self, parent, id, title):
##         wx.Frame.__init__(self, parent, id, title, size=(1024, 768))
##         self.CreateStatusBar()

##         filemenu = wx.Menu()
##         #filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
##         #filemenu.AppendSeparator()
##         menu_exit = filemenu.Append(wx.ID_EXIT, "E&xit")
##         menu_open = filemenu.Append(wx.ID_OPEN, "&Open")

##         self.Bind(wx.EVT_MENU, self.OnOpen, menu_open)
##         self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)

##         helpmenu = wx.Menu()
##         helpmenu.Append(wx.ID_ABOUT, "&About")

##         menubar = wx.MenuBar()
##         menubar.Append(filemenu, "&File")
##         menubar.Append(helpmenu, "&Help")
##         self.SetMenuBar(menubar)
##         self.Show(True)

##     def OnExit(self,e):
##         self.Close(True)

##     def OnOpen(self,e):
##         """ Open a file"""
##         dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
##         if dlg.ShowModal() == wx.ID_OK:
##              self.filename = dlg.GetFilename()
##              self.dirname = dlg.GetDirectory()
##              f = open(os.path.join(self.dirname, self.filename), 'r')
##              self.control.SetValue(f.read())
##              f.close()
##         dlg.Destroy()


## class PyroApp(wx.App):
##     def OnInit(self):
##         frame = MainWindow(None, -1, "Hello World!")
##         frame.Show(True)
##         self.SetTopWindow(frame)

##         return True







def convertTimeToDegrees(time):
    """Convert a time/datetime object into decimal degrees"""
    return time.hour*15.0 + time.minute/4.0 + time.second/(4.0*60.0)


def convertDegreesToTime(degrees):
    """Convert an angle into a time object"""
    hours, min_sec = divmod(degrees, 15.0)
    minutes, seconds = divmod(degrees, 0.25)
    seconds = seconds * 240.0
    return datetime.time(hour=hours, minutes=minutes, second=seconds)


# Inputs True or False, and outputs 'yes' or 'no', respectively
def boolean2yesno( input ):
    if input== True:
        out = "yes"
    else:
        out = "no"
    return out

# Utils for airmass calcs

def lst2curr( lst, tscope ):
    return make0to24(lst + tscope.lst2curr)

# Inputs a target structure with an SDSS name and determines the ra and dec from the name
def get_ra_dec_from_SDSS_name( src ):

    name = src.name
    name = name.replace('SDSSJ','')
    name = name.replace('SDSS','')
    h = float(name[0:2])
    m = float(name[2:4])
    s = float(name[4:9])
    src.ra = h + m/60.0 + s/3600.0
    d = float(name[9:12])
    if(name[9] == "-"):
        neg = -1.0
        d = -1.0*d
    else:
        neg = 1.0
    m = float(name[12:14])
    s = float(name[14:16])
    src.dec = neg*(d + m/60.0 + s/3600.0)

    return src

# Convert H:M:S/D:M:S to decimal hours/degrees
def convert_ra_dec(src):
    # Does the input value have seconds attached?
    
    #print src.ra
    #print len(src.ra)
    #print len((src.ra.split("."))[0])

    #print "src.ra = ", src.ra

    # Calculate the decimal RA
    ra = float(src.ra.replace(':',''))

    # Determine if seconds are included
    if len((src.ra.split("."))[0])==4:  # secs aren't included...
        h = float(int(ra)/100)
        m = ra - h*100.0
        s = 0.0
        #print h, m
    else:
        h = float(int(ra)/10000)
        m = float((int(ra) % 10000)/100)
        s = ra - h*10000.0 - m*100.0
        #print h, m, s

    src.ra = h + m/60.0 + s/3600.0

    # print "orig dec =", src.dec

    # Calculate the decimal Dec
    dec = src.dec.replace(':','')

    # Determine if arc seconds are included
    num_digs = len((src.dec.split("."))[0])
    sign_incl = ( dec[0]=='-' or dec[0]=='+' )

    # Remove the initial sign
    if(dec[0] == "-"):
        neg = -1.0
        dec = -1.0*float(dec)
    else:
        neg = 1.0
        dec = float(dec)

    if (num_digs==5 and sign_incl==True) or (num_digs==4 and sign_incl==False): # no arcsecs included
        deg = float(int(dec)/100)
        m = dec - deg*100.0
        s = 0.0
        #print deg, m
    else:
        deg = float(int(dec)/10000)
        m = float((int(dec) % 10000)/100)
        s = dec - deg*10000.0 - m*100.0
        #print deg, m, s
        
    src.dec = neg * (deg + m/60.0 + s/3600.0)
    
    return src

# Function converts read-in ra and dec strings to floats
def radec_str2float( src ):
    src.ra = float(src.ra)
    src.dec = float(src.dec)
    return src

# Shifts times so that they run between 00.00 and 24.00 (ie, 25.0 shifts to 1.0)
def make0to24( dechrs ):
    while( dechrs >= 24.0 ):
        dechrs -= 24.0
    while( dechrs < 0.0 ):
        dechrs += 24.0
    return dechrs

def getLSTFromRA( ra, ha ):
    return make0to24( ra+ha )

# Converts decimal hours to a string of form hhmmss (or hh:mm:ss if colons==True)
def dechrs2hhmmss( dechrs, colons ):
    dechrs = make0to24( dechrs )
    s = (int)(dechrs*3600.0+0.5)
    h = (int)(s/3600)
    s -= h*3600
    m = (int)(s/60)
    s -= m*60

    if colons== False:
        return '%02d%02d%02d' % (h,m,s)
    else:
        return '%02d:%02d:%02d' % (h,m,s)

def deg2degmmss( deg, colons ):
    if deg < 0.0:
        sign = "-"
        deg = -1.0*deg
    else:
        sign = "+"
    s = (int)(deg*3600.0 + 0.5)
    deg = (int)(s/3600)
    s -= deg*3600
    m = (int)(s/60)
    s -= m*60

    if colons == False:
        return '%s%02d%02d%02d' % (sign, deg, m, s)
    else:
        return '%s%02d:%02d:%02d' % (sign, deg, m, s)

# For a given object, calculate the times it is observable at an airmass equal to or better than a certain value
def invertAirmass( airmass, obs, target):

    #deg2rad = math.pi/180.0
    one_over_a = 1.0/airmass
    sin_dec = math.sin(target.coordinates.dec.radians)
    cos_dec = math.cos(target.coordinates.dec.radians)
    sin_lat = math.sin(obs.lat.radians)
    cos_lat = math.cos(obs.lat.radians)

    cos_ha = (one_over_a - sin_dec*sin_lat)/( cos_dec*cos_lat )
    if( cos_ha < -1 or cos_ha > 1 ):
        # print 'WARNING: airmass of %f is unobtainable for source %s\n' % (airmass, src.name)
        target.exclude = True
        target.excl_reason = "Bad Airmass"
    #ha1 = math.acos(cos_ha)*12.0/math.pi
    hour_angle1 = coordinates.angles.Angle(math.acos(cos_ha), unit="radian", bounds=(0, 360))
    hour_angle2 = coordinates.angles.Angle(math.acos(cos_ha)*-1.0, unit="radian", bounds=(0, 360))

    # Determine the observable LST in decimal hours
    rise_angle = hour_angle1 + target.coordinates.ra
    set_angle = hour_angle2 + target.coordinates.ra
    rise_lst = sidereal.SiderealTime(rise_angle.hours)
    set_lst = sidereal.SiderealTime(set_angle.hours)
    am_rise = rise_lst.utc(target.night_start)
    am_set = set_lst.utc(target.night_end)
    am_rise = am_rise.replace(tzinfo=obs.timezone)
    am_set = am_set.replace(tzinfo=obs.timezone)
    print math.degrees(math.acos(cos_ha)), rise_lst, set_lst, am_rise, am_set
    #lst_min = make0to24(src.ra + ha2)
    #hours, minutes = divmod(lst_min, 1.0)
    #rise_lst = datetime(hour=rise_angle.hms[0], minute=rise_angle[1], second=rise_angle[2], tzinfo=obs.sidereal)
    #set_lst = datetime(hour=set_angle.hms[0], minute=set_angle[1], second=set_angle[2], tzinfo=obs.sidereal)
                         
   # lst_min = getLSTFromRA(ra,ha2)
   # lst_max = getLSTFromRA(ra,ha1)

    # Determine the current time in decimal hours
   # am_rise = rise_lst.astimezone(obs.timezone)
   # am_set = set_lst.astimezone(obs.timezone)
   # curr_min = lst2curr( lst_min, tscope )
   # curr_max = lst2curr( lst_max, tscope )

    # Convert these to the form hhmmss
    #curr_min = dechrs2hhmmss( curr_min, False )
    #curr_max = dechrs2hhmmss( curr_max, False )
    return (am_rise, am_set)
    #return ( curr_min, curr_max  )


# Utils for tellurics

# Calculates the position of a source on the celestial sphere at local sidereal time lst
def getSphericalVec( src, lst ):
    return [ math.cos(h2r(getHourAngle(lst,src.ra)))*math.cos(d2r(src.dec)), math.sin(h2r(getHourAngle(lst,src.ra)))*math.cos(d2r(src.dec)), math.sin(d2r(src.dec))]

# The quality of match rating for a telluric with airmass difference da and angular difference dphi
def rate_tell(da,dphi):
    value = airmass_weight(da)*dist_weight(dphi) 
    return float(value)

# A weighting factor needed for rate_tell which describes how well the airmasses of the telluric and source match
def airmass_weight(da):
    max_val = 1.0/0.01
    value = 1.0/math.fabs(da)
    if( value>max_val ):
        return max_val
    else:
        return value

# A weighting factor needed for rate_tell which describes how well the angular positions of the telluric and source match
def dist_weight( angle ):
    cut1 = 20.0
    cut2 = 40.0
    if( angle < cut1 ):
        return 1.0
    elif( angle < cut2 ):
        return -1.0/(cut2-cut1)*(angle-cut1) + 1.0
    else:
        return 0.0

# Inputs two targets, and outputs the angular difference between the two on the sky
def angle_between( src1, src2 ):
    [r1,r2,r3] = getSphericalVec( src1, 0.0 )
    [s1,s2,s3] = getSphericalVec( src2, 0.0 )
    return 180.0/math.pi*math.fabs(math.acos( r1*s1 + r2*s2 + r3*s3 ))

# Inputs the local sidereal time and right ascension of an object, and outputs its hour angle
def getHourAngle( lst, ra ):
    return convertTimeToDegrees(lst) - ra

# Converts the input degrees to radians
def d2r( deg ):
    return deg*math.pi/180.0

# Converts the input hour to radians
def h2r( hour ):
    return hour*math.pi/12.0

# Inputs telescope location, a target (equipped with its position on the sky) and a local sidereal time, and outputs the airmass
def getAirmass( src, obs, lst ):
    ha = getHourAngle( lst, src.ra )
    cos_phi = math.cos(h2r(ha))*math.cos(d2r(src.dec))*math.cos(d2r(obs.lat)) + math.sin(d2r(src.dec))*math.sin(d2r(obs.lat))
    return 1.0/cos_phi

# Inputs an hour angle and two quantities "quant1" and "quant2", and outputs an airmass
# quant1 and quant2 are continually re-calculated if get_airmass is called instead
def get_airmass_from_quants( ha, quant1, quant2 ):
    cos_phi = math.cos(h2r(ha))*quant1 + quant2
    return 1.0/cos_phi

# Finds the best 'num_tells' tellurics for target 'src' from the tellurics listed in 'all_tellurics' using rate_tell().  The airmass of the source ('airmass'), which is calculated at the central time of the source's scan ('central_lst') is compared to the airmass of the telluric, calculated in this function at the central scan time of the telluric ('lst') using the quantities 'quant1_tells' and 'quant2_tells' (which saves repeated calculation of these quantities).
def find_tellurics_1src( src, central_lst, airmass, all_tellurics, quant1_tells, quant2_tells, lst, num_tells ):

    # results is a tell_comp_vals structure, which will hold information on how well all these tellurics match the source
    results = list()

    # Calculate the airmasses and angular difference of all tellurics
    for index, tell in enumerate(all_tellurics):
        airmass_tell =  get_airmass_from_quants( getHourAngle(lst,tell.ra), quant1_tells[index], quant2_tells[index] )
        da = (airmass - airmass_tell)
        dphi = angle_between( tell, src )
        temp_comp = tell_comp_vals( index, src.name, central_lst, airmass, lst, airmass_tell, da, dphi )
        results.append( temp_comp )

    # Rank the list
    results.sort(key=lambda x: x.rating, reverse=True)

    # Carve off the num_tells best solutions
    output_tells = list()
    output_comps = list()

    debug = 0
    if debug:
        print src.name
        for spot, result in enumerate(results):
            print spot, result.rating, result.index, result.da, result.dphi
            print result.src_time, result.tell_time

        sys.exit(3)

    for spot, result in enumerate(results[0:num_tells]):
        index = result.index
        tell2add = all_tellurics[ index ]
        tell2add.is_telluric = True
#        tell2add.tell_comp_vals = copy_tcvs(result)
        output_tells.append(tell2add)
#        print "airmass now is ", tell2add.tell_comp_vals.src_am
        output_comps.append(result)
#        print spot
#        output_tells[spot].details()
#        output_comps[spot].details()
            
    return [output_tells, output_comps]

def find_closest_tellurics( all_sources, telluric_filenames, site, pure_A0V_only, mag_min, mag_max, num_tells, tell_slots, Moon, obj_lsts, tell_lsts ):
# obj_lsts: the lsts at which to evaluate the airmasses of the objects, one for each object.  If None, then the lsts are calculated from scheduling information stored in the target structures
    func_name = "  find_closest_tellurics()"

    num_files = len(telluric_filenames)
    all_tellurics = get_tellurics(telluric_filenames, pure_A0V_only, mag_min, mag_max, Moon)
    num = len(all_tellurics)

    if num_files > 0:
        print '%s: Found %d possible tellurics in all (%d files)' % (func_name, num, num_files)

    # Padding inserted in object's scan duration for telluric
    tell_padding = 10

    # Calculate the starting time for the full night's scan in decimal hours
    if len(all_sources) != 0:
        src = all_sources[0]
        start_time = float( int(src.night_start) / 100 ) + float( int(src.night_start) % 100 )/60.0

    # Calculate cos(dec)*cos(lat) and sin(dec)*sin(lat) for all tellurics
    quant1_tells = list()
    quant2_tells = list()
    for tell in all_tellurics:
        quant1_tells.append( math.cos(d2r(tell.dec))*math.cos(d2r(site.lat)) )
        quant2_tells.append( math.sin(d2r(tell.dec))*math.sin(d2r(site.lat)) )

    output_tells = list()
    output_comps = list()
    for src_num, src in enumerate(all_sources):

        use_tells = True
        if src.label == 'STD' or src.label == 'Asteroid':
            use_tells = False
        if use_tells == True:
            # Determine the source's central scan time in lst
            if obj_lsts is None:
                central_loc_time = start_time + (src.start_observation + ((src.end_observation - tell_padding) - src.start_observation)/2 )/60.0
                central_lst = central_loc_time - site.lst2curr
            else:
                central_lst = obj_lsts[src_num]

            # Calculate the airmass of the source at its central scan time
            airmass = getAirmass( src, site, central_lst )
            src.airmass = airmass

            # Determine the telluric's central scan time in lst
            if tell_lsts is None:
                loc_time = start_time + (src.end_observation - tell_padding/2)/60.0 # There's already padding in the observation time for the telluric
                lst = loc_time - site.lst2curr
            else:
                lst = tell_lsts[src_num]
            # print "find tell lst  = %f central_lst = %f\n" % (lst, central_lst)
            # print "central_lst = %f, central_loc_time = %f, start_time = %f, src.start = %f, src.end = %f" % (central_lst, central_loc_time, start_time, src.start_observation, src.end_observation)
            [ out_tells1, out_comps1 ] = find_tellurics_1src( src, central_lst, airmass, all_tellurics, quant1_tells, quant2_tells, lst, num_tells )

            src.tellurics = out_tells1
            src.tell_comp_vals = out_comps1
            if len(out_tells1) < num_tells:
                print "%s:  Not enought tellurics found for %s!  %d requested, %d found." % (func_name, src.name, num_tells, len(out_tells1))
                src.num_tells = len(out_tells1)
            else:
                src.num_tells = num_tells

            src.tell_slots = tell_slots

            output_tells.append( out_tells1 )
            output_comps.append( out_comps1 )
        else:
            src.num_tells = 0
            src.tell_slots = 0

    # Print out all results
    debug = 0
    if( debug==1 ):
        stars = '  ****************************************'
        for src_num, src in enumerate(all_sources):
            print '%s\n  Results for src num = %d, Source details:\n' % (stars, src_num)
            all_sources[src_num].details()
            print '%s\n' % stars
            out_tells1 = output_tells[src_num]
            out_comps1 = output_comps[src_num]
            print '  Telluric details:\n%s\n' % (stars)

            for i in range(0,num_tells):
                print '  telluric match number %d' % (i)
                out_tells1[i].details()
                out_comps1[i].details()
                print '\n'

            print '%s\n\n' % (stars)

    return [ all_tellurics, output_tells, output_comps ]

def hh_mm_ssTOdechrs( input ):
    # Inputs a string of the form 'hh:mm:ss' or 'deg:mm:ss' and outputs decimal hours or decimal degrees, respectively
    [ d_or_h, m, s ] = input.rsplit(':')
    [ d_or_h, m, s ] = [ float(d_or_h), float(m), float(s) ]    
    [ factor, d_or_h ] = deal_with_neg( d_or_h )
    return factor*(d_or_h + m/60.0 + s/3600.0)

def deal_with_neg ( value ):
    if( value < 0.0 ):
        value = -1.0*value
        factor = -1.0
    else:
        factor = 1.0

    return [factor, value] 

def in_range( val, val_min, val_max ):
    return ( val >= float(val_min) and val <= float(val_max) )

def pure_enough( type, pure_A0V_only ):
    return( type=='A0V' or pure_A0V_only==0 )

# Inputs a source ('src') and the Moon ('Moon'), calculates the angular difference between them, and determines whether its less (return 'True') or greater (return 'False') then the input angle 'min_moon_angle' (in degrees).  'loud_Moon' determines if information is printed to screen.
def too_close_to_Moon( src, Moon, min_moon_angle, loud_Moon ):
    if Moon is not None:
        moon_ang = angle_between(src, Moon) 
        bad_moon = ( min_moon_angle > moon_ang )
        if bad_moon == True:
            if loud_Moon==True:
                print "Source %s is too close to the Moon! Only %2.2f degrees away (min allowed is %2.2f)" % (src.name, moon_ang, min_moon_angle)
            src.exclude = True # Exclude this source from the schedule
            src.excl_reason = "Moon"
        else:
            if loud_Moon==True:
                print "Source %s is far enough away from the Moon: %2.2f degrees away (min allowed is %2.2f)" %  (src.name, moon_ang, min_moon_angle)
        src.moon_angle = moon_ang
        return bad_moon
    else:
        src.moon_angle = -1.0
        return False

def usage():
	print "\nWelcome to PYRO's help message To avoid this message, you must:"
	print "  (1): not include the -h flag when running PYRO"
	print "  (2): run PYRO without any incorrect arguments"
	print ""
	print "PYRO is an acronym that stands for 'Planning Your Required Observations'.  It is a multi-purpose tool.  Some of its most useful/important tasks are:"
	print "(1) Converting custom target lists of objects to Magellan catalog format"
	print "(2) Collecting and displaying information on requested objects"
	print "(3) Matching targets to tellurics (although one should consider using find_telluric.py instead)"
	print "(4) Scheduling prioritized observations (needs work)"
	print ""
	print "Command line arguments:"
	print "--------------------------------------------------------------"
	print "\nOptional argumets (and defaults)"
	print " -b, --start: Starting time of run (2400h format)"
	print " -e, --end: Ending time of run (2400h format)"
	print " -d, --day: First day (local calendar day) of schedule.  Default: today, as determined by python's datetime.date.today() function.  (YYYY-MM-DD format)"
	print " -U, --UToff: Number of hours added to UT to get current local time.  Default compensates for Daylight Savings Time (should be accurate from April 4, 2010 until 2020, unless Chile changes its policy), and is printed to screen if used."
	print " -t, --targetlist: File containing target information.  Can input more than one target list; separate by \";\" (ex, --target \"list1.cat;list2.cat\").  (Default is \"z4.cat;z6.cat\").  To learn the proper formatting of the target list files, run pyro.py with the -f flag."
	print " -g, --granularity: Granularity of schedule (default is 5 minutes)"
	print " -a, --airmass: Worst airmass at which to allow observing of a target (default is 1.5)"
	print " -c, --catalog: Write out a catalog for the telescope operator to Mon_DD_YYYY.txt (formatted for LCO/Magellan; 'Mon' is three-letter abbreviation for the month, and 'DD' and 'YYYY' are the day and year, respectively.) (default is off)"
	print " -s, --seeing: Current seeing (affects calculated exposure times) (default is 0.6)"
	print " -n, --nights: Number of nights to schedule (unscheduled targets in one night will be carried over to the next) (default is 1)"
	print " -P, --Priority: Name(s) of absolute highest priority object(s).  (If necessary, bends airmass cutoffs.)  Can input more than one directly to the commandline; separate by \";\" (ex, --priority \"obj1;obj2\").  Alternatively, in the argument of these flags ends in \'.txt\', a text file of the same name is used to determine priority sources.  (Run pyro.py with te -f flag to learn the proper file formatting).  Does not work with --eaf or --majordome.  Might not schedule all priority sources if two highest priority objects peak at the same time."
	print " -v, --verbose: Name(s) of objects for which to print to screen all gathered information on.  Can input more than one; separate by \";\" (ex, --verbose \"obj1;obj2\")."
	print " -M, --Moon: Boolean.  If set, then don't consider sources close to the Moon.  Default: True (use Moon).  Compare with: --NoMoon"
	print " --NoMoon: Boolean.  If set, then do not eliminate sources based upon their proximity to the Moon.  Default: False (use Moon).  Compare with: -M, --Moon." 
	print " --tellurics: Specify a catalog of telluric standard stars (default is Hipparcus_Astars.txt).  To the learn the proper formatting of this input file, run pyro.py with the -f flag."
	print " --tmin: minimum magnitude allowed when matching tellurics.  The band is that specified by MAG_BAND in the tellurics file (run pyro.py with the -f flag to learn more about file formats.  Default = 8.0 (band is assumed V)."
	print " --tmax: maximum magnitude allowed when matching tellurics.  The band is that specified by MAG_BAND in the tellurics file (run pyro.py with the -f flag to learn more about file formats.  Default = 11.0 (band is assumed V)."
	print " --pureA0V: ==0 if variants of A0V stars (exampe, A0V+) are acceptable for tellurics, ==1 if only pure A0V stars are allowed.  Default = 1."

	print " --eaf: Use an Earliest Arrival First alg to schedule.  This tends to produce schedules with less slack, but may miss high-value targets (default is off)"
	print " --majordome: Use the MAJORDOME scheduling alg from Bringer et al 2000.  Implies --eaf. (Default is off)"
	print " -f: Calls explain_file_formats() (and then exits), which prints out a message explaining the proper format of all input files."
	print " -h, --help: Display this usage information and exit.\n"


def explain_file_formats():
	print "\nPYRO's file formatting help message (To avoid this message, don't run PYRO with the -f flag.)"

	print "\n\nProper formatting of the target list files (inut with -t, --targetlist flags)"
	print "--------------------------------------------------------------"
	print "The default format is the standard Magellan telescope operator format.  For convenience, however, it is possible to define your own custom-made format by doing the following:\n"
	print "Custom file formats are read directly from the file itself (assumed to be an ASCII text file), and are stored in lines that begin with \'###\'.  In these lines, the next column defines the attribute type, and the one after gives the relevant value (which is often the column number that contains the relevant information; column numbers start at 0).  Columns after that are ignored.  Below is full list of attribute types via example.  The example file is assumed both to be for Magnesium II quasar targets and to have the following format:\nname redshift ra dec Jmag zmag exposure-time weight code comments\nExample:\n"
	print "### RESET (No other argument necessary) Resets all the below marker values to their default values.  Necessary when more than one list type is included within one target file."
	print "### RA_DEC_TYPE 0 Defines whether units are hh:mm:ss and deg:arcmin:arcsec (==0), decimal (==1), or the sources are SDSS sources and the location is to be read from the name (==2).  MANDATORY."
	print "### RA_COL 2 Defines column that holds the Right Ascension.  MANDATORY if RA_DEC_TYPE is 0 or 1."
	print "### DEC_COL 3 Defines column that holds the Declination.  MANDATORY if RA_DEC_TYPE is 0 or 1."
	print "### NAME_COL 0 Defines column that holds the name of the object.  MANDATORY."
	print "# All other source list keywords are optional.  If not provided, the code attempts to compensate for their absence in various ways.  "
	print "### LABEL MG_II Defines the object label."
	print "### REDSHIFT_COL 1 Defines column that holds the redshift of the object.*"
	print "### MAG_COL 4 Defines column that holds the magnitude.*"
	print "### MAG_BAND Jmag Describes what band is represented by the data in MAG_COL."
	print "### MAG_COL2 5 Defines column that holds a second value of the magnitude.*"
	print "### MAG_BAND2 zmag Describes what band is represented by the data in MAG_COL2."
	print "### EXP_COL 6 Defines column that holds the exposure time."
	print "### WEIGHT_COL 7 Defines the scheduling priority-weight column."
	print "### COMMENT_COL 9 Defines the comment column."
	print "### MAG_UNKNOWN ? Defines the symbol used when a source within the list's magnitude is unknown."
	print "### FILTER_COL 8 Defines a column used to filter data (optional)."
	print "### FILTER_VAL a;b;c; Semi-colon separated list of acceptable values to by pass the filter."

	print " *if REDSHIFT_COL==COMMENT_COL, MAG_COL==COMMENT_COL, or MAG_COL2==COMMENT_COL, then the redshift and/or magnitudes are expected to be separated from the other comments by semi-colons and preceded by \'z=\' and/or \'MAG_COL(2)=\', respectively where MAG_COL or MAG_COL2 are the strings defined by the above markers of the same name (for example, \'blah;z=4.5;J=15.7;blah2\' is the correct comment if \'### MAG_BAND J\' is given)"
	print "\nSince the comments in this example would be ignored by the code, feel free to cut and paste this section into your target list.  These informational columns need not be placed at the beginning of the file.  Therefore, one could change types midway through a target list (but be careful to reset the defaults using ### RESET!).  Commented (#) and empty lines are ignored."
	print "--------------------------------------------------------------"

	print "\n\nProper formatting of the telluric files (input with --telluric flag)"
	print "--------------------------------------------------------------"
	print "Telluric files follow the same format as Target files, with the catalogue format of the Magellan telescope operators being the default.  The one exception is that telluric files have an extra marker:"
	print "### SPEC_COL 6 (or whatever number)"
	print "This column represents the spectral type of the telluric.  (Target files may use the marker as well, if desired, but it has no effect on the scheduler.)"
	print "--------------------------------------------------------------"

	print "\n\nProper formatting of the priority source files (input with -P, --Priority flags)"
	print "--------------------------------------------------------------"
	print "Priority source files should be ASCII text files with one source name per line.  To determine matches, pyro searches input target names for the substrings contained in these lines.  Thus, full source names are not required (but be careful not to assign priority to less worthy sources by putting a small substring in the priorities file, such as \'SDSS1\', which is likely to match many sources). Commented (#) and empty lines are allowed, and are ignored."
	print "--------------------------------------------------------------"


# Check if mandatory options are given on the commandline
def check_required_opts(argv):
    if (argv.count("-b")==0) and (argv.count("-e")==0):
        print "\n***** pyro.py: Required commandline arguments not provided.*****\n  Printing usage() and exiting..."
        usage()
        sys.exit(3)

# Convert clock time to time elapsed (output is integer minutes)
def timeElapsed(time, start_time):  
    if(time < 1200): # If we're past midnight
        time += 2400
    #print "Time (RST):", time
    start_time = (start_time - start_time % 100) * 60/100 + start_time % 100 
    time = (time - time % 100) * 60/100 + time % 100
    return time - start_time

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

# Calculate total time on target given an exposure time (seconds), a granularity (minutes), and an additional number of time slots to set aside for tellurics (tell_slots)
def getTotalObsTime(exposure, granularity, tell_slots):
    telluric = tell_slots*granularity
    obstime = exposure/60 + 5 + 2.5 # 5 to slew, 2.5 to read
    obstime += telluric
    obstime += (granularity - obstime % granularity)  # Round up to schedule granularity
    return obstime

# Calculate times the object is at a good enough airmass for observing
def getAirmassRange(target, airmass, obs, loud):

    airmass_cut = 2.0 # max airmass cutoff: to help avoid an infinite loop for priority objects
    if airmass > airmass_cut:
        if target.priority==True and loud.priority==True:
            print "getAirmassRange(): Maximum possible airmass of %f reached for target %s.  Giving up on the object..." % (airmass_cut, target.name)
        return

    # For the target in question, determine the rising and setting times relative to the input 'airmass'.
    am_rise, am_set = invertAirmass(airmass, obs, target)

    if am_rise < target.night_start:
        target.am_rise_time = target.night_start
    else:
        target.am_rise_time = am_rise

    if am_set > target.night_end:
        target.am_set_time = target.night_end
    else:
        target.am_set_time = am_set

    target.am_vis = target.am_set_time - target.am_rise_time
    if target.am_vis == 0: # Never rises during the observing window
        target.am_vis = -1

    ## old = 0

    ## if old==0:
    ##     am_rise = int(vis[0][0:4])
    ##     am_set = int(vis[1][0:4])

    ##     # Save these values of the actual airmass rise and set times to the Target structure
    ##     target.real_am_rise = am_rise
    ##     target.real_am_set = am_set
    ##     target.real_am_used = airmass

    ##     # For the sake of the scheduler, we modify these values by imposing the restrictions of our observing window.  We'll do this and store the new values as target.am_rise and target.am_set

    ##     # Make sure that start_time is between 0000 and 2400, and end_time is greater than start_time (end_time is most likely greater than 2400)
    ##     if start_time >= 2400:
    ##         start1 = start_time - 2400
    ##     else:
    ##         start1 = start_time
    ##     if end_time <= start1:
    ##         end1 = end_time+2400
    ##     else:
    ##         end1 = end_time

    ##     # Determine the rising and setting times of the target, relative to the restricted observing time window
    ##     good_rise = intimerange(am_rise,start1,end1)
    ##     good_set = intimerange(am_set,start1,end1)
    ##     if good_rise and good_set:
    ##         target.am_rise = am_rise
    ##         target.am_set = am_set
    ##     elif good_rise:
    ##         target.am_rise = am_rise
    ##         target.am_set = end_time
    ##     elif good_set:
    ##         target.am_rise = start_time
    ##         target.am_set = am_set
    ##     else:
    ##         target.am_rise = target.am_set = end_time


    ##     #    print "name = %s, am_rise = %d, am_set = %d, start = %d, end = %d, final rise = %d, final_set = %d" % (target.name, int(vis[0][0:4]), int(vis[1][0:4]), start_time, end_time, target.am_rise, target.am_set)


    ## if old==1:
    ##     target.am_rise = int(vis[0][0:4])
    ##     target.am_set = int(vis[1][0:4])

    ##     if(target.am_rise > end_time and target.am_rise < start_time):
    ##         if(target.am_set > end_time and target.am_set < start_time):
    ##             target.am_rise = target_am_set = end_time
    ##         else:
    ##             target.am_rise = start_time + 5
    ##     if(target.am_set > end_time and target.am_set < start_time):
    ##         target.am_set = end_time


    ## target.am_vis = timeElapsed(target.am_set, start_time) - timeElapsed(target.am_rise, start_time) # Visibility in decimal number of minutes
    ## #target.am_vis = (target.am_vis - target.am_vis % 60) * 100/60 + target.am_vis % 60  # Uncomment to give visibility range in hhmm
    ## if target.am_vis == 0:  # Object never rises
    ##     target.am_vis = -1

    ## # If the object is absolute highest priority, we may need to bend the rules.  Check to make sure its visibile longer than its exposure time
    ## if target.priority and (target.am_vis*60.0<target.exp):
    ##     airmass = airmass + 0.1
    ##     if loud.priority==True:
    ##         print "getAirmassRange(): extending max acceptable airmass for object %s to %2.2f b/c it\'s a priority" % (target.name, airmass)
    ##     getAirmassRange(target, start_time, end_time, airmass+0.1, site, loud)
    ## target.airmass = airmass
    ## #print "getAirmassRange:", target.am_rise, target.am_set, start_time, end_time

# Outputs True if the input time is between start time and end time when the two straddle midnight
def intimerange( time, start_time, end_time ):
    if time >= start_time and time <= end_time:
        return True
    elif time+2400 >= start_time and time+2400 <= end_time:
        return True
    else:
        return False

# Default scheduler.  Prioritizes by weight and places observations as early as possible.  Does not resolve conflicts.
def scheduleTarget(target, schedule, start_time, granularity, tell_slots, scheduled_targets, unscheduled_targets, loud):

    conflict = None

    [ rise_time, set_time, slots_needed, slots_available ] = get_slot_props( target, start_time, granularity, tell_slots, schedule, loud.scheduler )

#    rise_time = int(math.ceil(timeElapsed(target.am_rise, start_time) - 5)/granularity)
#    print target.name, target.am_rise, start_time, rise_time, timeElapsed(target.am_rise,start_time)
#    print "name = %s, target am_rise = %d, target am_set = %d, target am_vis = %d start_time = %d elapsed = %d" % (target.name, target.am_rise, target.am_set, target.am_vis, start_time, timeElapsed(target.am_rise,start_time))
#    set_time = int(math.floor(timeElapsed(target.am_set, start_time)/granularity))
    #obs_range = schedule[(convertTime(target.am_rise, start_time) - 5)/granularity:convertTime(target.am_set, start_time)/granularity]
    #telluric = 5 + 2.5 + 3 # 5 to slew, 2.5 to read, 3 minute exposure
    #time_req = exposure_time + 5 + 2.5 + telluric # 5 to slew, 2.5 to read, and telluric standard
    #time_req = time_req + (granularity - time_req % granularity) # Round up to scheduling increments
#    slots_needed = int(math.ceil(getTotalObsTime(target.exp, granularity, tell_slots)/granularity))
#    slots_available = schedule[rise_time:set_time].count(None)
#    if slots_available < slots_needed and loud.scheduler:
#        print rise_time, set_time
#        print "Not enough slots available; %d needed, %d available (rise time = %d, set time = %d)." % (slots_needed, slots_available, rise_time, set_time)
#        print "Not enough slots available;", slots_needed, "needed,", slots_available, "available (rise."

    counter = 0
    start = -1
    end = -1
    if loud.scheduler: print "Need %d slots for %s between %d and %d (exp time = %3.1f)" % (slots_needed, target.name, rise_time, set_time, target.exp)
    for i in range(0, set_time - rise_time):
        #print rise_time + i
        if(schedule[rise_time + i] is None):
            if(counter == 0): # We've just started a new block
                start = i
            counter = counter + 1
        else:
            start = -1
            counter = 0
        if(counter is slots_needed): # There are sufficient contiguous slots
            end = i
         #print schedule[rise_time + start:rise_time + end + 1]
            schedule[rise_time + start:rise_time + end + 1] = [target] * slots_needed
            target.start_observation = (rise_time + start) * granularity
            target.end_observation = (rise_time + end) * granularity
            if loud.scheduler: print "Placing in range:", rise_time + start, rise_time + end
            scheduled_targets.append(target)
            return True
    else: # There are not enough contiguous slots
        if loud.scheduler: print "*\t*\t*\tCONFLICT: DID NOT SCHEDULE", target.name,"\n\n"
        if target.priority==True and loud.priority==True:
            print "scheduleTarget(): priority object not scheduled!  Automatically excluded? %s (Reason: %s)" % (boolean2yesno(target.exclude), target.excl_reason)
        unscheduled_targets.append(target)
        return False

# Calculates the weight to assign the object in the scheduler
def calc_schedule_weight(label, z, mag, weight_opt):
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

# Prints the created schedule
def print_schedule( start_time, granularity, schedule, scheduling_night ):

    # Add tellurics to the schedule
    slot_num = 0
    while slot_num < len(schedule):
        slot = schedule[slot_num]
        if slot is None:
            slot_num = slot_num + 1
        else:
            tell_slots = slot.tell_slots
            max_tell_slot = slot.end_observation/granularity
            min_tell_slot = max_tell_slot - tell_slots + 1
            for tell_slot in range (min_tell_slot, max_tell_slot+1):
                schedule[tell_slot] = slot.tellurics[0]
            slot_num = max_tell_slot + 1

    print "Schedule for night %d:" % scheduling_night
    time = start_time
    for slot in schedule:
        if slot is None:
            print time, ": FREE"
        else:
            print time, ":", slot.label, slot.name, slot.exp/60
        time += granularity
        if(time % 100 == 60):
            time -= 60
            time += 100

# Determines if the input (split) line is an empty or comment line (returns False) or not (returns True)
def good_input_line( split_line ):
    if( len(split_line)==0 ): # empty line
        return False
    else:
        if( (split_line[0])[0] == '#' ): # comment line
            return False
        else:
            return True

# Determines if the input (vals) line is a "marker" line for the target list; ie, one that contains info on the data stored in each column
def is_marker_line(vals):
    if len(vals) != 0: #make sure line is not empty
        if vals[0] == '###':
            return True
    return False

def get_marker_dict():

    index_dict = { 'LABEL': None, 'NAME_COL': None, 'REDSHIFT_COL': None, 'RA_COL': None, 'DEC_COL': None, 'MAG_COL': None, 'MAG_COL2': None, 'MAG_BAND': None, 'MAG_BAND2': None,  'MAG_UNKNOWN': None, 'EXP_COL': None, 'COMMENT_COL': None, 'WEIGHT_COL': None, 'RA_DEC_TYPE': None, 'SPEC_COL': None, 'FILTER_COL': None, 'FILTER_VAL': None }
    
    return index_dict

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


# Inputs the name of a target file (or an array of names) and its (their) format(s) (run usage() for more info on file formate), and outputs an initial list of targets
def analyzeSourceList(targetfile, prilist, seeing, Moon, loud, weight_opt):

    func_name = "  analyzeSourceList()"
    print "%s: extracting targets from target file = " %(func_name), targetfile

    # set minimum exposure time
    exp_min = 60.0

    # set the initial maximum scheduling weight
    weight_max = -9999999.9

    # ra and dec calculation functions
    ra_dec_funcs = { 'get_ra_dec_from_SDSS_name': get_ra_dec_from_SDSS_name, 'convert_ra_dec': convert_ra_dec, 'radec_str2float': radec_str2float }

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
                weight = calc_schedule_weight(label, z, mag, weight_opt)
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
                coords = coordinates.ICRSCoordinates(ra=ra, dec=dec, unit=("hour", "degree"))
                #if ra_dec_type == 0:  # given in discrete (ie, hh:mm:ss and deg:arcmin:arcsec) form
                    #radec = 'convert_ra_dec'
                    
                #elif ra_dec_type == 1: # given in decimal form
                    #radec = 'radec_str2float'
            else:
                coord_string = name.replace('SDSSJ', '')
                coord_string = coord_string.replace('SDSS', '')
                coord_string = coord_string[0:2] + ":" + coord_string[2:4] + ":" + coord_string[4:9] + " " + coord_string[9:12] + ":" + coord_string[12:14] + ":" + coord_string[14:16]
                coords = coordinates.ICRSCoordinates(coord_string, unit=("hour", "degree"))

            # Add the target to the list
            #target =  ra_dec_funcs[radec]( Target(label, name, z, mag, ra, dec, weight, exposure) )
            target = Target(label, name, z, mag, coords, weight, exposure)

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

            target.moon_angle = target.coordinates.separation(Moon.coordinates)
            print "Angular distance from Moon:", target.moon_angle
            min_moon_angle = coordinates.angles.Angle("40.0", unit="degree")
            if target.moon_angle.degrees < min_moon_angle.degrees:
                print "Warning! Target", target.name, "too close to Moon!"
                target.exclude = True
                target.excl_reason = "Too close to Moon."
                
            targets.append(target)

    # Close the object file
    obj_file.close()

    return [ weight_max, targets ]

def get_tellurics(tellfiles, pure_A0V_only, mag_min, mag_max, Moon):

	func_name = "  get_tellurics()"

	print "%s: extracting tellurics from these input files = " % (func_name), tellfiles

	tells = list()

	# Cycle through all object lists and grab the objects
	for index in range( len(tellfiles) ):
		tellfile = tellfiles[index]
		# Grab all tellurics from this telluric file
		tells1 = analyze_tell_list(tellfile, Moon)
		print "%s: Found %d tellurics in telluric file %s" % (func_name, len(tells1), tellfile)
		# Append new targets to the total list
		bad_mag=0
		not_pure=0
		filtered=0
		for tell in tells1:
			if tell.mag is None:
				bad_mag = bad_mag + 1
			elif tell.mag < mag_min or tell.mag > mag_max:
				bad_mag = bad_mag + 1
			elif pure_enough(tell.sptype, pure_A0V_only) == False:
				not_pure = not_pure + 1
			elif tell.exclude == True:
				filtered = filtered + 1
			else:
				tells.append(tell)

		print "%s: Rejected %d of the tellurics in %s because of magnitude, %d because of spectral type, and %d because of other filter settings." % (func_name, bad_mag, tellfile, not_pure, filtered)
		print "%s: Kept %d good tellurics." % (func_name, len(tells1)-bad_mag-not_pure)
		print "%s: Cumulative total = %d tellurics" % (func_name, len(tells))

	return tells


# Inputs the name of a telluric file (or an array of names) and outputs an initial list of targets
def analyze_tell_list(tellfile, Moon):

    func_name = "  analyze_tell_list()"
    print "%s: extracting tellurics from telluric file = " %(func_name), tellfile

    # ra and dec calculation functions
    ra_dec_funcs = { 'get_ra_dec_from_SDSS_name': get_ra_dec_from_SDSS_name, 'convert_ra_dec': convert_ra_dec, 'radec_str2float': radec_str2float }

    # check if the file exists
    if os.path.isfile(tellfile)==False:
        print "***** %s: telluric file does not exist!  Telluric file name: %s *****" % (func_name, tellfile)
        print "(You might want to try inputting the telluric file name with command line argument -f)"
        sys.exit(4)

    # Open the telluric file
    obj_file = open(tellfile, "r")

    # set defaults for column indexing (stored in dictionary)
    index_dict = get_marker_dict()
    index_dict = reset_index_dict( index_dict, tellfile )

    tells = list()

    # Cycle through lines in file
    for line in obj_file:

        obj_info = line.split()
        if is_marker_line(obj_info): # check if this is a "marker line" (defines what columns are which).  If so, update the appropriate index
            #print "Marker found: ", obj_info
            if obj_info[1] == 'RESET':
                index_dict = get_marker_dict()
                index_dict = reset_index_dict( index_dict, tellfile )
            else:
                index_dict[obj_info[1]] = obj_info[2]
        elif good_input_line(obj_info): # check if this is an object line (ie, neither an empty line nor comment line)
            #print "Object found: ", obj_info

            # Determine the target label
            label = index_dict['LABEL']
            if label is None:
                label = 'Telluric'

            # Determine the telluric name
            name = read_dict( obj_info, index_dict, 'NAME_COL', 's' )

            if label=='HIPPARCUS':
                name = 'HIP' + name

            # Determine the comment column and comment
            comment_col = index_dict['COMMENT_COL']
            if comment_col is not None:
                comment_col = int(comment_col)
            comment = read_dict( obj_info, index_dict, 'COMMENT_COL' ,'s' )

            # Determine the magnitude(s)
            mag_band = index_dict['MAG_BAND']
            mag = read_dict_maybe_comment( obj_info, index_dict, 'MAG_COL', mag_band, comment_col, comment, index_dict['MAG_UNKNOWN'], 'f' )
            mag_band2 = index_dict['MAG_BAND2']
            mag2 = read_dict_maybe_comment( obj_info, index_dict, 'MAG_COL2', mag_band2, comment_col, comment, index_dict['MAG_UNKNOWN'], 'f' )

            # Determine the spectral type
            sptype = read_dict( obj_info, index_dict, 'SPEC_COL', 's')

            weight = 0.0
            exposure = 5.0

            # Determine the RA/Dec
            ra_dec_type = int(index_dict['RA_DEC_TYPE'])
            if ra_dec_type != 2:
                ra = read_dict(obj_info, index_dict, 'RA_COL', 's')
                dec = read_dict(obj_info, index_dict, 'DEC_COL', 's')
                if ra_dec_type == 0:  # given in discrete (ie, hh:mm:ss and deg:arcmin:arcsec) form
                    radec = 'convert_ra_dec'
                elif ra_dec_type == 1: # given in decimal form
                    radec = 'radec_str2float'
            else:
                ra = "-1.0"
                dec = "-1.0"
                radec = 'get_ra_dec_from_SDSS_name'

            # Add the telluric to the list
            tell =  ra_dec_funcs[radec]( Target(label, name, 0.0, mag, ra, dec, weight, exposure) )

						# Update some general information
            tell.mag_band = index_dict['MAG_BAND']
            tell.mag_band2 = index_dict['MAG_BAND2']               
            tell.mag2 = mag2
            tell.sptype = sptype

			# If a filter is passed (via the index dictionary), then make sure that this object passes the test.
            if by_pass_filter(obj_info,index_dict)==False:
                tell.exclude = True

            # Finally, make sure this target is not too close to the Moon
            min_moon_angle = 30.0
            too_close_to_Moon(tell, Moon, min_moon_angle, False)
                
            tells.append(tell)

    # Close the object file
    obj_file.close()

    return tells

# If a filter is passed (via ### FILTER_COL and ### FILTER_VAL in the object files), then check if this object passes the filter (return 'True') or not (return 'False')
def by_pass_filter( obj_info, index_dict ):
    src_info = read_dict( obj_info, index_dict, 'FILTER_COL', 's' )
    good_vals = index_dict['FILTER_VAL']
    if src_info is None or good_vals is None:
        return True # If filter is not set, let everything through
    else:
        # Determine the patterns to match
        good_vals = good_vals.split(";")
        for index, sub in enumerate(good_vals):
            if src_info.find(sub) != -1:
                return True
        #print src_info
        return False

def reset_index_dict( index_dict, targetfile ):
    index_dict['LABEL'] = targetfile
    # Default: Magellan observing catalog
    index_dict['NAME_COL'] = 1
    index_dict['RA_COL'] = 2
    index_dict['DEC_COL'] = 3
    return index_dict

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

# Alg taken from Bringer et al 2000 "Flexible Automatic Scheduling for Autonomous Telescopes: The MAJORDOME"
# Use this one with EAF scheduling
def scheduleTargetMAJORDOME(target, schedule, start_time, granularity, tell_slots, scheduled_targets, unscheduled_targets, loud):
    conflict = None
    loud.scheduler = True
    [ rise_time, set_time, slots_needed, slots_available ] = get_slot_props( target, start_time, granularity, tell_slots, schedule, loud.scheduler )

#    rise_time = int(math.ceil(timeElapsed(target.am_rise, start_time) - 5)/granularity)
#    set_time = int(math.floor(timeElapsed(target.am_set, start_time)/granularity))
#    print "Time required", getTotalObsTime(target.exp, granularity, tell_slots)
#    slots_needed = int(math.ceil(getTotalObsTime(target.exp, granularity, tell_slots)/granularity))
#    slots_available = schedule[rise_time:set_time].count(None)
#    if slots_available < slots_needed:
#        print "Not enough slots available; %d needed, %d available (rise time = %d, set time = %d)." % (slots_needed, slots_available, rise_time, set_time)
        #print "Not enough slots available;", slots_needed, "needed,", slots_available, "available."

    counter = 0
    start = -1
    end = -1
    print "Need", slots_needed, "slots for", target.name, "between", rise_time, "and", set_time
    for i in range(0, set_time - rise_time):
        #print rise_time + i
        if(schedule[rise_time + i] is None):
            if(counter == 0): # We've just started a new block
                start = i
            counter = counter + 1
        else:
            start = -1
            counter = 0
        if(counter is slots_needed): # There are sufficient contiguous slots
            end = i
            schedule[rise_time + start:rise_time + end + 1] = [target] * slots_needed
            target.start_observation = (rise_time + start) * granularity
            target.end_observation = (rise_time + end) * granularity
            print "Placing in range:", rise_time + start, rise_time + end
            scheduled_targets.append(target)
            return True
    else: # There are not enough contiguous slots
        for i in range(0, set_time - rise_time):
            if(schedule[rise_time + i] is not None and schedule[rise_time + i].weight < target.weight): # Find the first lower-weight task
                conflict = schedule[rise_time + i]
                conflict_slots = int(math.ceil(getTotalObsTime(conflict.exp, granularity, tell_slots)/granularity))
                print "Found lower-weight conflict", conflict.name
                #print "Conflict slots", conflict_slots
                #print "Obstime", getTotalObsTime(conflict.exp, granularity, tell_slots)
                if(conflict_slots >= slots_needed and rise_time + i + slots_needed <= set_time):
                    #time = start_time
                    #print "SCHEDULE BEFORE DISPLACEMENT"
                    #for slot in schedule:
                    #    if slot is None:
                    #        print time, ": FREE"
                    #    else:
                    #        print time, ":", slot.label, slot.name, slot.exp/60
                    #    time += granularity
                    #    if(time % 100 == 60):
                    #        time -= 60
                    #        time += 100
                    schedule[rise_time + i:rise_time + i + conflict_slots] = [None] * conflict_slots # Remove old target
                    schedule[rise_time + i:rise_time + i + slots_needed] = [target] * slots_needed
                    scheduled_targets.remove(conflict)
                    unscheduled_targets.append(conflict)
                    print "*\t*\t*\tSCHEDULED", target.name, "BY DISPLACING", conflict.name
                    scheduled_targets.append(target)
                    #time = start_time
                    #print "SCHEDULE AFTER DISPLACEMENT"
                    #for slot in schedule:
                    #    if slot is None:
                    #        print time, ": FREE"
                    #    else:
                    #        print time, ":", slot.label, slot.name, slot.exp/60
                    #    time += granularity
                    #    if(time % 100 == 60):
                    #        time -= 60
                    #        time += 100
                    return True
        else:
            print "*\t*\t*\tCONFLICT: DID NOT SCHEDULE", target.name,"\n\n"
            unscheduled_targets.append(target)
            return False



# Inputs a target, scan start time, schedule, granularity, and outputs the rise and set time slot numbers ('rise_time' and 'set_time'), number of slots required ('slots_needed') and number of slots available ('slots_available')
def get_slot_props( target, start_time, granularity, tell_slots, schedule, loud ):

    # Calculate the time (in integer minutes) from start time at which this target rises and sets
    elapse_rise = timeElapsed(target.am_rise,start_time)
    elapse_set = timeElapsed(target.am_set,start_time)

    # Convert these to discrete slots numbers (first slot in schedule is 0)
    rise_time = elapse_rise/granularity
    if (elapse_rise % granularity)>0: rise_time = rise_time + 1
    set_time = elapse_set/granularity

    if loud: print "Src = %s, rise slot = %d, set slot = %d" % (target.name, rise_time, set_time)
    if loud: print "Time required", getTotalObsTime(target.exp, granularity, tell_slots)
    slots_needed = int(math.ceil(getTotalObsTime(target.exp, granularity, tell_slots)/granularity))
    slots_available = schedule[rise_time:set_time].count(None)
    if slots_available < slots_needed and loud:
        print "Not enough slots available; %d needed, %d available." % (slots_needed, slots_available)

    return [rise_time, set_time, slots_needed, slots_available]


# Formula taken from http://scienceworld.wolfram.com/astronomy/JulianDate.html, and is correct for Gregorian calendar dates from 1901 to 2099
def getJulianDay(d):
    """Take in a datetime object and return the Julian Day Number."""
    return 367*d.year - int(d.year*(d.year+int((d.month+9)/12))/4) + int(275*d.month/9) + d.day + 1721013.5 + d.utcoffset().seconds/(60.0*60.0*24.0)

# Inputs the UT year ('Y'), month ('M'), day ('D') and decimal hour ('UT'), as well as the site's longitude (in decimal hours, west is positive), and outputs the local sidereal time
# Taken from http://aa.usno.navy.mil/faq/docs/GAST.html 
def getLST(d, obs):
    """Take in a datetime object and return a datetime object corresponding to the local sidereal time at the observatory"""
    
    # Calculate some important intermediate quantities
    jd = getJulianDay(d)
    #jd = jd0 + d.utcoffset()/(60.0*24.0)
    d = jd - 2451545.0 # Days since J2000.0, including fractional days
    d0 = jd0 - 2451545.0
    t = d/36525.0

    # Calculate the Greenwich Mean Sidereal Time
    #gmst = 6.697374558 + 0.06570982441908*d0 + 1.00273790935*(d.utcoffset()/60.0) + 0.000026*t
    #gmst = make0to24( gmst )
    GMST = 280.46061837 + 360.98564736629*d

    # Calculate the local sidereal time
    #lst = make0to24(gmst - obs.long)
    LST_deg = (GMST - obs.long) % 360.0
    hours, min_sec = divmod(LST_deg, 15.0)
    minutes, seconds = divmod(min_sec, 0.25)
    seconds = seconds * 240.0
    lst = datetime(hours, minutes, seconds, tzinfo=Timezone(d.utcoffset(), True))
    #lst.replace(tzinfo=Timezone(d.utcoffset(), True))
    return lst

# Inputs a local date and outputs the offset from local time in UT (Accurate until 2020).  Assumes day is Chilean (not UT), and uses the Daylight Savings schedule given on:
# <http://www.timeanddate.com/worldclock/timezone.html?n=232>
def calc_UToff( Y, M, D ):
    UToff = -4.0
    if M < 3 or M > 10:
        return -3.0
    elif M==3:
        if ( (Y==2011 and D<13) or (Y==2012 and D<11) or (Y==2013 and D<10) or (Y==2014 and D<9) or (Y==2015 and D<15) or (Y==2016 and D<13) or (Y==2017 and D<12) or (Y==2018 and D<11) or (Y==2019 and D<10) ):
            return -3.0
    elif M==10:
        if( (Y==2010 and D>9) or (Y==2011 and D>8) or (Y==2012 and D>13) or (Y==2013 and D>12) or (Y==2014 and D>11) or (Y==2015 and D>10) or (Y==2016 and D>8) or (Y==2017 and D>14) or (Y==2018 and D>13) or (Y==2019 and D>12) ):
            return -3.0

    return -4.0

def convert_time( site, intype, outtype, time ):
# types: 's'=sidereal, 'u'=ut, 'w'=watch
    if intype==outtype:
        return time
    elif intype=="s": # inputting local sidereal time
        if outtype=="u":
            return time - site.ut2lst
        elif outtype=="w":
            return time + site.lst2curr
    elif intype=="u":
        if outtype=="s":
            return time + site.ut2lst
        elif outtype=="w":
            return time + site.UT2curr
    elif intype=="w":
        if outtype=="s":
            return time - site.lst2curr
        elif outtype=="u":
            return time - site.UT2curr

# Calculates the conversion factor between lst and local time
def calc_lst2curr( Y, M, D, UT, UT2curr, longitude ):

    UT2lst = calc_UT2lst( Y, M, D, UT, longitude )
    lst2curr = make0to24(UT2curr - UT2lst )
    # print "calc_lst2curr(): lst2curr = %f, UT2lst = %f, UToff = %f" % (lst2curr, UT2lst, UT2curr)
    return lst2curr

def calc_UT2lst( Y, M, D, UT, longitude ):
    return  make0to24(calc_lst( Y, M, D, UT, longitude) - UT)

def makeMoon(obs, local_time, loud):

    # Formula taken from The Astronomical Almanac, 2009, D22: "Low-precision formulae for geocentric coordinates of the Moon"
    #jd = calc_Julian_day( day[0], day[1], day[2], local_time - site.UT2curr )
    print local_time.isoformat()
    jd = getJulianDay(local_time)

    # Calculate the number of Julian centuries since 2000
    t = (float(jd) - 2451545.0)/36525.0 # Number of Julian centuries since 2000

    # Calculate important intermediate quantities
    lam = 218.32 + 481267.881*t #+ 6.29*sin( d2r( 135.0 + 477198.87*t ) ) - 1.27*sin( d2r( 259.3 - 413335.36*t ) ) + 0.66*sin( d2r( 235.7 + 890534.22*t ) ) + 0.21*sin( d2r( 269.9 + 954397.74*t ) ) - 0.19*sin( d2r( 357.5 + 35999.05*t ) ) - 0.11*sin( d2r( 186.5 + 966404.03*t ) )
    beta = 5.13*sin( d2r( 93.3 + 483202.02*t ) ) + 0.28*sin( d2r( 228.2+960400.89*t ) ) - 0.28*sin( d2r( 318.3 + 6003.15*t ) ) - 0.17*sin( d2r( 217.6 - 407332.21*t ) )
    pi1 = 0.9508 + 0.0518*cos( d2r( 135.0 + 477198.87*t ) ) + 0.0095*cos( d2r( 259.3 - 413335.36*t ) ) + 0.0078*cos( d2r( 235.7 + 890534.22*t ) ) + 0.0028*cos( d2r( 269.9 + 954397.74*t ) )
    r = 1.0/sin( d2r( pi1 ) )

    # Calculate the geocentric direction cosines
    l = cos( d2r( beta ) )*cos( d2r( lam ) )
    m = 0.9175*cos( d2r( beta ) )*sin( d2r( lam ) ) - 0.3978*sin( d2r( beta ) )
    n = 0.3978*cos( d2r( beta ) )*sin( d2r( lam ) ) + 0.9175*sin( d2r( beta ) )

    # Calculate the geocentric rectangular coordinates
    x = r*l
    y = r*m
    z = r*n

    # Calculate the topocentric rectangular coordinates
    #phi1 = site.lat
    #lst = local_time - site.lst2curr
    #x1 = x - cos( d2r( phi1 ) )*cos( d2r( lst ) )
    #y1 = y - cos( d2r( phi1 ) )*sin( d2r( lst ) )
    #z1 = z - sin( d2r( phi1 ) )
    #lst = coordinates.angles.Angle(convertTimeToDegrees(local_time.astimezone(obs.sidereal)), unit="degree")
    GMST = sidereal.SiderealTime.fromDatetime(local_time)
    LST = coordinates.angles.Angle((GMST.lst(obs.long.radians)).hours, unit="hour")
    print LST.hours
    x1 = x - cos(obs.lat.radians)*cos(LST.radians)
    y1 = y - cos(obs.lat.radians)*sin(LST.radians)
    z1 = z - sin(obs.lat.radians)
    r1 = math.sqrt( x1*x1 + y1*y1 + z1*z1 )

    # Calculate the ra and dec
    moon_coords = coordinates.ICRSCoordinates(ra=math.atan2(y1,x1), dec=math.asin(z1/r1), unit=("radian", "radian"))
    #ra = math.atan2( y1, x1 )*12.0/math.pi
    #dec = math.asin( z1/r1 )*180/math.pi
    #if ra < 0.0:
    #    ra += 24.0

    if loud.moon==True:
        print "makeMoon(): Moon's coordinates on %s determined to be approximately ra = %f, dec = %f" % ( local_time.date.isoformat(), moon_coords.ra.degrees, moon_coords.dec.degrees)

#    ra = 21.0 + 12.0/60.0 + 44.0/3600.0
#    dec = -1.0*(12.0 + 49.0/60.0 + 3.0/3600.0)
    
#    print "ra = %f, dec = %f" % (ra, dec)

    Moon = Target('Moon', 'Moon', 0.0, 0.0, moon_coords, 0.0, 0.0)

    return Moon

def sin( rads ):
    return math.sin(rads)

def cos( rads ):
    return math.cos(rads)


# Inputs an int array [ YYYY, MM, 'DD' ], and outputs a string reading the date
def str_date( date ):

    [ YYYY, MM, DD ] = [ date[0], date[1], date[2] ]
    if MM==1:
        Month = 'Jan'
    elif MM==2:
        Month = 'Feb'
    elif MM==3:
        Month = 'Mar'
    elif MM==4:
        Month = 'Apr'
    elif MM==5:
        Month = 'May'
    elif MM==6:
        Month = 'Jun'
    elif MM==7:
        Month = 'Jul'
    elif MM==8:
        Month = 'Aug'
    elif MM==9:
        Month = 'Sep'
    elif MM==10:
        Month = 'Oct'
    elif MM==11:
        Month = 'Nov'
    elif MM==12:
        Month = 'Dec'

    output = "%s_%02d_%04d" % (Month, DD, YYYY)
    return output



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

    #check_required_opts(argv) # not required at this time...

    #if(start_time < 1200):   # We're probably after midnight
    #    start_time += 2400

    #obs_length = timeElapsed(end_time, start_time)

    # Grab today's date (Gregorian calendar)
    if first_day is None:
        today = (str(datetime.date.today())).split("-")
        utc = str(datetime.datetime.utcnow())
        first_day = [ int(today[0]), int(today[1]), int(today[2]) ]



    obs = Observatory('LCO')
    start = datetime.datetime(year=2013, month = 5, day = 13, hour = 19, minute=0, tzinfo = obs.timezone)
    end = datetime.datetime(year=2013, month = 5, day = 14, hour = 7, minute=0, tzinfo = obs.timezone)

    obs_length = end - start

    # If desired, create the Moon
    if useMoon == True:
        Moon = makeMoon(obs, start, loud)
    else:
        Moon = None

    # Read in the targets and initialize their structures
    targets = getTargets( targetlist, priorities, seeing, Moon, loud, weight_opt )

    # Do airmass calculations for all targets
    for target in targets:
        target.night_start = start
        target.night_end = end
        getAirmassRange(target, airmass, obs, loud)
        print "Target %s rise/set (%s, %s) AM rise/set (%s, %s)" % (target.name, target.rise_time.isoformat(), target.set_time.isoformat(), target.am_rise_time.isoformat(), target.am_set_time.isoformat())


if __name__ == "__main__":
    main(sys.argv[1:])






        #print "airmass range: %s %04d %04d %04d" % (target.name, target.am_rise, target.am_set, target.am_vis)

##     for scheduling_night in range(1, nights+1):
##         day = first_day + [ 0, scheduling_night-1, 0 ]
##         print "%s:  Running scheduler for date %d-%d-%d, day %d of %d" % (prog_name, day[0], day[1], day[2], scheduling_night, nights)

##         # Update the offset between lst and local time
##         lco.lst2curr = calc_lst( day[0], day[1], day[2], 0.0, lco.long )

##         schedule = [None] * int(obs_length/granularity)

##         targets.sort(key=lambda x: x.weight, reverse=True)
##         if eaf:
##             targets.sort(key = lambda x: timeElapsed(x.am_rise, start_time))
        
##         #for target in targets:
##         #    print "%s %04d %04d %04d" % (target.name, target.am_rise, target.am_set, target.am_vis)
##     #targets.sort(key=lambda x: float(x.exp)/60/x.am_vis, reverse = True)
##         conflicts = list()
##         scheduled = list()

##         if loud.scheduler:
##             print "Targets"
##             print "---------------------------------------------"

##         for target in targets:
##             if target.exclude == False: # Make sure target not automatically excluded (because of proximity to Moon, for example
##                 if majordome:
##                     was_scheduled = scheduleTargetMAJORDOME(target, schedule, start_time, granularity, tell_slots, scheduled, conflicts, loud)
##                 else:
##                     was_scheduled = scheduleTarget(target, schedule, start_time, granularity, tell_slots, scheduled, conflicts, loud)
##             else:
##                 if loud.scheduler:
##                     print "%s excluded from schedule (reason = %s)" % (target.name, target.excl_reason)

##         if loud.scheduler:
##             for target in targets:
##                 print "Name:", target.name, "\t\t\tWeight:", target.weight, "Range: %04d %04d" % (target.am_rise, target.am_set), "\tFlex:", 60*target.am_vis/target.exp, "\tExposure Time:", target.exp #"RA/DEC:", target.ra, target.dec

##                 print "\nSuccessfully scheduled", len(scheduled), "of", len(targets), "targets."
##                 print "Slack time:", schedule.count(None) * granularity, "minutes."

##                 #print "Total path length observed:", reduce(lambda x, y: (x + (y.z - 2) if y.z != 0.0 else x), scheduled, 0.0)
##                 #print "Total path length observed above z = 4.7:", reduce(lambda x, y: (x + (y.z - 4.7) if y.z != 0.0 else x), scheduled, 0.0)
##             print "\nCould not schedule these targets:"
##             for conflict in conflicts:
##                 print conflict.name

##             print "\nScheduled these targets:"
##             for target in scheduled:
##                 print target.name



## #        print "Schedule for night %d:" % scheduling_night
## #        time = start_time
## #        for slot in schedule:
## #            if slot is None:
## #                print time, ": FREE"
## #            else:
## #                print time, ":", slot.label, slot.name, slot.exp/60
## #            time += granularity
## #            if(time % 100 == 60):
## #                time -= 60
## #                time += 100

                

##         num_tells = 5 # number of tells to output at the beginning and end of the scan for each source
##         tell_slots = 3 # number of time slots to devote to tellurics
##         # Find tellurics for ALL targets, whether they're scheduled or not
##         [ all_tells, out_tells, out_tcvs ] = find_closest_tellurics(targets, telluric_files, lco, pure_A0V_only, tell_min, tell_max, num_tells, tell_slots, Moon, None, None )

##         #for target in scheduled:
##         #    print "Telluric stars for %s: " % target.name
##         #    for tell in target.tellurics:
##         #        print "HIP" + tell.name

##         if make_catalog == True:
##             tscope_catalog = open( str_date(day) +  ".cat", "w")

##             # Print all sources (and their best tellurics) into the catalog
##             obj_no = 100
##             incr = 100
##             while( num_tells >= incr ):
##                 incr += 10
##             for target in targets:
##                 tscope_catalog.write("#\n")
##                 target.scheduled_id = "%04d" % obj_no
##                 tscope_catalog.write(target.catalog_entry(True))
##                 obj_no_tell = obj_no
##                 for tell_num in range(0,target.num_tells):
##                     obj_no_tell = obj_no_tell + 1
##                     target.tellurics[tell_num].scheduled_id = "%04d" % obj_no_tell
##                     tscope_catalog.write(target.telluric_catalog_entry(tell_num))
##                 obj_no += incr

##             # Now cycle through and print all tellurics into the catalog
##             tscope_catalog.write("#\n#\n# Complete list of Tellurics\n#\n")
##             # Create a dummy source with all tellurics
##             dummy_target = Target('target', 'dummy', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
##             dummy_target.num_tells = len(all_tells)
##             dummy_target.tellurics = all_tells
##             dummy_target.tell_comp_vals = list()
##             for tell_num in range(0,dummy_target.num_tells):
##                 dummy_target.tellurics[tell_num].scheduled_id = "%04d" % obj_no
##                 dummy_target.tell_comp_vals.append(tell_comp_vals(-1, 'dummy', 0.0, 0.0, 0.0, 0.0, 1.0, 0.0))
##                 tscope_catalog.write(dummy_target.telluric_catalog_entry(tell_num) )
##                 obj_no = obj_no + 1


##         # Print the final schedule to screen
##         # print_schedule( start_time, granularity, schedule, scheduling_night )

##         # If desired, print out all of the details of a (some) source(s)
##         if loud_objects is not None:
##             for index, target in enumerate(targets):
##                 for object in loud_objects:
##                     if target.name.find(object) != -1:
##                         print targets[index].details()



##         targets = conflicts

