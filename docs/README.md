# RDA apps clients

This repository contains the Research Data Archive (RDA) apps clients.
Subdirectories are organized by language, e.g. python, perl, c++, bash

At this stage, the (RDA) REST API clients are available for Python (2.x and 3.x), see [src/python](src/python) for more details.


# RDA External Application API Description

## Table of Contents
- [General Information](#general-info)
- [Install](#install)
- [Curl Syntax](#curl)
- [Wget Syntax](#wget)
- [HTTPS GET Commands and Responses](#https-get)
  + [Dataset Summary](#summary)
  + [Dataset Parameter Summary](#param-summary)
  + [Dataset Metadata](#metadata)
  + [Request Status](#status)
  + [Request Filelist](#filelist)
  + [Control File Template](#template)
- [HTTPS POST Commands and Responses](#https-post)
  + [Submit Subset/Format Conversion Request](#submit)
- [HTTPS DELETE Commands and Responses](#https-delete)
  + [Purge Request](#Purge)

------

### General Info

- We have written a python client to abstract the request and authentication details.
  + The client can be used as a command-line tool or as an imported python module to work with python objects directly.
  + In most cases, the client will print the JSON response after a command is entered.
  + A Jupyter Notebook was created to show the basic functionality of rdams_client.py. 
    - [The Jupyter Notebook can be found here](../src/python/rdams_client_example.ipynb)
  + [rdams_client.py can be found here](../src/python/rdams_client.py)
- All HTTPS requests to to the RDA APPS API must include a bearer token to access the API.
  + Token information can be found on [you user profile](https://rda.ucar.edu/accounts/profile)
- Responses are JSON formatted.
  + Typically, error responses will give an explaination of what went wrong in the value of the `messages` key. 
  + If `status` is `ok`, then all relevant data will be in the value of the `result` key.
- Feel free to contact the RDA with questions: [rdahelp](mailto:rdahelp@ucar.edu) or [Riley Conroy](mailto:rpconroy@ucar.edu)

------
### Install

While the python client can simply be downloaded from github and used provided you have `requests` installed, we also have a package that can be installed using pip:

    pip install rda-apps-clients

This gives you command line access to the command `rdams_client` that is a essentially an alias to rdams_client.py.
Additionally, you can programatically use the module via
    
    from rda_apps_clients import rdams_client

------
### Authentication

`POST`, `DELETE`, and some user-specific 'GET' HTTP requests require that you include a bearer token in your URL.
To do this you would need to first find your token in [you user profile](https://rda.ucar.edu/accounts/profile).

Next, you would append this token to the end of any url using `?token=[bearer token]. For example,
```
https://rda.ucar.edu/api/status/?token=dkjf93f93jf8n9vdfh
```
This step is abstracted if using the python client, `rdams_client.py`

------
### Curl

The list below is how to perform HTTPS `GET`, `POST`, and `DELETE` commands using `curl` respectively.

    curl -X GET [URL]

    curl -X POST -d @json_control_file -H 'Content-Type:application/json'[URL]

    curl -X DELETE [URL]

URL in these examples could be for example `https://rda.ucar.edu/api/summary/ds083.2` or `https://rda.ucar.edu/api/status` or `https://rda.ucar.edu/api/get_req_files/123456`

------

### WGET

The list below is how to perform HTTPS `GET`, `POST`, and `DELETE` commands using `wget` respectively.

    wget [URL]

    wget --header='Content-Type:application/json' --post-file [JsonControlFile] [URL]

    wget --method=delete [URL]

URL in these case could be for example `https://rda.ucar.edu/api/summary/ds083.2` or `https://rda.ucar.edu/api/request` or `https://rda.ucar.edu/api/request/123456`

------

### HTTPS GET


### Summary

#### Description
Returns a summary of datasets and dataset groups that have subsetting available.

#### URL

```
GET https://rda.ucar.edu/api/summary/[dsnnn.n]
```

#### Example Response
```json
{
   "request_duration": "0.049611 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "subsetting_available": true,
      "data": [
         {
            "request_type": "T",
            "group_index": 0
         },
         {
            "request_type": "T",
            "group_index": 1,
            "title": "GRIB1 6 HOURLY FILES 1999.07.30 to 2007.12.06"
         },
         {
            "request_type": "T",
            "group_index": 2,
            "title": "GRIB2 6 HOURLY FILES 2007.12.06 to current"
         }
      ]
   },
   "request_end": "2020-03-03T10:23:45.197258",
   "request_start": "2020-03-03T10:23:45.147647"
}
```

------

### Param Summary

#### Description

Returns a summary of only the Parameters in a dataset for subsetting.

#### URL

```
GET https://rda.ucar.edu/api/paramsummary/[dsnnn.n]
```

#### Example Response

```json
{
   "request_duration": "0.173482 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "dsid": "083.2",
      "subsetting_available": true,
      "data": [
         {
            "native_format": "WMO_GRIB2",
            "param": "VIS",
            "GCMD_uuid": "9337898d-68dc-43d7-93a9-6afdb4ab1784",
            "units": "m",
            "param_description": "Visibility"
         },
         {
            "param_description": "Categorical snow (yes=1; no=0)",
            "native_format": "WMO_GRIB2",
            "param": "CSNOW"
         },
         {
            "native_format": "WMO_GRIB2",
            "param": "PEVPR",
            "standard_name": "potential_water_evaporation_flux",
            "GCMD_uuid": "b68ab978-6db6-49ee-84e2-5f37b461a998",
            "units": "W m^-2",
            "param_description": "Potential evaporation rate"
         },
         {
            "native_format": "WMO_GRIB2",
            "param": "T CDC",
            "GCMD_uuid": "acb52274-6c0d-4241-a979-3fa3efca6702",
            "units": "%",
            "param_description": "Total cloud cover"
         },

         ...

         {
            "native_format": "WMO_GRIB1",
            "param": "ABSV",
            "standard_name": "atmosphere_absolute_vorticity",
            "ISO_TopicCategoryCode": "climatologyMeteorologyAtmosphere",
            "units": "s^-1",
            "GCMD_uuid": "858a80ff-5aa4-4590-b2e2-e88a802a6ee4",
            "param_description": "Absolute vorticity"
         },
         {
            "native_format": "WMO_GRIB1",
            "param": "VVEL",
            "standard_name": "lagrangian_tendency_of_air_pressure",
            "ISO_TopicCategoryCode": "climatologyMeteorologyAtmosphere",
            "units": "Pa s^-1",
            "GCMD_uuid": "841a7ac7-5981-4e93-895f-1b57c3d892a0",
            "param_description": "Vertical velocity (pressure)"
         }
      ]
   },
   "request_end": "2020-03-03T10:52:38.637789",
   "request_start": "2020-03-03T10:52:38.464307"
}

```

------

### Metadata

#### Description

Returns full metadata of a dataset available for subsetting.

#### URL

```
GET https://rda.ucar.edu/api/metadata/[dsnnn.n]
```

#### Example Response

```json
{
   "request_duration": "0.173482 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "dsid": "083.2",
      "subsetting_available": true,
      "data": [
         {
            "product": "Analysis",
            "param_description": "Convective inhibition",
            "end_date": 200712060600,
            "level": null,
            "native_format": "WMO_GRIB1",
            "gridproj": "latLon",
            "griddef": "360:181:90N:0E:90S:359E:1:1",
            "param": "CIN",
            "levels": [
               {
                  "level_description": "Ground or water surface",
                  "level": "SFC",
                  "level_value": "0"
               },
               {
                  "level_value": "0,180",
                  "level_description": "Layer between two levels at specified pressure differences from ground to level",
                  "level": "SPDY",
                  "units": "mbar"
               }
            ],
            "GCMD_uuid": "ebce0874-7635-4094-8ef4-968851873771",
            "units": "J kg^-1",
            "ISO_TopicCategoryCode": "climatologyMeteorologyAtmosphere",
            "start_date": 199907301800
         },

        ...

         {
            "product": "Analysis",
            "param_description": "Vertical velocity (pressure)",
            "end_date": 200712060600,
            "level": null,
            "native_format": "WMO_GRIB1",
            "gridproj": "latLon",
            "griddef": "360:181:90N:0E:90S:359E:1:1",
            "param": "VVEL",
            "standard_name": "lagrangian_tendency_of_air_pressure",
            "levels": [
               {
                  "level_value": "1000",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "975",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "950",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "925",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "900",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "850",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "800",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "750",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "700",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "650",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "600",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "550",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "500",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "450",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "400",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "350",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "300",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "250",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "200",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "150",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_value": "100",
                  "level_description": "Isobaric surface",
                  "level": "ISBL",
                  "units": "mbar"
               },
               {
                  "level_description": "Sigma level",
                  "level": "SIGL",
                  "level_value": "0.995"
               }
            ],
            "GCMD_uuid": "841a7ac7-5981-4e93-895f-1b57c3d892a0",
            "units": "Pa s^-1",
            "ISO_TopicCategoryCode": "climatologyMeteorologyAtmosphere",
            "start_date": 199907301800
         }
      ]
   },
   "request_end": "2020-03-03T11:32:33.317202",
   "request_start": "2020-03-03T11:32:32.453649"

```

------

### Status

#### Description

Returns that status of a given request index.
A request index is a six digit integer. 

An authentication token is needed for this for this request. See [Authentication Section](#authentication) for more details.

Or

Returns the status of all requests for user.

#### URL

```
GET https://rda.ucar.edu/api/status/[RequestIndex]
```

Or, 

```
GET https://rda.ucar.edu/api/status/
```

#### Example Response

If `[RequestIndex]` is given

```json
   {
   "request_duration": "0.046309 seconds",
   "https_response": 200,
   "messages": [],
   "result": 
   {
         "status": "Completed",
         "date_ready": "2020-03-01",
         "request_index": 410935,
         "NCAR_contact": "rpconroy@ucar.edu",
         "rqstid": "LASTNAME410935",
         "request_id": "LASTNAME410935",
         "date_purge": "2020-03-06",
         "date_rqst": "2020-03-01",
         "subset_info": {
            "note": "- Start date: 2018-01-15 00:00\n- End date: 2020-03-16 12:00\n- Parameter(s):\n    Pressure\n- Vertical level(s):\n    Specified height above ground: 80 m\n- Product(s):\n    Analysis\n- Spatial subsetting (single gridpoint):\n    Latitude: -29.5\n    Longitude: 17\n"
         }
      }
   "request_end": "2020-03-03T11:35:43.433348",
   "request_start": "2020-03-03T11:35:43.387039"
   }

```

Or if `[RequestIndex]` is not specified, get all requests

```json
   {
   "request_duration": "0.046309 seconds",
   "https_response": 200,
   "messages": [],
   "result": [
   {
         "status": "Completed",
         "date_ready": "2020-03-01",
         "request_index": 410935,
         "NCAR_contact": "rpconroy@ucar.edu",
         "rqstid": "LASTNAME410935",
         "request_id": "LASTNAME410935",
         "date_purge": "2020-03-06",
         "date_rqst": "2020-03-01",
         "subset_info": {
            "note": "- Start date: 2018-01-15 00:00\n- End date: 2020-03-16 12:00\n- Parameter(s):\n    Pressure\n- Vertical level(s):\n    Specified height above ground: 80 m\n- Product(s):\n    Analysis\n- Spatial subsetting (single gridpoint):\n    Latitude: -29.5\n    Longitude: 17\n"
         }
      },
      {
         "status": "Completed",
         "date_ready": "2020-03-01",
         "request_index": 410936,
         "NCAR_contact": "rpconroy@ucar.edu",
         "rqstid": "LASTNAME410936",
         "request_id": "LASTNAME410936",
         "date_purge": "2020-03-06",
         "date_rqst": "2020-03-01",
         "subset_info": {
            "note": "- Output format: csv\n- Start date: 2019-09-15 00:00\n- End date: 2020-03-16 12:00\n- Parameter(s):\n    u-component of wind\n- Vertical level(s):\n    Specified height above ground: 100 m\n- Product(s):\n    Analysis\n- Spatial subsetting (single gridpoint):\n    Latitude: -43.75\n    Longitude: -64.5\n"
         }
      }
   ],
   "request_end": "2020-03-03T11:35:43.433348",
   "request_start": "2020-03-03T11:35:43.387039"
   }
```

------

### Filelist

#### Description

Returns the available files generated from a request.

An authentication token is needed for this for this request. See [Authentication Section](#authentication) for more details.

#### URL

```
GET https://rda.ucar.edu/api/get_req_files/[RequestIndex]
```

#### Example Response

```json
{
    "request_duration": "0.01604 seconds",
    "https_response": 200,
    "messages": [],
    "result": {
        "total_size": 156,
        "web_files": [
            {
                "web_path": "https://rda.ucar.edu/dsrqst/LASTNAME411039/Filename.extension",
                "wfile": "Filename.extension",
                "size": 156
            }
        ]
    },
    "request_end": "2020-03-03T11:42:43.230800",
    "request_start": "2020-03-03T11:42:43.214760"
}
```

------

### Template

#### Description

Returns an example control file for a give dataset.

#### URL

```
GET https://rda.ucar.edu/api/control_file_template/[dsxxx.x]
```

#### Example Response

```json
{
   "request_duration": "0.007501 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "template": "dataset=ds083.2\ndate=201103020000/to/201103151200\nparam=TMP/R H/ABS V\nlevel=ISBL:850/700/500\noformat=netCDF\nnlat=30\nslat=-25\nwlon=-150\nelon=-30\n#groupindex=2\ntargetdir=/glade/scratch\n"
   },
   "request_end": "2020-03-03T11:44:21.842582",
   "request_start": "2020-03-03T11:44:21.835081"
}
```

------

### HTTPS POST

### Submit

#### Description

Submits a request, where the POST data is json formatted control file.

An authentication token is needed for this for this request. See [Authentication Section](#authentication) for more details.

#### URL

```
POST https://rda.ucar.edu/api/submit
```

#### Example Response

```json
{
   "request_duration": "1.171259 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "request_id": "411298"
   },
   "request_end": "2020-03-03T11:45:16.513226",
   "request_start": "2020-03-03T11:45:15.341967"
}
```

------

### HTTPS DELETE

### Purge

#### Description

Deletes a given RequestIndex. This may be necessary as Users may only have up to 8 requests open at a given time. By default an open request will be available for 7 days. Contact the specialist for the dataset to extend the amount of time it is available. 

An authentication token is needed for this for this request. See [Authentication Section](#authentication) for more details.

#### URL

```
DELETE https://rda.ucar.edu/api/purge/[RequestIndex]
```

#### Example Response

```json
{
   "request_duration": "0.243377 seconds",
   "https_response": 200,
   "messages": [],
   "result": {
      "purge_successful": "true"
   },
   "request_end": "2020-03-03T11:46:17.021646",
   "request_start": "2020-03-03T11:46:16.778269"
}
```

