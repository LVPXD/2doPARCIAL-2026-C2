class CancionNoEncontradaError(Exception):
    def __init__(self, id_buscado):
        super().__init__(f"No se encontró la canción con id {id_buscado}.")


class ListaVaciaError(Exception):
    def __init__(self):
        super().__init__("No se puede quitar el primer elemento porque la lista enlazada está vacía.")


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


class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class ListaEnlazada:
    def __init__(self):
        self.primero = None

    def esta_vacia(self) -> bool:
        return self.primero is None

    def tamanio(self) -> int:
        contador = 0
        actual = self.primero
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        return contador

    def insertar_al_inicio(self, dato):
        self.primero = Nodo(dato, self.primero)

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def quitar_primero(self):
        if self.primero is None:
            raise ListaVaciaError()
        dato = self.primero.dato
        self.primero = self.primero.siguiente
        return dato

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class Playlist:
    def __init__(self):
        self._lista = ListaEnlazada()

    def agregar(self, cancion: Cancion):
        self._lista.insertar_al_final(cancion)

    def quitar(self, id: int) -> Cancion:
        anterior = None
        actual = self._lista.primero
        while actual is not None:
            if actual.dato.id == id:
                if anterior is None:
                    self._lista.primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return actual.dato
            anterior = actual
            actual = actual.siguiente
        raise CancionNoEncontradaError(id)

    def listar(self) -> list:
        return [str(cancion) for cancion in self._lista]

    def duracion_total(self) -> int:
        total = 0
        for cancion in self._lista:
            total += cancion.duracion_seg
        return total

# Teoría:
# Se recorren los n nodos existentes para llegar al último y enlazar el nuevo nodo al final (complejidad O(n)).