class ColaVaciaError(Exception):
    def __init__(self):
        super().__init__("La cola está vacía.")


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


class Cola:
    def __init__(self):
        self._lista = ListaEnlazada()

    def encolar(self, dato):
        self._lista.insertar_al_final(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError()
        return self._lista.quitar_primero()

    def ver_frente(self):
        if self.esta_vacia():
            raise ColaVaciaError()
        return self._lista.primero.dato

    def esta_vacia(self) -> bool:
        return self._lista.esta_vacia()


class ColaReproduccion:
    def __init__(self):
        self._cola = Cola()

    def encolar_cancion(self, cancion: Cancion):
        self._cola.encolar(cancion)

    def siguiente(self) -> Cancion:
        return self._cola.desencolar()

    def que_sigue(self) -> Cancion:
        return self._cola.ver_frente()

# Teoría:
# El primer siguiente() devuelve "Jijiji".
# A diferencia de la pila que es LIFO (sale el último que entró), la cola es FIFO (el primero en entrar es el primero en salir), por lo que respeta el orden de llegada.