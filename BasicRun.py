#!/usr/bin/env python
# coding: utf-8

# ## Basic Operations of the SYOTools version of the HWO ETCs

#first the necessary imports 
from syotools.models import Camera, Telescope, Spectrograph, PhotometricExposure, SpectrographicExposure
from syotools.utils.jsonunit import str_jsunit

# create a Telescope, Camera, and Exposure 
# if called without arguments, you get the defaults 
t, c, e = Telescope(), Camera(), PhotometricExposure()

#set the telescope to EAC1 
t.set_from_yaml('EAC1')

t.add_camera(c)
c.add_exposure(e)


for attr in t._tracked_attributes:
    print('{}: {}'.format(attr, str_jsunit(getattr(t,attr))))


for attr in c._tracked_attributes:
    print('{}: {}'.format(attr, str_jsunit(getattr(c,attr))))


for attr in e._tracked_attributes:
    print('{}: {}'.format(attr, str_jsunit(getattr(e, attr))))

print(e.snr)

