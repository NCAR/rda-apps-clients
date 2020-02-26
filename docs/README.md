# RDA External Application API Description

The list below is summary of the `RDA APPS_API` functions using the `cURL` syntax:

    curl -u [RDAusername]:[RDApassword] -X GET https://rda.ucar.edu/apps/summary
Returns a summary of datasets and dataset groups that have subsetting available.

    GET https://rda.ucar.edu/apps/summary/[dsnnn.n]
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
