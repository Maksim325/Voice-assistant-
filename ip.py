from ip2geotools.databases.noncommercial import DbIpCity
ip = '91.220.61.246'
respons = DbIpCity.get(ip, api_key='free')
print(respons.city)
print(respons.latitude)
print(respons.longitude)
