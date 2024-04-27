import api
import requests


class Peliculas:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"


    def saludar(self) -> dict:
        url =  f"{self.base}/"
        response = requests.get(url)
        return {"status-code": response.status_code, "saludo": response.json()["result"]}


    def verificar_informacion(self, pelicula: str) -> bool:
        url =  f"{self.base}/peliculas"
        response = requests.get(url)
        return pelicula in response.json()["result"]


    def dar_informacion(self, pelicula: str) -> dict:
        url =  f"{self.base}/informacion"
        info = {"pelicula": pelicula}
        response = requests.get(url, params= info)
        return {"status-code": response.status_code, "mensaje": response.json()["result"]}


    def dar_informacion_aleatoria(self) -> dict:
        url =  f"{self.base}/aleatorio"
        response = requests.get(url)
        if response.status_code != 200:
            return {"status-code": response.status_code, "mensaje": response.json()["result"]}
        new_url = response.json()["result"]
        new_response = requests.get(new_url)
        return {"status-code": new_response.status_code, "mensaje": new_response.json()["result"]}
        

    def agregar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        url = f"{self.base}/update"
        authorization = {'Authorization': access_token}
        body = {"pelicula": pelicula, "sinopsis": sinopsis}
        response = requests.post(url, headers= authorization, data= body)
        if response.status_code == 401:
            return "Agregar pelicula no autorizado"
        if response.status_code == 400:
            return response.json()["result"]
        return "La base de la API ha sido actualizada"


    def actualizar_informacion(self, pelicula: str, sinopsis: str, access_token: str):
        url = f"{self.base}/update"
        authorization = {'Authorization': access_token}
        body = {"pelicula": pelicula, "sinopsis": sinopsis}
        response = requests.patch(url, headers= authorization, data= body)
        if response.status_code == 401:
            return "Editar información no autorizado"
        if response.status_code == 200:
            return "La base de la API ha sido actualizada"    
        return response.json()["result"]


    def eliminar_pelicula(self, pelicula: str, access_token: str):
        url = f"{self.base}/remove"
        authorization = {'Authorization': access_token}
        body = {"pelicula": pelicula}
        response = requests.delete(url, headers= authorization, data= body)
        if response.status_code == 401:
            return "Eliminar pelicula no autorizado"
        if response.status_code == 200:
            return "La base de la API ha sido actualizada"    
        return response.json()["result"]
        

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "Mamma Mia": "Mamma Mia es una Comedia musical con ABBA",
        "Monsters Inc": "Monsters Inc trata sobre monstruos que asustan, niños y risas",
        "Incredibles": "Incredibles trata de una familia de superhéroes que salva el mundo",
        "Avengers": "Avengers trata de superhéroes que luchan contra villanos poderosos",
        "Titanic": "Titanic es sobre amor trágico en el hundimiento del Titanic",
        "Akira": "Akira es una película de ciencia ficción japonesa con poderes psíquicos",
        "High School Musical": "High School Musical es un drama musical adolescente en East High",
        "The Princess Diaries": "The Princess Diaries es sobre Mia, una joven que descubre que es" 
        "princesa de Genovia",
        "Iron Man": "Iron Man trata sobre un hombre construye traje de alta tecnología "
        "para salvar al mundo",
        "Tarzan": "Tarzan es sobre un hombre criado por simios en la jungla",
        "The Pianist": "The Pianist es sobre un músico judío que sobrevive en Varsovia"
        " durante el Holocausto",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    Peliculas = Peliculas(HOST, PORT)
    print(Peliculas.saludar())
    print(Peliculas.dar_informacion_aleatoria())
    print(Peliculas.actualizar_informacion("Titanic", "Titanic es sobre amor trágico inspitado"
                                          " en el historico hundimiento del Titanic","tereiic2233"))
    print(Peliculas.verificar_informacion("Tarzan"))
    print(Peliculas.dar_informacion("The Princess Diaries"))
    print(Peliculas.dar_informacion("Monsters Inc"))
    print(Peliculas.agregar_informacion("Matilda", "Matilda es sobre una niña con poderes"
                                     "telequinéticos que enfrenta a su malvada directora", 
                                      "tereiic2233"))
    print(Peliculas.dar_informacion("Matilda"))