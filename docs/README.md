# RDA External Application API Description

## Table of Contents
- [Curl Syntax](#curl)
- [Wget Syntax](#wget)
- [HTTP GET Commands and Responses](#http_get)
- [HTTP POST Commands and Responses](#http_post)
- [HTTP DELETE Commands and Responses](#http_delete)


### Curl

The list below is how to perform HTTP GET, POST, and Delete commands using curl respectively.

    curl -u [RDAusername]:[RDApassword] -X GET [URL]

    curl -u [RDAusername]:[RDApassword] -X POST [URL]

    curl -u [RDAusername]:[RDApassword] -X DELETE [URL]

URL in these case could be for example `https://rda.ucar.edu/apps/summary/ds083.2` or `https://rda.ucar.edu/apps/request` or `https://rda.ucar.edu/apps/request/123456`

### WGET

The list below is how to perform HTTP GET, POST, and Delete commands using wget respectively.

    wget --user [RDAusername] --password [RDApassword] [URL]

    wget --user [RDAusername] --password [RDApassword] --header='Content-Type:application/json' --post-file [JsonControlFile] [URL]

    wget --user [RDAusername] --password [RDApassword] --method=delete [URL]

URL in these case could be for example `https://rda.ucar.edu/apps/summary/ds083.2` or `https://rda.ucar.edu/apps/request` or `https://rda.ucar.edu/apps/request/123456`

### HTTP GET

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

Returns a summary of dataset groups that have subsetting available in `dsnnn.n`.

    GET https://rda.ucar.edu/apps/metadata/[dsnnn.n]
Returns a list of all available parameters found in `dsnnn.n` for subsetting.

    GET https://rda.ucar.edu/apps/metadata/[dsnnn.n]/-f
Returns a list of all available parameters found in `dsnnn.n` for subsetting in fixed sized columns.

    GET https://rda.ucar.edu/apps/paramsummary/[dsnnn.n]
Returns a summary of all available parameters (only parameters) found in `dsnnn.n` for subsetting.

    GET https://rda.ucar.edu/apps/paramsummary/[dsnnn.n]/-f
Returns a summary of all available parameters (only parameters) found in `dsnnn.n` for subsetting in fixed sized columns.

    GET https://rda.ucar.edu/apps/template
Returns a RDA Data subset request control file template for RDA dataset `dsnnn.n`. This for use with the `rdams-client.py` tool, but can be easily mapped into a JSON structure.

    GET https://rda.ucar.edu/apps/template/[dsnnn.n]
Returns a RDA Data subset request control file template for RDA dataset `dsnnn.n`. This for use with the rdams-client.py tool, but can be easily mapped into a JSON structure. For an example see [ds131.2_control_file](ds131.2_control_file).

    POST -H "Content-Type: application/json" -d @dsnnn.n.json https://rda.ucar.edu/apps/request
Submits a RDA Data subset request by sending a JSON data structure found in the file named `dsnnn.n.json` to the RDA data server. For an example see [ds131.2.json](ds131.2.json), which is mapped from the [ds131.2_control_file](ds131.2_control_file).

    GET https://rda.ucar.edu/apps/request
Returns a summary and status of all current RDA Data Requests.

    GET https://rda.ucar.edu/apps/request/[RequestId]
Returns a summary and status of RDA Data Request `RequestId`.

    GET https://rda.ucar.edu/apps/request/[RequestId]/-proc_status
Returns only a status of RDA Data Request `RequestId`.

    GET https://rda.ucar.edu/apps/request/[RequestId]/-globus_download
Set up a Globus Endpoint Share to download RDA Data Request `RequestId`.

    GET https://rda.ucar.edu/apps/request/[RequestId]/filelist
Returns a JSON of {"FileDownloadPath":"Filesize (Bytes)"} for RDA Data Request `RequestId`.

    DELETE https://rda.ucar.edu/apps/request/[RequestId]
Purges RDA Data Request `RequestId` from RDA data server.
