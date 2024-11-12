# test_vote_counter.py

import unittest
from unittest.mock import patch, mock_open
from vote_counter import VoteCounter 

class TestVoteCounter(unittest.TestCase):

    # Extracción de método para crear el CSV simulado.
    # Este método evita duplicación de código, ya que genera un CSV válido o inválido según el parámetro 'valid'.
    def _get_mock_csv(self, valid=True):
        if valid:
            return """city,candidate,votes
            Springfield,Alice,1200
            Springfield,Bob,750
            Shelbyville,Alice,2000
            Shelbyville,Bob,2500"""
        else:
            return """city,candidate,votes
            Springfield,Bob,750
            Shelbyville,Alice,2000
            Springfield,Alice,invalid
            Shelbyville,Bob,2500"""

    # Extracción de método para verificar los resultados impresos.
    # Elimina la duplicación de la verificación de los resultados esperados.
    # Ahora, podemos reutilizar este método en diferentes pruebas para validar las salidas de impresión.
    def _assert_vote_results(self, mock_print, expected_calls):
        for call in expected_calls:
            mock_print.assert_any_call(call)
        self.assertEqual(mock_print.call_count, len(expected_calls))

    @patch("builtins.print")
    def test_count_votes_valid_file(self, mock_print):
        # Usamos el método "_get_mock_csv" para obtener un archivo CSV simulado con datos válidos
        mock_csv = self._get_mock_csv(valid=True)

        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")  
            counter.count_votes()
        
        # Verificamos que las impresiones correctas fueron llamadas para los votos de los candidatos y el ganador
        expected_calls = [
            "Alice: 3200 votes",
            "Bob: 3250 votes",
            "winner is Bob"
        ]
        self._assert_vote_results(mock_print, expected_calls)  # Reutilizamos el método de verificación

    @patch("builtins.print")
    def test_count_votes_invalid_votes(self, mock_print):
        # Usamos el método "_get_mock_csv" para obtener un archivo CSV simulado con datos inválidos
        mock_csv = self._get_mock_csv(valid=False)

        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv") 
            counter.count_votes()

        # Verificamos que solo los votos válidos se impriman y que el ganador correcto sea mostrado
        expected_calls = [
            "Bob: 3250 votes",
            "Alice: 2000 votes",
            "winner is Bob"
        ]
        self._assert_vote_results(mock_print, expected_calls)  # Reutilizamos el método de verificación

if __name__ == "__main__":
    unittest.main()
