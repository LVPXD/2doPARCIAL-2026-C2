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


def versiones_de(biblioteca: Biblioteca, versiones: list, cancion_id: int) -> list:
    """Lista de (titulo, tipo) de todo lo derivado, sin incluir la canción original."""
    # Verifica que la canción exista en la biblioteca (si no está, lanza CancionNoEncontradaError)
    biblioteca.obtener(cancion_id)

    # Buscar versiones directas de cancion_id
    directas = [v for v in versiones if v[1] == cancion_id]

    # Ordenar de menor a mayor por cancion_id (a mano, sin usar sort ni sorted)
    for i in range(1, len(directas)):
        actual = directas[i]
        j = i - 1
        while j >= 0 and directas[j][0] > actual[0]:
            directas[j + 1] = directas[j]
            j -= 1
        directas[j + 1] = actual

    # Caso base: si no hay versiones directas, el bucle no se ejecuta y devuelve []
    resultado = []
    for ver_id, _, tipo in directas:
        cancion_ver = biblioteca.obtener(ver_id)
        resultado.append((cancion_ver.titulo, tipo))  # Preorden: primero la versión directa
        resultado.extend(versiones_de(biblioteca, versiones, ver_id))  # Luego lo que cuelga de ella

    return resultado

# Teoría:
# - Caso base: cuando ninguna canción es versión de cancion_id (como pasa con el id 70), la función no hace más llamadas recursivas y devuelve [].
# - Secuencia de llamadas para versiones_de(..., 12):
#   1. versiones_de(..., 12) llama a versiones_de(..., 13)
#   2. versiones_de(..., 13) llama a versiones_de(..., 70)
#   3. versiones_de(..., 70) es caso base y devuelve []
#   4. versiones_de(..., 13) recibe [] y devuelve [("Ji Ji Ji (Remix)", "remix")]
#   5. versiones_de(..., 12) recibe esa lista y devuelve [("Ji Ji Ji", "live"), ("Ji Ji Ji (Remix)", "remix")]