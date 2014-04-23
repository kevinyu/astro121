"""
$ ssh [-XY] -p 31 radiolab@leuschner.berkeley.edu

Things we will do
- point dish
- set LO frequency
- acquire data
- convert data to numpy arrays

$ cd ugradio/ugradio_code

Can initialize a dish with Dish(verbose=True) for debugging
>>> import dish
>>> d = dish.Dish()

Point to az, alt with the option of validating
It raises a ValueError if pointing is out of range
>>> d.point(alt, az, validate=None)

Point home at beginning of the shit
>>> d.home()

Take power with noise off and noise on using 100K blackbody
in order to capture changes in system temperature
>>> d.noise_on
>>> d.noise_off

Setting the LO frequency
>>> import dish_synth
>>> s = dish_synth.Synth()

clock of the system is at 24 MHz, bandwidth is 12 MHz
Can set frequency and amplitude of the LO
>>> s.set_freq(1390)
>>> s.set_amp(0)

if we want frequency 1420, we want to set our LO so that we get
the spectrum in the right range
1390 | 1402 | 1414 | 1420
If we set it to 1390 we get the thingy to alias twice over so your spectrum looks ok

Taking data
it takes 1/3 of a second to take a spectra
>>> import takespec
>>> takespec.takeSpec(filename, numFiles=1, numSpec=32)

reading the datas on me own computer
>>> import readspec_mod
>>> d = readspec_mod.readSpec("blahblah0.log")
>>> d.shape
(8192, 31)

convers frequencies from 1414 to 1426

stuff
- homing
pointing
coord-conv

- data collect
frequency control
noise control

- where to point
what frequencies to look at?

- raw data
remove RF interference
averages

"""
