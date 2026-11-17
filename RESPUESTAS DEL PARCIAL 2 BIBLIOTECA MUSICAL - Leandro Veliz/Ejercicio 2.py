class CancionNoEncontradaError(Exception):
    def __init__(self, id_buscado):
        super().__init__(f"No se encontró la canción con id {id_buscado}.")


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


class Biblioteca:
    def __init__(self):
        self._canciones = []

    def agregar(self, cancion: Cancion):
        self._canciones.append(cancion)

    def cantidad(self) -> int:
        return len(self._canciones)

    def obtener(self, id: int) -> Cancion:
        for cancion in self._canciones:
            if cancion.id == id:
                return cancion
        raise CancionNoEncontradaError(id)

    def listar(self) -> list:
        return [str(cancion) for cancion in self._canciones]

    def __iter__(self):
        return iter(self._canciones)

# Teoría:
# La biblioteca guarda el catálogo general con todas las canciones disponibles en el sistema.
# Una playlist guarda una selección específica y ordenada de canciones armada por el usuario para reproducir.