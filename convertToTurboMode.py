__author__ = 'mmerth'

import sys
import csv
import re


def main(args):
    tab_file = open(args[0])
    csv_reader = csv.reader(tab_file, dialect='excel-tab')
    for row in csv_reader:
        # skip the line for the root name, we only want children of root.
        if not str.isalnum(row[5]):
            generate_turbo_mode_line(row)


def generate_turbo_mode_line(property_list):
    # First 6 columns are as follows:
    # Field?
    # DataType
    # Min
    # Max
    # Landmark
    # Root name (don't need this, since we only want the children of root)
    # Everything after are field/group names,
    # and any empty string needs to be converted to '*'

    isField = True
    dataType = ""
    minProp = ""
    maxProp = ""
    landmark = ""

    # parse column A (Field?)
    if re.match("n", str.lower(property_list[0])):
        isField = False

    # parse column B (DataType)
    if re.match("number", str.lower(property_list[1])):
        dataType = 'dataType="JDouble"'
    elif re.match("date", str.lower(property_list[1])):
        dataType = 'dataType="JDate"'
    elif re.match("time", str.lower(property_list[1])):
        dataType = 'dataType="JTime"'

    # parse column C (Min)
    if isField:
        if str.isdigit(property_list[2]):
            minProp = 'minLength="' + property_list[2] + '"'
        else:
            minProp = 'minLength="0"'
    elif str.isdigit(property_list[2]):
        minProp = 'min="' + property_list[2] + '"'

    # parse column D (Max)
    if isField and str.isdigit(property_list[3]):
        maxProp = 'maxLength="' + property_list[3] + '"'
    elif str.isdigit(property_list[3]):
        maxProp = 'max="' + property_list[3] + '"'

    # parse column E (Landmark)
    if isField and str.isalnum(property_list[4]):
        landmark = 'keyType="LANDMARK" defaultValue="' + property_list[4] + '"'
    elif str.isalnum(property_list[4]):
        landmark = 'isRecord="Y" type="' + property_list[4] + '"'


    hierarchy = ""
    # loop through all columns starting at column 7, building the hierarchy info.
    # also try to clean up the names, and create repGroups
    for column in property_list[6:]:
        column = re.sub(r'\W', "", column)
        if str.isalnum(column):
            hierarchy += column
            break
        else:
            hierarchy += "*"

    turboLine = "%s %s %s %s %s" % (hierarchy, dataType, minProp, maxProp, landmark)
    print(turboLine)

if __name__ == "__main__":
    main(sys.argv[1:])
