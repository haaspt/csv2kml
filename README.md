csv2kml
=========

Program to convert data from a properly formatted CSV file to a Google Earth KML file. Created to map Educational and Organizational Parters of Tandem, Partners in Early Learning.

Required CSV format:

- No column headers
- For educational partners: site name, site address, site status, staff lead for site, staff lead email
- For organizational partners: partner name, partner address

Required files to run:

- csv2kml: csv2kml.py
- Google API Doc: googleV3API.txt   #GoogleV3 APIs can be obtained at https://console.developers.google.com
- Properly formatted CSV file: yourfilename.csv

Execution syntax:
$ python csv2kml.py yourfilename.csv


Changes
-------

- v1.0   : 2015-08-26
           Initial stable release. Can produce maps for external consumption of either Ed or Org Partners, based on user choice.
 

To-Do
-----
- Add an address/coordinates caching system to speed the process on subsequent runs.
- Allow users to select target CSV file from inside the program, rather than as a shell argument.
- Ability to produce maps for internal organizational use.
- Allow greater flexibility in CSV formatting, CSV headers, styling, etc.