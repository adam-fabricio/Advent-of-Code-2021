"""Advent of Code 2021 do site 'https://adventofcode.com/'."""


from typing import Dict


class Submarino(object):
    """A classe submarino, implementa as funções comuns entre outras."""
    def __init__(self):
        """Define variaveis comuns do submarino."""
        
        self.posicao_x = 0
        self.posicao_y = 0
        self.posicao_aim = 0
        self.bingo = Bingo()


    def le_arquivo(self, caminho: str) -> list:
        """Le os arquivo de entrada e retorna uma lista."""
        with open(caminho) as arq:
            linhas = arq.read()
        lista = linhas.split("\n")[:-1]
        return lista

    def sonar(self, relatorio) -> list:
        """Sonar recebe uma lista de valores e gera uma lista informando se o 
        valor 'aumentou', 'diminuiu', 'não mudou' e o primeiro item é 'N/A'.
        """

        result = []
        for indice in range(len(relatorio)):
            if indice == 0:
                result.append("N/A")
            else:
                if relatorio[indice] > relatorio[indice - 1]:
                    result.append("aumentou")
                elif relatorio[indice] < relatorio[indice - 1]:
                    result.append("diminuiu")
                else:
                    result.append("nao mudou")
        return result


    def sonar_filtro(self, relatorio: list) -> list:
        """Faz um filtro no valor do relatório, gerando um compilado que é a 
        soma dos 3 ultimos valores."""

        result = []
        for index in range(len(relatorio) - 2):
            result.append(int(relatorio[index]) + int(relatorio[index + 1]) + int(relatorio[index + 2]))
        return result

    def sonar_contagem_de_ocorrencia(self, relatorio: list, ocorrencia: list) -> int:
        """Retorna o numero de ocorrencia no relatório."""

        return relatorio.count(ocorrencia)


    def forward(self, valor: str) -> None:
        self.posicao_x += int(valor)
        self.posicao_y += int(valor) * self.posicao_aim        

    def down(self, valor: str) -> None:
        self.posicao_aim += int(valor)
        

    def up(self, valor: str) -> None:
        self.posicao_aim -= int(valor)

    def movimenta(self, lista: list) -> None:
        for item in lista:
            direcao, valor = item.split(" ")
            if direcao == "forward":
                self.forward(valor)
            elif direcao == "up":
                self.up(valor)
            elif direcao == "down":
                self.down(valor)

    def separa_bit_do_diagnostico(self, bits: str) -> list:
        """Individualiza os bits da cadeia e forma um dicionario"""

        return list(map(int, list(bits)))


    def consolidar_relatorio(self, relatorio: list) -> dict:
        """Consolida os valores dos bits."""
        
        quantidade_bits = len(relatorio[0])
        lista_bit = {}
        for index in range(quantidade_bits):
            lista_bit[f"bit_{index}"] = 0


        for item in relatorio:
            for posicao, bit in enumerate(list(map(int, list(item)))):
                if bit:
                    lista_bit[f"bit_{quantidade_bits - posicao - 1}"] += 1

        for bits in lista_bit:
            if lista_bit[bits] > len(relatorio) * 0.5:
                lista_bit[bits] = 1
            
            elif lista_bit[bits] == len(relatorio) * 0.5:
                lista_bit[bits] = 1     
            
            else:
                lista_bit[bits] = 0
        
        return lista_bit


    def calcula_gamma(self, consolidado: dict) -> int:
        gamma = 0
        for indice in consolidado:
            gamma += consolidado[indice] * 2 ** int(indice.split("_")[-1])
        return gamma
    
    def calcula_epsilon(self, consolidado: dict) -> int:

        epsilon = 0

        for indice in consolidado:
            if consolidado[indice]:
                consolidado[indice] = 0
            else:
                consolidado[indice] = 1
            
            epsilon += consolidado[indice] * 2 ** int(indice.split("_")[-1])

        return epsilon

    def dividir_lista(self, relatorio: list, bit_change: str) -> list:
        resultado = [i for i in relatorio if bit_change == i[:len(bit_change)]]
        return resultado

    def calcular_gerador_oxigenio(self, relatorio:list, comum_bit: str = "") -> int:

        if len(relatorio) == 1:
            resultado_consolidado = self.consolidar_relatorio(relatorio)
            return self.calcula_gamma(resultado_consolidado)
        
        else:
            consolidado = self.consolidar_relatorio(relatorio)
            comum_bit += str(consolidado[f"bit_{len(consolidado) - 1 - len(comum_bit)}"])
            novo_consolidado = self.dividir_lista(relatorio, comum_bit)
            return self.calcular_gerador_oxigenio(novo_consolidado, comum_bit)



    def calcular_purificador_de_CO2(self, relatorio:list, comum_bit: str = "") -> int:

        if len(relatorio) == 1:
            resultado_consolidado = self.consolidar_relatorio(relatorio)
            return self.calcula_gamma(resultado_consolidado)
        
        else:
            consolidado = self.consolidar_relatorio(relatorio) 
            if consolidado[f"bit_{len(consolidado) - 1 - len(comum_bit)}"]:
                comum_bit += "0"
            else:
                comum_bit += "1"
            novo_consolidado = self.dividir_lista(relatorio, comum_bit)
            return self.calcular_purificador_de_CO2(novo_consolidado, comum_bit)


class Cartela():

    def __init__(self):
        self.cartela = []

    def adicionar_linha(self, linha: str) -> None:

        self.cartela.append([int(i) for i in linha.split(" ") if i])
    
    

class Bingo():

    def __init__(self):
        self.cartelas = []


    def gera_numeros_sorteados(self, lista_bingo: list) -> list:
        return lista_bingo[0].split(",")
    
    def criar_cartelas(self, lista_bingo: list) -> object:
        for i in range(len(lista_bingo)):
            if not i:
                pass
            elif i == len(lista_bingo) -1:
                self.cartelas[-1].adicionar_linha(lista_bingo[i])
            elif not lista_bingo[i] and lista_bingo[i+1]:
                self.cartelas.append(Cartela())
            
            elif lista_bingo[i] and lista_bingo[i+1]:
                self.cartelas[-1].adicionar_linha(lista_bingo[i])
            
            else:
            #elif lista_bingo[i] and not lista_bingo[i+1]:
                self.cartelas[-1].adicionar_linha(lista_bingo[i])
                
            



            
