__author__ = 'Han'
#use the code before you change the paths
#network data: route_exclude_all_428.gdb.zip
#purpose: calculate and output shortest paths of each two points.
import arcpy, datetime, os
from arcpy import env

mypath = 'C:/Users/.../include_all_barriers/output/output'+ datetime.datetime.now().strftime("%y-%m-%d_%H_%M")
if not os.path.isdir(mypath):
   os.makedirs(mypath)
try:
    #Check out the Network Analyst extension license
    arcpy.CheckOutExtension("Network")
    #Set environment settings
    env.workspace = "C:/Users/.../include_all_barriers/route_exclude_all_428.gdb"
    env.overwriteOutput = True
    #Set local variables
    inNetworkDataset = "network/network_ND"
    impedanceAttribute = "Length"
    #pairs12102014
    f = open(r"C:\Users\...\include_all_barriers\pairs.txt", 'r+')
    n = 10000
    for line in f:
        n = n - 1
        if n == 0:
            print "10000times"
            n = 10000
            mypath = 'C:/Users/.../include_all_barriers/output/output'+ datetime.datetime.now().strftime("%y-%m-%d_%H_%M")
            if not os.path.isdir(mypath):
               os.makedirs(mypath)
            #break
        else:
            lineArray = line.split(";")
            print lineArray[0].strip()
            print lineArray[1].strip()
            lyr = lineArray[0].strip()
            lyrQuery = lineArray[1].strip()
            lyrPath = "C:/Users/.../include_all_barriers/route_exclude_all_428.gdb/Pairs/Pair"
            arcpy.MakeFeatureLayer_management ("C:/Users/.../include_all_barriers/route_exclude_all_428.gdb/network/network_ND_Junctions", lyr)
            arcpy.SelectLayerByAttribute_management (lyr, "NEW_SELECTION", lyrQuery)
            arcpy.CopyFeatures_management(lyr, lyrPath)
            

            outNALayerName = lyr
            startLocation = "Pairs/Pair"
            outDirectionsFile = mypath + "/" + outNALayerName + "Directions.txt"

            #Create a new route layer. The route starts at the distribution center and
            #takes the best sequence to visit the store locations.
            outNALayer = arcpy.na.MakeRouteLayer(inNetworkDataset, outNALayerName,
                                                 impedanceAttribute)

            #Get the layer object from the result object. The route layer can
            #now be referenced using the layer object.
            outNALayer = outNALayer.getOutput(0)

            #Get the names of all the sublayers within the route layer.
            subLayerNames = arcpy.na.GetNAClassNames(outNALayer)
            #Stores the layer names that we will use later
            stopsLayerName = subLayerNames["Stops"]

            #Load the distribution center as the start location using default field
            #mappings and search tolerance
            arcpy.na.AddLocations(outNALayer,stopsLayerName,startLocation,"","",
                                  exclude_restricted_elements = "EXCLUDE")
                                  
            fieldMappings = arcpy.na.NAClassFieldMappings(outNALayer, stopsLayerName)
            fieldMappings["Name"].mappedFieldName = "Name"
            fieldMappings["Attr_" + impedanceAttribute].mappedFieldName = "ServiceTime"
            #arcpy.na.AddLocations(outNALayer, stopsLayerName, storeLocations,
                                  #fieldMappings, "", append="APPEND",
                                  #exclude_restricted_elements = "EXCLUDE")

            #Generate driving directions in a HTML file
            arcpy.na.Directions(outNALayer,"TEXT",outDirectionsFile,"Miles",
                                "REPORT_TIME",impedanceAttribute)

            arcpy.Delete_management(lyrPath)
            print "Script completed successfully"
    f.close()
except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)


