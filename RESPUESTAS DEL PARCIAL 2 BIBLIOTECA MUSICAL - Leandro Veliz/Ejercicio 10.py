import os
import struct

FORMATO_ENCABEZADO = "=4s1sI"
TAMANIO_ENCABEZADO = 9  # struct.calcsize(FORMATO_ENCABEZADO) -> 9 bytes

FORMATO_REGISTRO = "=I40s40s40s16sHH"
TAMANIO_REGISTRO = 144  # struct.calcsize(FORMATO_REGISTRO) -> 144 bytes


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


def _codificar_cadena(texto: str, ancho: int) -> bytes:
    datos = texto.encode("utf-8")[:ancho]
    while len(datos) > 0:
        try:
            datos.decode("utf-8")
            break
        except UnicodeDecodeError:
            datos = datos[:-1]
    return datos


def _decodificar_cadena(datos: bytes) -> str:
    return datos.split(b"\x00", 1)[0].decode("utf-8")


def _empaquetar_cancion(c: Cancion) -> bytes:
    return struct.pack(
        FORMATO_REGISTRO,
        c.id,
        _codificar_cadena(c.titulo, 40),
        _codificar_cadena(c.artista, 40),
        _codificar_cadena(c.album, 40),
        _codificar_cadena(c.genero, 16),
        c.anio,
        c.duracion_seg,
    )


def _desempaquetar_cancion(datos: bytes) -> Cancion:
    id_c, tit, art, alb, gen, anio, dur = struct.unpack(FORMATO_REGISTRO, datos)
    return Cancion(
        id_c,
        _decodificar_cadena(tit),
        _decodificar_cadena(art),
        _decodificar_cadena(alb),
        _decodificar_cadena(gen),
        anio,
        dur,
    )


def _validar_encabezado_y_tamanio(archivo, ruta: str) -> int:
    try:
        tamanio_archivo = os.path.getsize(ruta)
    except OSError:
        raise ArchivoInvalidoError(f"El archivo '{ruta}' no existe.")

    if tamanio_archivo < TAMANIO_ENCABEZADO:
        raise ArchivoInvalidoError("El archivo es demasiado corto para tener un encabezado válido.")

    archivo.seek(0)
    datos_enc = archivo.read(TAMANIO_ENCABEZADO)
    magia, tema, cantidad = struct.unpack(FORMATO_ENCABEZADO, datos_enc)

    if magia != b"AYED":
        raise ArchivoInvalidoError("La magia del encabezado no es AYED.")
    if tema != b"M":
        raise ArchivoInvalidoError("El tema del encabezado no es M.")
    if tamanio_archivo != TAMANIO_ENCABEZADO + cantidad * TAMANIO_REGISTRO:
        raise ArchivoInvalidoError("El tamaño del archivo no coincide con la cantidad de registros indicada.")

    return cantidad


def guardar_binario(ruta: str, biblioteca: Biblioteca):
    with open(ruta, mode="wb") as archivo:
        encabezado = struct.pack(FORMATO_ENCABEZADO, b"AYED", b"M", biblioteca.cantidad())
        archivo.write(encabezado)
        for cancion in biblioteca:
            archivo.write(_empaquetar_cancion(cancion))


def cargar_binario(ruta: str) -> Biblioteca:
    try:
        with open(ruta, mode="rb") as archivo:
            cantidad = _validar_encabezado_y_tamanio(archivo, ruta)
            biblioteca = Biblioteca()
            for _ in range(cantidad):
                datos_reg = archivo.read(TAMANIO_REGISTRO)
                biblioteca.agregar(_desempaquetar_cancion(datos_reg))
            return biblioteca
    except FileNotFoundError:
        raise ArchivoInvalidoError(f"El archivo '{ruta}' no existe.")


def actualizar_registro(ruta: str, posicion: int, cancion: Cancion):
    try:
        with open(ruta, mode="r+b") as archivo:
            cantidad = _validar_encabezado_y_tamanio(archivo, ruta)
            if posicion < 0 or posicion >= cantidad:
                raise ArchivoInvalidoError(f"La posición {posicion} está fuera de rango.")
            offset = TAMANIO_ENCABEZADO + posicion * TAMANIO_REGISTRO
            archivo.seek(offset)
            archivo.write(_empaquetar_cancion(cancion))
    except FileNotFoundError:
        raise ArchivoInvalidoError(f"El archivo '{ruta}' no existe.")

# Teoría:
# La fórmula para calcular el byte donde empieza el registro k es:
# byte_inicio = 9 + k * 144  (es decir: tamaño_encabezado + k * tamaño_registro).