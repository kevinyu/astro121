import numpy as np
import logging
import os
import random
import threading
import time

import ephem

from rotation import rd2aa
from objects import OBJECTS


_minutes = 60.  # seconds (makeshift units)
# config variables
LONG = -122.2573  # deg
LAT = 37.8732  # deg
POINT_INTERVAL = 0.5 * _minutes  # repoint every 30 seconds
HOME_INTERVAL = 60. * _minutes  # point home every hour
# RETRY_TIME = 5. * _minutes  # if initial pointing fails, retry in 5 minutes
# set FAILURE_LIMIT to None to try forever
FAILURE_LIMIT = None  # try for FAILURE_LIMIT * RETRY_TIME in seconds
ALT_LIMS = (17., 85.)
LOGDIR = "logs"
DATADIR = "data"

# setup logging
logger = logging.Logger("caniputanythinghere")
# add handler at bottom in script
# TODO: maybe use a more relevant timestamp on log?
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)
if not os.path.exists(DATADIR):
    os.makedirs(DATADIR)


try:
    import radiolab
except:
    # just keep this here for now while testing
    print "Not actually importing real radiolab!"
    class MockRadiolab:
        def pntHome(self):
            time.sleep(0)
        def pntTo(self, az, alt):
            time.sleep(0)
        def recordDVM(self, *args, **kwargs):
            while True:
                print "Taking data point."
                time.sleep(1)
    radiolab = MockRadiolab()


class Tracker:
    def __init__(self, ra=None, dec=None, obj=None, session=None):
        """Tracks an object in the sky and collects data.

        Takes either a pyephem object, or a ra and dec (not both)
        Arguments:
            ra (radians): Right ascension of object
            dec (radians): Declination of object
            obj (ephem.Body): Pyephem object
            session (str): Name of observing session (name of data file)
        """
        self.obs = ephem.Observer()
        self.obs.long, self.obs.lat = ephem.hours(np.deg2rad(LONG)), ephem.degrees(np.deg2rad(LAT))
        logger.info("Observer set at (long, lat): {long_}, {lat}".format(
            long_=self.obs.long, lat=self.obs.lat))

        if (obj and not (ra or dec)):
            self.source = obj
        elif ((ra and dec) and not obj):
            self.source = ephem.FixedBody()
            self.source._ra = ephem.hours(ra)
            self.source._dec = ephem.degrees(dec)
            self.source._epoch = ephem.J2000  # for precessing
        else:
            raise Exception("Only use either (ra, dec) or an ephem obj.")

        self.last_home = None
        self.session = session

    def track(self, timelimit=None):
        """Main tracking function

        Start tracking and launches data taking daemon thread.
        Starts by pointing home, then will repoint the telescope every POINT_INTERVAL seconds.

        Arguments:
            timelimit (float, optional): time limit of observation session in seconds
        """
        logger.info("Tracking started. Session name: {session}".format(session=self.session))

        self.point_home()

        self.start_time = time.time()

        self.refresh_pointing()

        self.data_thread = threading.Thread(target=self.take_data)
        self.data_thread.daemon = True
        self.data_thread.start()

        time.sleep(POINT_INTERVAL)

        while (not timelimit) or (time.time() - self.start_time <= timelimit):
            if not self.last_home or (time.time() - self.last_home >= HOME_INTERVAL):
                self.point_home()
            self.refresh_pointing()
            time.sleep(POINT_INTERVAL)

    def point_home(self):
        """Wrapper around radiolab.pntHome that also logs"""
        logger.warning("Start pointing home.")
        self.last_home = time.time()
        radiolab.pntHome()
        logger.warning("Finished pointing.")

    def point(self, az, alt):
        """Wrapper around radiolab.pntTo that also logs, pass as degrees"""
        logger.warning("Start pointing to (az, alt): {az} {alt}".format(az=az, alt=alt))
        radiolab.pntTo(az=az, alt=alt)
        logger.warning("Finished pointing.")

    def take_data(self):
        """Wrapper around radiolab.recordDVM that logs and sets the filename to the session name."""
        datafile = os.path.join(DATADIR, "{session}.npz".format(session=self.session))
        logger.info("Taking data for {session} to {datafile}".format(
            session=self.session, datafile=datafile))
        radiolab.recordDVM(filename=datafile, sun=type(self.source) is not ephem.FixedBody,
                verbose=True, showPlot=False)

    def refresh_pointing(self):
        """Updates the az, alt of the observed object, and repoints the interferometer
        """
        self.obs.date = ephem.now()
        self.source.compute(self.obs)

        az = np.rad2deg(self.source.az)
        alt = np.rad2deg(self.source.alt)

        # i should clean this up
        if not (ALT_LIMS[0] < alt < ALT_LIMS[1]):
            logger.warning("Object at {az} {alt} is beyond telescope limits."
                    "".format(az=az, alt=alt))

        if alt < ALT_LIMS[0]:
            alt = ALT_LIMS[0]
        elif alt > ALT_LIMS[1]:
            alt = ALT_LIMS[1]

        self.point(az, alt)
        return True


def get_counter():
    """Grabs latest value from counter file and increments it by 1 every time"""
    counterpath = os.path.join(LOGDIR, "counter")
    if not os.path.exists(counterpath):
        x = 0
    else:
        with open(counterpath, "r") as counterfile:
            x = int(counterfile.read())
    with open(counterpath, "w+") as counterfile:
        counterfile.write(str(x + 1))
    return x


if __name__ == "__main__":
    import sys
    import getopt

    ### Read arguments
    if not sys.argv[1:]:
        print ("Arguments error: python tracker.py <obj-id>"
            " [--time=<hours>] [--name=<session-name>]")
        sys.exit(2)

    try:
        opts, _ = getopt.getopt(sys.argv[2:], "t:n:", ["time=", "name="])
    except getopt.GetoptError:
        print ("Arguments error: python tracker.py <obj-id>"
            " [--time=<hours>] [--name=<session-name>]")
        sys.exit(2)

    objkey = sys.argv[1]
    if objkey not in OBJECTS:
        print ("Arguments error: python tracker.py <obj-id>"
            " [--time=<hours>] [--name=<session-name>]")
        raise Exception("{objkey} not configured with RA, DEC"
                " or with a pyephem object. Choose from:\n{options}"
                .format(objkey=objkey, options=OBJECTS.keys()))
    ###

    # Create a unique-ish name for the session
    count = get_counter()
    session_name = "{objkey}-{counter}".format(objkey=objkey, counter=count)
    observation_time = None
    for opt, arg in opts:
        if opt in ["-n", "--name"]:
            session_name = arg + "-" + str(count)
        elif opt in ["-t", "--time"]:
            observation_time = float(arg) * 60. * 60.  # convert to seconds

    with open(os.path.join(LOGDIR, "{session}.log".format(session=session_name)), "a+") as logfile:
        try:
            # Send all print statements and logger statements to logfile
            sys.stdout = logfile
            log_handler = logging.StreamHandler(stream=sys.stdout)
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
            logger.info("*** USER REQUESTS TO TRACK {key}***".format(key=objkey))
            tracker = Tracker(session=session_name, **OBJECTS[objkey])
            tracker.track(timelimit=observation_time)
        except KeyboardInterrupt:
            logger.warning("Tracking stopped by user.")
        except:
            logger.error("Unexpected conclusion to tracking.")
            raise
        else:
            logger.warning("Tracking finished.")
        finally:
            sys.stdout = sys.__stdout__

    print "Tracking session closed."
