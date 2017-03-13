#!/usr/bin/python3

import webapp
import urllib.parse
import os.path

class contentApp (webapp.webApp):
    
    content = {}
    contentInv = {}

    def writeCSV(self, num, url):

        fich = open('url.csv', 'a') #Abrimos el fichero en modo escritura, añadiendo contenido al ya existente

        fich.write(str(num) + "," + url + "\n")

        fich.close()

    def readCSV(self):
        if os.path.isfile("url.csv"):
            fich = open('url.csv', 'r')

            for linea in fich.readlines():
                num = int(linea.split(",")[0])
                url = linea.split(",")[1]
                url = url.replace("\n", "")

                #Rellenamos los diccionarios con lo que teniamos en el fichero
                self.content[num] = url 
                self.contentInv[url] = num

            fich.close()



    def parse(self, request):
        
        return (request.split(' ', 1)[0], request.split(' ',2)[1], request.split('=')[-1], request)
                #nos quedamos con metodo        #nos quedamos con el recurso        #nos quedamos con el body
    def process(self, parsed):

        method, resourceName, body, reqComplete = parsed

        if(len(self.content) == 0):
            self.readCSV()

        
        if (method == "GET"):
            if (resourceName == "/"):
                httpCode = "200 OK"
                htmlBody = ("<html><body><form method='POST' action=''>URL:<br> <input type='text' name='url'><br><br>" +
                            "<input type='submit' value='Acortar'><br><br>" +
                            "</form></body></html>")

                for i in self.content:
                    htmlBody = htmlBody + str(i) + ": " + self.content[i] + "<br>"
            else:


                try:
                    resourceName = resourceName[1:]
                    num = int(resourceName)

                    print(self.content)

                    if num in self.content:

                        httpCode = "302 Found"
                        htmlBody = ("<html><head><meta http-equiv='refresh' content='0; " +
                                    "url=" + self.content[num] +"'></head>")

                    else:
                        httpCode = "404 Not Found"
                        htmlBody = "ERROR. Recurso no disponible"

                except ValueError:
                    httpCode = "404 Not Found"
                    htmlBody = "Introduce un numero en el recurso"
                

        elif method == "POST":     
                #si es un metodo post sin qs, devolvemos error
            if "url" not in reqComplete:
                httpCode = "404 Not Found"
                htmlBody = "Not Found. POST method without QS"
            
            else:

                body = urllib.parse.unquote(body)               
                    #si no comienza por http:// o https:// se lo añadimos

                if body == "":
                    httpCode = "200 OK"
                    htmlBody = "Introduce una url."

                else:

                    if not (body[0:7] == "http://" or body[0:8] == "https://"):
                        body = "http://" + body

                       #si la qs no esta incluida en el diccionario, la añadimos y lo guardamos en fichero
                    if not body in self.contentInv:
                        num = 1 + (len(self.content) - 1)

                        self.content[num] = body
                        self.contentInv[body] = num

                        self.writeCSV(num,body)
                    
                        httpCode = "200 OK"
                        htmlBody = ("<html><body><a href='" + self.content[num] + "'>" + str(num) + "</a>" +
                                    " --> " +
                                    "<a href='" + self.content[num] + "'>" + self.content[num] + "</a>" +
                                    "</body></html>")
                                    #Muestra como enlaces pinchables la url acortada y la url original
                    else: #si la url a acortar ya estuviera en el diccionario
                        httpCode = "200 OK"
                        htmlBody = "La url ya esta asignada"    
                
        else:
            httpCode = "404 Not Found"
            htmlBody = "Not Found"

        return (httpCode, htmlBody)


if __name__ == "__main__":

    testWebApp = contentApp("localhost", 1234)
