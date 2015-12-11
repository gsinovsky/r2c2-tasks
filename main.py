from traffic import find_path

path = find_path("El Cafetal","Los Ruices").next()
i = 1

print "Path from El Cafetal to Los Ruices:"

for cost, node in path:
    print "%i.Sector: %s ***** Accumulated Time: %.2f" %(i,node,cost)
    i += 1

totalTime, sector = path[-1]
print "\nTotal trip time (in minutes): %.2f" %(totalTime)