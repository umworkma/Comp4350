import models
import controllers

#for org in controllers.getAllOrganizations():
#    print org
allOrgs = controllers.getAllOrganizations()
print allOrgs
print "\n\n"

'''
aikon = controllers.getOrganizationByID(1)
print aikon
print "\n\n"
'''

'''
result = controllers.updateOrganization(1, 'NEW NAME', 'NEW DESC');
print result
newAikon = controllers.getOrganizationByID(1)
print newAikon
print "\n\n"
result = controllers.updateOrganization(1, 'Ai-kon', 'Anime & Manga conventions');
print result
oldAikon = controllers.getOrganizationByID(1)
print oldAikon
print "\n\n"
'''

#newOrg = models.Organization()
#newOrg.name = 'Dan Inc'
#newOrg.description = 'omg I hope this works'
#json = newOrg.serialize
#print json
#result = controllers.saveOrganization(json)
