# basic coron imaging ETC fored from hri_etc on Sept 11, 2024 - JT

import numpy as np
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, Paragraph, Range1d  
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import Slider, Div, Select 
from bokeh.models.layouts import TabPanel, Tabs
from bokeh.layouts import row, column 
from bokeh.io import curdoc
import astropy.units as u


# This import supports the new exptime panel for coronagraphic imaging - JT 091124 
from syotools.models import Telescope, Coronagraph

import phot_compute_snr as phot_etc 

import Telescope as T 
import cor_help as h 
import get_cor_seds 
import pysynphot as S 

cac, tel = Coronagraph(), Telescope() 
tel.set_from_json('EAC1')
tel.add_coronagraph(cac) 
cac_exp = cac.create_exposure() 
cac._calc_count_rates_imaging() 
cac._signal_to_noise
#end of new stuff 

spec_dict = get_cor_seds.add_spectrum_to_library() 
template_to_start_with = 'Flat (AB)' 
spec_dict[template_to_start_with].wave 
spec_dict[template_to_start_with].flux # <---- these are the variables you need to make the plot 
spec_dict[template_to_start_with].convert('abmag') 

# set up ColumnDataSources for the coron texptime plot 
source_exp = ColumnDataSource(data=dict(x=[1,2,3,4,5], y=[38,43,55,63,254], desc=['RC = 10-10 no post', 'RC=10-10 with post', 'RC = 10-9 no post', 'RC = 10-9 with post', 'RC = 10-8 no post'] ))
#source2 = ColumnDataSource(data=dict(x=hdi.pivotwave[0:2], y=snr[0:2], desc=hdi.bandnames[0:2]))
#source3 = ColumnDataSource(data=dict(x=hdi.pivotwave[-3:], y=snr[-3:], desc=hdi.bandnames[-3:]))

hover = HoverTool(point_policy="snap_to_data", 
        tooltips="""
        <div>
            <div>
                <span style="font-size: 17px; font-weight: bold; color: #696">@desc </span>
            </div>
            <div>
                <span style="font-size: 15px; font-weight: bold; color: #696">Exptime = </span>
                <span style="font-size: 15px; font-weight: bold; color: #696;">@y</span>
            </div>
        </div>
        """
    )


texp_plot = figure(height=400, width=700, tools="crosshair,pan,reset,save,box_zoom,wheel_zoom",
	x_range=[0, 6], y_range=[0, 100], border_fill_color='black', toolbar_location='right')
texp_plot.xaxis.major_label_overrides = {0:' ', 1:"10^-1, no post", 2:"10^10 with post", 3:"10^-9 no post", 4:"10^-9 with post", 5:"RC = 10-8", 6:" "} 
texp_plot.line('x', 'y', source=source_exp, line_width=3, line_color='blue', line_alpha=1.0) 
texp_plot.scatter('x', 'y', source=source_exp, fill_color='white', line_color='blue', size=10)
texp_plot.add_tools(hover)
texp_plot.xaxis.axis_label = 'Contrast and Degree of Post-processing' 
texp_plot.yaxis.axis_label = 'Exposured Time Required in Hours' 

spectrum_template = ColumnDataSource(data=dict(w=spec_dict[template_to_start_with].wave, f=spec_dict[template_to_start_with].flux, \
                                   w0=spec_dict[template_to_start_with].wave, f0=spec_dict[template_to_start_with].flux))

sed_plot = figure(height=400, width=700,tools="crosshair,pan,reset,save,box_zoom,wheel_zoom",
              x_range=[120, 2300], y_range=[35, 21], border_fill_color='black', toolbar_location='right')
sed_plot.x_range = Range1d(100, 2300, bounds=(120, 2300)) 
sed_plot.yaxis.axis_label = 'AB Magnitude'
sed_plot.xaxis.axis_label = 'Wavelength [nm]'
sed_plot.line('w','f',line_color='orange', line_width=3, source=spectrum_template, line_alpha=1.0)  

