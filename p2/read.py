
buscado = 'await mongoose.connect'

with open('app/rest_server.js', 'r') as fich:
	data = fich.readlines()
	
	for i, linea in enumarate(data):
		if buscado in linea:
			data[i] = "const mongoURL = process.env.MONGO_URL || 'mongodb://" + IP-B + ":27017/bio_bbdd';"
			break
		elif:
			continue
			
	
	
with open('app/rest_server.js', 'w') as fich:
	fich.writelines(data)
	
	
buscado2 = 'const mongoURL'
with open('app/md-seed-config.js', 'r') as fich:
	data2 = fich.readlines()
	
	for i, linea in enumarate(data2):
		if buscado2 in linea:
			data2[i] = "const mongoURL = process.env.MONGO_URL || 'mongodb://" + IP-B + ":27017/bio_bbdd';"
			break
		elif:
			continue
	
	
with open('app/md-seed-config.js', 'w') as fich:
	fich.writelines(data2)


