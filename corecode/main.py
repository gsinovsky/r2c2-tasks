from traffic import find_path
import timeit
from routeCounter import get_top_sectors

def getPath(origin,destination):

    print "\nPath to find: from %s to %s\n" %(origin,destination)

    start = timeit.default_timer()

    path = find_path(origin,destination).next()

    stop = timeit.default_timer()

    print "-------------------------------------------------------------------------"
    print "\nPath from %s to %s, calculated in %.2f minutes\n" %(origin,destination,(stop-start)/60)
    
    i = 1
    for cost, node in path:
        print "%i.Sector: %s ***** Accumulated Time: %.2f" %(i,node,cost)
        i += 1

    totalTime, sector = path[-1]
    print "\nTotal trip time (in minutes): %.2f\n" %(totalTime)
    print "-------------------------------------------------------------------------"


def getTopPaths():
    topSectors = get_top_sectors()

    for (origin,destination) in topSectors:
        getPath(origin,destination)
        

getTopPaths()