def update_exptime(attrname, old, new):

    cac.telescope.aperture = aperture.value * u.m

    if ("Type 1" in ss_method.value): 
        cac.eta_p = 0.2 

    if ("Type 2" in ss_method.value): 
        cac.eta_p = 0.4 

    if ("Type 3" in ss_method.value): 
        cac.eta_p = 0.6 
	
    print("You have asked for Starlight Suppression Method = ", ss_method.value, " eta_p =", cac.eta_p, "telescope = ",  cac.telescope.aperture) 
    print("And your asked for Starlight Suppression Method = ", ss_method.value, " eta_p =", cac.eta_p, "telescope = ",  cac.telescope.aperture) 

    x = [1,2,3,4,5] 
    y = [1., 5, 6, 11, 3]

    # case 1 
    cac.raw_contrast = 1e-10 
    cac.sigma_DeltaC = 0. 
    tt = np.arange(1, 500) 
    ee = [] 
    for t in tt: 
        cac.int_time = t * u.hr
        cac._calc_count_rates_imaging() 
        ee.append(cac._signal_to_noise.value) 

    exptime_to_use = np.min(tt[np.array(ee) > snr_goal.value]) 
    y[0] = exptime_to_use 

    # case 2 
    cac.raw_contrast = 1e-10 
    cac.sigma_DeltaC = 5e-12 
    tt = np.arange(1, 500) 
    ee = [] 
    for t in tt: 
        cac.int_time = t * u.hr
        cac._calc_count_rates_imaging() 
        ee.append(cac._signal_to_noise.value) 

    exptime_to_use = np.min(tt[np.array(ee) > snr_goal.value]) 
    y[1] = exptime_to_use 

    # case 3 
    cac.raw_contrast = 1e-9  
    cac.sigma_DeltaC = 0.
    tt = np.arange(1, 500) 
    ee = [] 
    for t in tt: 
        cac.int_time = t * u.hr
        cac._calc_count_rates_imaging() 
        ee.append(cac._signal_to_noise.value) 

    exptime_to_use = np.min(tt[np.array(ee) > snr_goal.value]) 
    y[2] = exptime_to_use 

    # case 4 
    cac.raw_contrast = 1e-9  
    cac.sigma_DeltaC = 5e-12 
    tt = np.arange(1, 500) 
    ee = [] 
    for t in tt: 
        cac.int_time = t * u.hr
        cac._calc_count_rates_imaging() 
        ee.append(cac._signal_to_noise.value) 

    exptime_to_use = np.min(tt[np.array(ee) > snr_goal.value]) 
    y[3] = exptime_to_use 

    # case 5 
    cac.raw_contrast = 1e-8  
    tt = np.arange(1, 500) 
    ee = [] 
    for t in tt: 
        cac.int_time = t * u.hr
        cac._calc_count_rates_imaging() 
        ee.append(cac._signal_to_noise.value) 

    exptime_to_use = np.min(tt[np.array(ee) > snr_goal.value]) 
    y[4] = exptime_to_use 

    desc = ['RC = 10-10 no post', 'RC=10-10 with post', 'RC = 10-9 no post', 'RC = 10-9 with post', 'RC = 10-8 no post'] 
    source_exp.data = dict(x=x, y=y, desc=desc)

# fake source for managing callbacks 
source = ColumnDataSource(data=dict(value=[]))
source.on_change('data', update_exptime)

# Set up widgets
aperture = Slider(title="Aperture (meters)", value=6., start=4., end=10.0, step=0.1, tags=[4,5,6,6], width=250) 
aperture_callback = CustomJS(args=dict(source=source), code="""
    source.data = { value: [cb_obj.value] }
""")
aperture.js_on_change('value_throttled', aperture_callback) 

snr_goal= Slider(title="Required SNR", value=7., start=1.0, end=20.0, step=1. , width=250) 
snr_callback = CustomJS(args=dict(source=source), code="""
    source.data = { value: [cb_obj.value] }
""")
snr_goal.js_on_change("value_throttled", snr_callback) 

magnitude = Slider(title="V Magnitude (AB)", value=28.0, start=20.0, end=35., width=250) 
magnitude_callback = CustomJS(args=dict(source=source), code="""
    source.data = { value: [cb_obj.value] }
""")
magnitude.js_on_change("value_throttled", magnitude_callback) 

ss_method = Select(title="Starlight Suppression System", value="Type 1 Coronagraph", 
                options=["Type 1 Coronagraph", "Type 2 Coronagraph", "Type 3 Coronagraph"], width=250) 

template = Select(title="Template Spectrum", value="Flat (AB)", 
                options=["Flat (AB)", "Blackbody (5000K)", "O5V Star", \
                         "B5V Star", "G2V Star", "M2V Star", "Orion Nebula", "Elliptical Galaxy", "Sbc Galaxy", \
                         "Starburst Galaxy", "NGC 1068"], width=250) 

for w in [ss_method]: 
    w.on_change('value', update_exptime)
	
controls = column(children=[aperture, snr_goal, ss_method], sizing_mode='fixed', max_width=300, width=300, height=700) 
controls_tab = TabPanel(child=controls, title='Controls')
info_tab = TabPanel(child=Div(text = h.help()), title='Info')
inputs = Tabs(tabs=[ controls_tab, info_tab], width=300) 

#plots = Tabs(tabs=[ TabPanel(child=texp_plot, title='Exposure Time'), TabPanel(child=sed_plot, title='SED')] ) 
plots = Tabs(tabs=[ TabPanel(child=texp_plot, title='Exposure Time') ]) 

curdoc().add_root(row(children=[inputs, plots])) 
curdoc().add_root(source) 
