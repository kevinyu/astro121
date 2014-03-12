import numpy as np
import logging
import os
import random
import threading
import time

import ephem

from rotation import rd2aa


# config variables
LONG = -122.2573  # deg
LAT = 37.8732  # deg
POINT_INTERVAL = 60.  # repoint every minute
HOME_INTERVAL = 60. * 60.  # point home every hour
ALT_LIMS = (np.deg2rad(17), np.deg2rad(85))
OBJECTS = dict(
    sun = {"obj": ephem.Sun()},
    moon = {"obj": ephem.Moon()},
    m17 = {"ra": np.deg2rad(275.1083), "dec": np.deg2rad(-16.1767)}
)
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
            print "rl: pointing home"
        def pntTo(self, az, alt):
            print "rl: pointing {az} {alt}".format(az=az, alt=alt)
        def recordDVM(self, *args, **kwargs):
            print "rl: recording data..."
            while True:
                print "take data point "
                time.sleep(2)
    radiolab = MockRadiolab()


class Tracker:
    def __init__(self, ra=None, dec=None, obj=None, session=None):
        """Tracks an object in the sky and collects data."""
        self.obs = ephem.Observer()
        self.obs.long, self.obs.lat = np.deg2rad(LONG), np.deg2rad(LAT)
        logger.info("Observer set at (long, lat): {long_}, {lat}".format(
            long_=self.obs.long, lat=self.obs.lat))

        if (obj and not (ra or dec)) or ((ra and dec) and not obj):
            # this variable will be None if the object's RA and DEC are fixed
            self.moving_obj = obj
            self.ra = ra and ephem.hours(ra)
            self.dec = ra and ephem.degrees(dec)
        else:
            raise Exception("Only use either (ra, dec) or an ephem obj.")

        self.last_home = None
        self.session = session or "noname-{randnum}".format(str(random.random())[-6:])

    def track(self, timelimit=None):
        logger.info("Tracking started. Session name: {session}".format(session=self.session))

        self.point_home()

        self.start_time = time.time()
        if not self.refresh_pointing():
            raise Exception("Initial pointing's ALT was out of range")

        self.data_thread = threading.Thread(target=self.take_data)
        self.data_thread.daemon = True
        self.data_thread.start()

        while (not timelimit) or (time.time() - self.start_time <= timelimit):
            if not self.last_home or (time.time() - self.last_home >= HOME_INTERVAL):
                self.point_home()
            time.sleep(POINT_INTERVAL)
            self.refresh_pointing()

    def point_home(self):
        """Wrapper around point home"""
        logger.info("Pointing home")
        self.last_home = time.time()
        radiolab.pntHome()
        logger.info("Pointing complete")

    def point(self, az, alt):
        logger.info("Pointing to (az, alt): {az} {alt}".format(az=az, alt=alt))
        radiolab.pntTo(az=az, alt=alt)
        logger.info("Pointing complete")

    def take_data(self):
        datafile = os.path.join(DATADIR, "{session}.npz".format(session=self.session))
        logger.info("Taking data for {session} to {datafile}".format(
            session=self.session, datafile=datafile))
        radiolab.recordDVM(filename=datafile, sun=bool(self.moving_obj),
                verbose=True, showplot=False)

    def refresh_pointing(self):
        self.obs.date = ephem.now()
        if self.moving_obj:
            self.moving_obj.compute(self.obs)
            self.ra = self.moving_obj.ra
            self.dec = self.moving_obj.dec

        az, alt = rd2aa(self.ra, self.dec,
                lst=self.obs.sidereal_time(), lat=self.obs.lat)
        az = ephem.hours(az)
        alt = ephem.degrees(alt)
        if not (ALT_LIMS[0] < alt < ALT_LIMS[1]):
            logger.warning("Object at {az} {alt} is beyond telescope limits."
                    " Not pointing...".format(az=az, alt=alt))
            return False
        self.point(az, alt)
        return True


def get_counter():
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
    try:
        objkey = sys.argv[1]
    except IndexError:
        raise Exception("Call with object of interest as command line arg;"
                " i.e. python tracker.py m17")
    if objkey not in OBJECTS:
        raise Exception("{objkey} not configured with RA, DEC"
                "or with a pyephem object".format(objkey=objkey))

    session_name = "{objkey}-{counter}".format(objkey=objkey, counter=get_counter())
    log_handler = logging.FileHandler(os.path.join(LOGDIR, "tracking.log"))
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.info("*** USER REQUESTS TO TRACK {key}".format(key=objkey))
    tracker = Tracker(session=session_name, **OBJECTS[objkey])
    tracker.track()
