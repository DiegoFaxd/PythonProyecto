class Dijkstra:

    def __init__(self, mapa):
        # Referencia al entorno para saber dónde hay muros y caminos
        self.mapa = mapa

    def calcular_ruta(self, inicio, destino):
        # Diccionario con el costo para llegar a cada nodo (el inicio cuesta 0)
        distancias = {inicio: 0}
        # Guarda de dónde venimos para luego trazar la ruta
        anteriores = {}
        # Nodos ya evaluados
        visitados = set()
        # Nodos descubiertos pendientes de revisar
        nodos_por_visitar = [inicio]

        while len(nodos_por_visitar) > 0:
            # Buscamos el nodo con la distancia más corta en nuestra lista
            nodo_actual = nodos_por_visitar[0]
            menor_distancia = distancias[nodo_actual]
            
            for nodo in nodos_por_visitar:
                if distancias[nodo] < menor_distancia:
                    menor_distancia = distancias[nodo]
                    nodo_actual = nodo

            # Lo sacamos de pendientes y lo marcamos como visitado
            nodos_por_visitar.remove(nodo_actual)
            visitados.add(nodo_actual)

            # Si ya llegamos al destino, no seguimos buscando
            if nodo_actual == destino:
                break

            # Revisamos las casillas vecinas (arriba, abajo, izq, der)
            fila, columna = nodo_actual
            vecinos = self.mapa.vecinos(fila, columna)

            for vecino in vecinos:
                if vecino in visitados:
                    continue

                # Cada paso cuesta 1
                nueva_distancia = distancias[nodo_actual] + 1

                # Si es un camino más rápido o es nuevo, actualizamos datos
                if vecino not in distancias or nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual
                    
                    if vecino not in nodos_por_visitar:
                        nodos_por_visitar.append(vecino)

        # Retornamos el resultado de armar la ruta hacia atrás
        return self.reconstruir_ruta(anteriores, inicio, destino)

    def reconstruir_ruta(self, anteriores, inicio, destino):
        ruta = []
        actual = destino

        # Vamos del destino al inicio usando el diccionario 'anteriores'
        while actual != inicio:
            ruta.append(actual)
            if actual not in anteriores:
                return [] # Retorna vacío si no hay camino posible
            actual = anteriores[actual]

        # Agregamos el punto de inicio y volteamos la lista para que quede en orden
        ruta.append(inicio)
        ruta.reverse()
        return ruta