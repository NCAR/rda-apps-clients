# `rdams_client` for Python

The `rdams_client` Python utility can be run by registered RDA users to get detailed metadata for RDA data sets, to submit subset requests on select gridded data sets, to check on the processing status of any subset requests, and to download completed request output files to a local system.

The script can be used both on the command line or loaded as a module to interact with the response object directly. The Jupyter Notebooks in this directory provides an example of how you could potentially use the module.

`rdams_client.py` can be run using both python 2 and python 3, however, the `requests` library is required load the script.

## Installation

Download the `rdams_client` for the version of Python you are using (Python 2.x or Python 3.x) and execute `python rdams_client.py -help` for additional information.

## Usage
`rdams_client.py` can be used as a command line tool or as a python module.

**Command line Options**
```
python rdams_client.py -get_summary <dsnnn.n>
python rdams_client.py -get_metadata <dsnnn.n> <-f>
python rdams_client.py -get_param_summary <dsnnn.n> <-f>
python rdams_client.py -submit [control_file_name]
python rdams_client.py -get_status <RequestIndex> <-proc_status>
python rdams_client.py -download [RequestIndex]
python rdams_client.py -globus_download [RequestIndex]
python rdams_client.py -get_control_file_template <dsnnn.n>
python rdams_client.py -help
```

### Description of Options
- `-get_summary` provides an overview of what data sets and data set groups have subsetting available.
- `-get_summary <dsnnn.n>` provides an overview of what dataset groups have subsetting available in `dsnnn.n`.
- `-get_metadata <dsnnn.n>` dumps out a list of all available parameters found in `dsnnn.n` for subsetting.
- `-get_metadata <dsnnn.n> <-f>` dumps out the metadata in fixed sized columns. `-get_metadata <dsnnn.n>` parameters are dumped out on each line in the following order, using `|`s as separators:
`dataset|param|param_description|startdate|enddate|native_format|product|gridproj|griddef|level|level_description|levelvalue`
- `-submit [control_file_name]` is used to submit a subset request control file. Subset request control files are built from the parameters dumped out by the `-get_metadata <dsnnn.n>` option.
- `-get_status` dumps out the status of all subset requests.
- `-get_status <RequestID>` dumps out the status of subset request `RequestID`.
- `-download [RequestIndex]` download request output files for `RequestIndex` to your local system. *Only for external users*
- `-get_control_file_template` dumps out an example control file template to your local directory.
- `-get_control_file_template <dsnnn.n>` dumps out a working example control file for dsnnn.n to your local directory.

## Example

To submit an example request, try the following:

- Download an example control file for the data set of your choice, `dsnnn.n`:
```
rdams.py -get_control_file_template <dsnnn.n>
```

- Submit the example control file for "dsnnn.n" into the system as a subset request:
```
rdams.py -submit [dsnnn.n_control_file]
```

- Check on subset request processing status:
```
rdams.py -get_status
```

- Download completed requests (only for external users):
```
rdams.py -download [RequestIndex]
```

- Get a listing of parameters available for subsetting (used to populate dsnnn.n_control_file):
```
rdams.py -get_metadata dsnnn.n
```

- Download a generic control file template that includes field descriptors:
```
rdams.py -get_control_file_template
```

### Description of Parameters in Control File Template

```
dataset=dsnnn.n                              # Required, use '-get_metadata' field 'dataset'
date=YYYYMMDDHHMN/to/YYYYMMDDHHMM            # Required, use '-get_metadata' fields 'startdate' and 'enddate' as bounds
datetype=init                                # Optional, use if you would like the date range to include data based on model initialization date/time instead of valid date/time
param=SSSS/SSSS/SSSS                         # Required, use '-get_metadata' field 'param' or 'param_description'.  Separate multiple parameters with "/".
level=SSSS:NNN/NNN;SSSS:NNN;SSSS:NNN/NNN     # Optional, use '-get_metadata' field 'level' or 'level_description' for 'SSSS'.
                                             # Use '-get_metadata' field 'levelvalue' for 'NNN'.  Separate multiple level values with "/".
oformat=SSSS                                 # Optional but required if spatial subsetting is requested on select datasets. Current options are netCDF or csv for single grid point extraction. 
nlat=NN                                      # Optional, use for spatial subset requests 90 to -90
slat=NN                                      # Optional, use for spatial subset requests 90 to -90
wlon=NN                                      # Optional, use for spatial subset requests -180 to 180
elon=NN                                      # Optional, use for spatial subset requests -180 to 180
					     # To extract a single grid point at lat=yy.y,lon=xxx.x, set both nlat and slat=yy.y, and both elon and wlon = xxx.x
product=SSSS/SSSS/SSSS                       # Optional, use '-get_metadata' field 'product'.  Separate multiple products with "/".
gridproj=SSSS                                # Optional, use '-get_metadata' field 'gridproj'
griddef=SSSS                                 # Optional, use '-get_metadata' field 'griddef'
groupindex=NN                                # Optional, use '-get_summary' field 'groupindex' if available
compression=NN                               # Optional, use 'GZ' for gzip, 'Z' for unix compress, 'BZ2' for bzip2, or 'ZIP' for Zip, for external users only
targetdir=SSSS                               # Optional, request output will be created in current working directory if 'targetdir' is not set to a desired output directory.  This option is only available for NCAR HPC users.

```
