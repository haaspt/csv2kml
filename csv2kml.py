# ==================================================================================================
# csv2kml.py
# ------------
#
#
# ------------------
# Patrick Tyler Haas
# patrick.tyler.haas@gmail.com
#
# ==================================================================================================

import argparse
import csv
import json
import os
import simplekml
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from progressbar import ProgressBar
from ssl import SSLError
from sys import argv

class Site(object):
    """
    Object to store information about Educational Sites.
    """

    def __init__(self, name, address, status, staffLead, email):
        self.name = name
        self.address = address
        self.status = status
        self.staffLead = staffLead
        self.email = email

    def coordinates(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class Partner(object):
    """
    Object to store information about Partner Organizations.
    """

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def coordinates(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


os.system('clear')

parser = argparse.ArgumentParser()
parser.add_argument("targetFile", help = "the CSV file to be loaded")
parser.add_argument("-i", "--internal", action = "store_true", help = "KML output is designed for internal Tandem usage")
parser.add_argument("-v", "--verbose", action = "store_true", help = "Prints verbose during address conversion")
args = parser.parse_args()

with open("googleV3API", "r") as googleAPI:
    myAPI = googleAPI.read()
    googleAPI.close()
"""
with open("AddressCache.json", "r") as infile:
    cache_data = json.load(infile)
    infile.close()
"""

def siteType():
    """Allows user to specify if the data being imported/map being exported contains Tandem Educational Partner or Tandem Organizational Partner data.
    """

    tandemEdSite = True
    validEntry = False
    while not validEntry:
        siteType = raw_input(
            "1) Tandem Educational Partners \n\n2) Tandem Organizational Partners \n\nPlease select site type: ")
        if siteType == "1":
            tandemEdSite = True
            validEntry = True
        elif siteType == "2":
            tandemEdSite = False
            validEntry = True
        else:
            print "\nYour entry is invalid, please select either '1' or '2'.\n"
            validEntry = False

    return tandemEdSite


def csvImport():
    with open(args.targetFile, 'rU') as csvfile:
        print "Loading data from CSV..."
        data = list(rec for rec in csv.reader(csvfile, delimiter=","))
        csvfile.close()
    print "CSV data loaded!"
    return data


def objectify(inData):
    """Stores data from imported CSV as attributes in a list of objects.
    """

    print "Building data structure..."

    if tandemEdSite:
        siteList = []
        for name, address, status, staffLead, email in inData:
            siteList.append(Site(name, address, status, staffLead, email))

        return siteList

    else:
        partnerList = []
        for name, address in inData:
            partnerList.append(Partner(name, address))

        return partnerList


def geoCoder(list):
    """Utilizes the geopy module to convert addresses to lat. and long.
    Google API key is stored in a separate file.
    """

    print "Converting addresses to coordinates..."
    geolocator = GoogleV3(api_key=myAPI)
    pbar = ProgressBar()
    errorCount = 0
    for site in pbar(list):
        while not hasattr(site, "latitude"):
            try:
                location = geolocator.geocode(site.address)
                site.coordinates(location.latitude, location.longitude)
                """In case of excessive timeout errors use this code:
                time.sleep(0.5)
                """
            except GeocoderTimedOut as e:
                print "Error: geocode failed on input %s with message %s" % (site.name, e)
                errorCount += 1
            except GeocoderServiceError as e:
                print "Error: geocode failed on input %s with message %s" % (site.name, e)
                errorCount += 1
            except SSLError as e:
                print "Error: geocode failed on input %s with message %s" % (site.name, e)
                errorCount += 1

    if errorCount == 0:
        print "Addresses successfully converted!"
    else:
        print "Addresses converted."
        print "Process returned %r errors." % errorCount

    return list


def kmlConvert(sitelist):
    """Converts data stored in the list of objects and converts to KML points.
    User specifies output file name, .kml file suffix is automatically appended.
    """

    kml = simplekml.Kml()


    style_dict = {"Red": "http://maps.google.com/mapfiles/kml/paddle/red-blank.png", "Yellow": "http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png", "Green": "http://maps.google.com/mapfiles/kml/paddle/grn-blank.png", "New": "http://maps.google.com/mapfiles/kml/paddle/blu-blank.png"}

    if args.internal:
        pass
    else:
        if tandemEdSite:
            site_style.iconstyle.icon.href = "http://www.tandembayarea.org/wp-content/uploads/2015/08/tandemEduMarker.png"
        else:
            site_style.iconstyle.icon.href = "http://www.tandembayarea.org/wp-content/uploads/2015/08/tandemPartMarker.png"

    for site in sitelist:
        pnt = kml.newpoint()
        site_style = simplekml.Style()
        pnt.name = site.name
        site_style.iconstyle.icon.href = style_dict[site.status]

        if args.internal:
            pnt.description = "%s \n\n %s" % (site.staffLead, site.address)
        else:
            if tandemEdSite:
                pnt.description = "For questions about this site please contact %s. \n %s" % (site.staffLead, site.email)
            else:
                pnt.description = "A Tandem Partner Site"

        pnt.coords = [(site.longitude, site.latitude)]
        pnt.style = site_style

    outputfile = raw_input("Please select output filename: ") + ".kml"
    kml.save(outputfile)
    print "File saved!"

    return

if args.internal:
    tandemEdSite = True
else:
    tandemEdSite = siteType()

data = csvImport()

siteList = objectify(data)

siteList = geoCoder(siteList)

kmlConvert(siteList)

print "Process complete. Exiting..."
