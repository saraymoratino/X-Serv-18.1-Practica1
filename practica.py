#!/usr/bin/python

import webapp


def form():

	answer = "<html><body>"
	answer += "<form id='formulario' action='' method='POST'>"
	answer += "<fieldset><legend><b style= 'color:blue'>Acortador de url's</b></legend>"
	answer += "<label>URL: </label>"
	answer += "<input type='text' name='url' value='Introduce la URL' style='color:grey'/>"
	answer += "<input type='submit' value='Send' /></fieldset></form>"
	answer += "</body></html>"
	return answer

class acortador_urls(webapp.webApp):
	def parse(self, request):
		List = (request.split()[0], request.split()[1], request) #Metodo #Recurso #Peticion
		return List
	def process(self, parsedRequest):
		global url_number
		
		List = parsedRequest
		titulo = "<p><tt><i><h2 style='color:red'>URL y su URL acortada</h2></i></tt></p>"
		if List[0] == 'GET':
			file = open("urls.txt", "r");
			lines = file.read()
			try:
				url_number = int(lines.split("/")[-2].split("<")[0]) + 1
			except IndexError:
				pass # Fichero vacío
			file.close()
			if List[1] == '/':
				return ('200 OK', '<html><body>' + form() + titulo + lines + '</html></body>')
			else:
				try:
					resource = int(List[1].split("/")[1])
				except ValueError:
					html_answer = "El recurso introducido no es valido"
					return ('400 Bad Request', '<html><body><h2>' + html_answer + '</html></body></h2>')	
				short_url = "localhost:1234/" + str(resource)	 
				if short_url in lines:
					url = lines.split(short_url)[0].split("href=")[-1].split(">")[0]
					return('308 Permanent Redirect ','<html>' '<head><meta http-equiv="Refresh" content=' + "3;url=" + url + '></head>'
						   '<body><h2>Redirigiendo...</h2></body>''</html>')
				else:
					html_answer = "El recurso introducido no se encuentra dentro del fichero"
					return ('404 Not Found', '<html><body><h2>' + html_answer + '</html></body></h2>')	
				
		else:
			url = List[2].split('\r\n\r\n')[1].split('=')[1]
			if not url.startswith("http://") and not url.startswith("https://"):
				url = "http://" + url
			file = open("urls.txt", "r");
			lines = file.read()
			file.close()
			if url not in lines:
				file = open("urls.txt", "a")
				short_url = "localhost:1234/" + str(url_number)
				html_answer = '<a href=' + url + '>' + url + '</a>' + ' <a href=' + url + '>' + short_url + '</a><br>'
				file.write(html_answer)
				file.close()
				url_number += 1
			else:
				short_url = "localhost:1234/" + lines.split(url)[3].split("/")[1].split("<")[0]
				html_answer = '<a href=' + url + '>' + url + '</a>' + ' ----> ' +'<a href=' + url + '>' + short_url + '</a><br>'
			return ('200 OK', '<html><body>' + html_answer + '</html></body>')
if __name__ == "__main__":
	url_number = 0
	testWebApp = acortador_urls("localhost", 1234)
