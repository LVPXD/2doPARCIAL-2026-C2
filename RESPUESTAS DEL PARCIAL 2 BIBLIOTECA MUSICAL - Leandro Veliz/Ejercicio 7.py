class CancionNoEncontradaError(Exception):
    def __init__(self, criterio_buscado):
        super().__init__(f"No se encontró la canción: {criterio_buscado}.")


class CampoBusquedaInvalidoError(Exception):
    def __init__(self, campo):
        super().__init__(f"El campo '{campo}' no es válido para la búsqueda.")


class Cancion:
    def __init__(self, id: int, titulo: str, artista: str, album: str, genero: str, anio: int, duracion_seg: int):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = anio
        self.duracion_seg = duracion_seg

    def duracion_mmss(self) -> str:
        minutos = self.duracion_seg // 60
        segundos = self.duracion_seg % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self) -> str:
        return f"#{self.id} {self.titulo} | {self.artista} | {self.anio} | {self.duracion_mmss()}"

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, Cancion):
            return False
        return self.id == otro.id


def busqueda_lineal(canciones: list, campo: str, valor) -> list:
    if campo not in ("titulo", "artista", "genero"):
        raise CampoBusquedaInvalidoError(campo)
    resultado = []
    for cancion in canciones:
        if getattr(cancion, campo) == valor:
            resultado.append(cancion)
    return resultado


def busqueda_binaria_por_titulo(canciones_ordenadas: list, titulo: str) -> Cancion:
    izq = 0
    der = len(canciones_ordenadas) - 1
    while izq <= der:
        medio = (izq + der) // 2
        titulo_medio = canciones_ordenadas[medio].titulo
        if titulo_medio == titulo:
            return canciones_ordenadas[medio]
        elif titulo_medio < titulo:
            izq = medio + 1
        else:
            der = medio - 1
    raise CancionNoEncontradaError(titulo)

# Teoría:
# Pide la lista ordenada porque en cada paso compara con el elemento central y descarta la mitad de la lista sabiendo si el título buscado es menor o mayor alfabéticamente.
# La búsqueda binaria tiene complejidad O(log n) y la búsqueda lineal por artista tiene complejidad O(n).