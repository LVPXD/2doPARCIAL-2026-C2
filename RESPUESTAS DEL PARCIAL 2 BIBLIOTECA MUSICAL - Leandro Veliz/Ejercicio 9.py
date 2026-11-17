import csv

ENCABEZADO_ESPERADO = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]


class ArchivoInvalidoError(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


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


def guardar_canciones_csv(ruta: str, biblioteca: Biblioteca):
    with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=",")
        escritor.writerow(ENCABEZADO_ESPERADO)
        for c in biblioteca:
            escritor.writerow([c.id, c.titulo, c.artista, c.album, c.genero, c.anio, c.duracion_seg])


def cargar_canciones_csv(ruta: str) -> Biblioteca:
    try:
        with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            try:
                encabezado = next(lector)
            except StopIteration:
                raise ArchivoInvalidoError("El archivo CSV está vacío y no tiene encabezado.")

            if encabezado != ENCABEZADO_ESPERADO:
                raise ArchivoInvalidoError("El encabezado del archivo CSV no coincide con el formato pedido.")

            biblioteca = Biblioteca()
            for num_fila, fila in enumerate(lector, start=2):
                if len(fila) < 7:
                    raise ArchivoInvalidoError(f"La fila {num_fila} tiene menos columnas de las esperadas.")
                try:
                    cancion = Cancion(
                        int(fila[0]),
                        fila[1],
                        fila[2],
                        fila[3],
                        fila[4],
                        int(fila[5]),
                        int(fila[6]),
                    )
                except ValueError:
                    raise ArchivoInvalidoError(f"Datos numéricos inválidos en la fila {num_fila}.")
                biblioteca.agregar(cancion)
            return biblioteca
    except FileNotFoundError:
        raise ArchivoInvalidoError(f"El archivo '{ruta}' no existe.")

# Teoría:
# Sí, hay que recorrer las filas anteriores porque en un archivo CSV las líneas tienen longitud variable y es necesario leer secuencialmente cada salto de línea para saber dónde empieza la fila 50.