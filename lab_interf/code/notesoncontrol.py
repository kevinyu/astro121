

"""
Controlling the interferometer
>>> import radiolab

Every hour or so, you should point home to reset tick crap (rounding errors)
>>> radiolab.pntHome()
0

To point to AZ, ALT coordinates
>>> radiolab.pntTo(alt=ALT, az=AZ)

Taking data
Using the digital volt-meter
>>> radiolab.recordDVM(
        filename="FILENAME.npz",
        sun=True,
        moon=False,
        recordLength=np.inf,  # how long to observe for, in seconds
        verbose=True,
        showPlot=False)

now you have a file called "FILENAME.npz"
loading the data gives you 3 arrays,
>>> data = np.load("newdata.npz")
>>> data["jd"]  # juilian day
>>> data["volts"]  # volts
>>> data["lst"]  # local sidereal time
>>> data["ra"]  # RA and DEC if sun or moon is true in recordDVM
>>> data["dec"]

how to use screen
see what screens are up
$ screen -list
start screen session
$ screen -S NAME
CTRL-A will kill the session
CTRL-A then D detaches screen session
resume screen
$ screen -r

Dont use ssh -X! Do ssh -x or 'ssh' to use actual ssh, not the alias ssh which does ssh -X by default

running threads
define functions to do stuff like logging/recording data/reorienting/etc, then you can run them in parallel
>>> from threading import Thread
>>> Thread(target=FUNCTION).start()

make sure to send out an email before beginning to observe
"""
