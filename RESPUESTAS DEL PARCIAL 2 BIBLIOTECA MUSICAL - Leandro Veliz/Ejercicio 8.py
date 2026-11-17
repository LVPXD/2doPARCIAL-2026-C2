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


def ordenar_por_anio_seleccion(canciones: list) -> list:
    """Selección. Año de mayor a menor."""
    n = len(canciones)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if canciones[j].anio > canciones[max_idx].anio:
                max_idx = j
        canciones[i], canciones[max_idx] = canciones[max_idx], canciones[i]
    return canciones


def ordenar_por_duracion_insercion(canciones: list) -> list:
    """Inserción. duracion_seg de menor a mayor."""
    n = len(canciones)
    for i in range(1, n):
        actual = canciones[i]
        j = i - 1
        while j >= 0 and canciones[j].duracion_seg > actual.duracion_seg:
            canciones[j + 1] = canciones[j]
            j -= 1
        canciones[j + 1] = actual
    return canciones

# Teoría:
# En el peor caso, ambos algoritmos (selección e inserción) tienen complejidad O(n^2).
# El ordenamiento por inserción es el que conserva el orden relativo de dos canciones con la misma clave (es un algoritmo estable).