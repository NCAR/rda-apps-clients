# RDA External Application API Description

## Table of Contents
- [General Information](#general-info)
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


### General Info

- We have written a python client to abstract the request and authentication details.
  + The client can be used as a command-line tool or as an imported python module to work with python objects directly.
  + In most cases, the client will print the JSON response after a command is entered.
  + A Jupyter Notebook was created to show the basic functionality of rdams_client.py. 
    - [rdams_client.py can be found here](../src/python/rdams_client_example.ipynb)
  + [rdams_client.py can be found here](../src/python/rdams_client.py)
- All HTTPS requests to to the RDA APPS API must have Basic Authentication headers to access the API.
  + The username and password combination would be the same as your rda.ucar.edu login combination.
- Responses are JSON formatted.
  + Typically, error responses will give an explaination of what went wrong in the value of the `messages` key. 
  + If `status` is `ok`, then all relevant data will be in the value of the `result` key.
- Feel free to contact the RDA with questions: [rdahelp](mailto:rdahelp@ucar.edu) or [Riley Conroy](mailto:rpconroy@ucar.edu)


### Curl

The list below is how to perform HTTPS GET, POST, and Delete commands using curl respectively.

    curl -u [RDAusername]:[RDApassword] -X GET [URL]

    curl -u [RDAusername]:[RDApassword] -X POST [URL]

    curl -u [RDAusername]:[RDApassword] -X DELETE [URL]

URL in these case could be for example `https://rda.ucar.edu/apps/summary/ds083.2` or `https://rda.ucar.edu/apps/request` or `https://rda.ucar.edu/apps/request/123456`

### WGET

The list below is how to perform HTTPS GET, POST, and Delete commands using wget respectively.

    wget --user [RDAusername] --password [RDApassword] [URL]

    wget --user [RDAusername] --password [RDApassword] --header='Content-Type:application/json' --post-file [JsonControlFile] [URL]

    wget --user [RDAusername] --password [RDApassword] --method=delete [URL]

URL in these case could be for example `https://rda.ucar.edu/apps/summary/ds083.2` or `https://rda.ucar.edu/apps/request` or `https://rda.ucar.edu/apps/request/123456`

### HTTPS GET

### Summary

#### Description
Returns a summary of datasets and dataset groups that have subsetting available.

#### URL

```
GET https://rda.ucar.edu/apps/summary/[dsnnn.n]
```

#### Example Response
```json
{
   "status": "ok",
   "request_duration": "0.049611 seconds",
   "code": 200,
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

### Param Summary

#### Description

Returns a summary of only the Parameters in a dataset for subsetting.

#### URL

```
GET https://rda.ucar.edu/apps/paramsummary/[dsnnn.n]
```

#### Example Response

```json
{
   "status": "ok",
   "request_duration": "0.173482 seconds",
   "code": 200,
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

### Metadata

#### Description

Returns full metadata of a dataset available for subsetting.

#### URL

```
GET https://rda.ucar.edu/apps/metadata/[dsnnn.n]
```

#### Example Response

```json

```

### Status

#### Description

Returns that status of a given request index.
A request index is a six digit integer.

#### URL

```
GET https://rda.ucar.edu/apps/request/[RequestIndex]
```

#### Example Response

```json

```

### Filelist

#### Description

Returns the available files generated from a request.

#### URL

```
GET https://rda.ucar.edu/apps/request/[RequestIndex]/filelist
```

#### Example Response

```json

```

### Template

#### Description

Returns an example control file for a give dataset.

#### URL

```
GET https://rda.ucar.edu/apps/request/template/[dsxxx.x]
```

#### Example Response

```json
```

### HTTPS POST

### Submit

#### Description

Submits a request, where the post data is json formatted control file

#### URL

```
POST https://rda.ucar.edu/apps/request/
```

#### Example Response

```json
```

### HTTPS DELETE

### Purge

#### Description

Deletes a given RequestIndex. This may be necessary as Users may only have up to 8 requests open at a given time. By default an open request will be available for 7 days. Contact the specialist for the dataset to extend the amount of time it is available. 

#### URL

```
DELETE https://rda.ucar.edu/apps/request/[RequestIndex]
```

#### Example Response

```json
```

