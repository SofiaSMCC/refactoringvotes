import csv
from typing import List

class VoteCounter:
    # Constructor que inicializa el archivo de votos y el diccionario para almacenar los resultados
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.results = {}

    # Extracción de método: separamos la funcionalidad de lectura del archivo en un método independiente
    # Esto mejora la modularidad y permite modificar la lógica de lectura sin afectar otras partes del código
    def read_votes(self) -> List[List[str]]:
        with open(self.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)  # Skip the header
            return list(reader)

    # Extracción de método: maneja la conversión de cadenas a enteros para evitar duplicación
    # Esto simplifica el manejo de errores, retornando 0 en caso de que no sea posible convertir
    @staticmethod
    def parse_votes(row: List[str]) -> int:
        try:
            return int(row[2])
        except ValueError:
            return 0

    # Extracción de método y nombrado claro de variables: toma un conjunto de filas y calcula el total de votos
    # Usamos "candidate" y "votes" para mejorar la legibilidad y comprensibilidad del código
    def tally_votes(self, rows: List[List[str]]) -> None:
        for row in rows:
            candidate = row[1]
            votes = self.parse_votes(row)
            # Actualiza el total de votos del candidato, usando get() para simplificar la condición
            self.results[candidate] = self.results.get(candidate, 0) + votes

    # Extracción de método: encapsula la lógica de impresión de resultados y del ganador
    # Esto permite modificar cómo se muestran los resultados sin afectar el flujo de cálculo
    '''  
    def display_results(self) -> None:
        for candidate, total_votes in self.results.items():
            print(f"{candidate}: {total_votes} votes")

        # En lugar de ordenar todos los resultados, max() encuentra el candidato con más votos
        winner = max(self.results.items(), key=lambda item: item[1])[0]
        print(f"winner is {winner}")

     '''
    def display_results(self) -> None:
        for candidate, total_votes in self.results.items():
            print(f"{candidate}: {total_votes} votes")

        # Verificamos si hay empate
        max_votes = max(self.results.values())
        winners = [candidate for candidate, votes in self.results.items() if votes == max_votes]
        
        if len(winners) > 1:
            print("It's a tie!")
        else:
            print(f"winner is {winners[0]}")



    # Función principal del proceso de contar los votos, tallar los resultados y mostrarlos
    def count_votes(self) -> None:
        rows = self.read_votes()
        self.tally_votes(rows)
        self.display_results()

# Example usage
counter = VoteCounter('votes.csv')
counter.count_votes()
