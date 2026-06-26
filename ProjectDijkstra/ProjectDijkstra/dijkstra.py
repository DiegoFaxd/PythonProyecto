class Dijkstra:

    def __init__(self, mapa):
        self.mapa = mapa

    def calcular_ruta(self, inicio, destino):
        distancias = {inicio: 0}
        anteriores = {}
        visitados = set()
        nodos_por_visitar = [inicio]

        while len(nodos_por_visitar) > 0:
          
            nodo_actual = nodos_por_visitar[0]
            menor_distancia = distancias[nodo_actual]
            
            for nodo in nodos_por_visitar:
                if distancias[nodo] < menor_distancia:
                    menor_distancia = distancias[nodo]
                    nodo_actual = nodo

            nodos_por_visitar.remove(nodo_actual)
            visitados.add(nodo_actual)

            if nodo_actual == destino:
                break

            fila, columna = nodo_actual
            vecinos = self.mapa.vecinos(fila, columna)

            for vecino in vecinos:
                if vecino in visitados:
                    continue

                nueva_distancia = distancias[nodo_actual] + 1

                if vecino not in distancias or nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual
                    
                    if vecino not in nodos_por_visitar:
                        nodos_por_visitar.append(vecino)

        return self.reconstruir_ruta(anteriores, inicio, destino)

    def reconstruir_ruta(self, anteriores, inicio, destino):
        ruta = []
        actual = destino

        while actual != inicio:
            ruta.append(actual)
            if actual not in anteriores:
                return []
            actual = anteriores[actual]

        ruta.append(inicio)
        ruta.reverse()
        return ruta