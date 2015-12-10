from traffic import find_path

print "Path from El Cafetal to Los Ruices:"
path = find_path("El Cafetal","Los Ruices").next()

print path
i = 0

for cost, node in path:
    print "%i.Sector: %s Cost: %.2f" %(i,node,cost)
    i += 1
