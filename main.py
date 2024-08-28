import numpy as np

# Função para inicializar a matriz de feromônio
def inicializar_feromonio(num_cidades):
    return np.ones((num_cidades, num_cidades)) * 1e-6

# Função para calcular a distância total de um caminho
def calcular_distancia(caminho, matriz_distancias):
    distancia = 0
    for i in range(len(caminho) - 1):
        distancia += matriz_distancias[caminho[i], caminho[i + 1]]
    distancia += matriz_distancias[caminho[-1], caminho[0]]  # Fechando o ciclo
    return distancia

# Função de probabilidade para escolher a próxima cidade
def calcular_probabilidade(feromonio, visibilidade, alpha, beta):
    total = np.sum((feromonio ** alpha) * (visibilidade ** beta))
    probabilidade = ((feromonio ** alpha) * (visibilidade ** beta)) / total
    return probabilidade

# Atualização de feromônio
def atualizar_feromonio(feromonio, caminhos, qualidade_caminhos, rho, Q):
    delta_feromonio = np.zeros_like(feromonio)
    for k in range(len(caminhos)):
        for i in range(len(caminhos[k]) - 1):
            delta_feromonio[caminhos[k][i], caminhos[k][i + 1]] += Q / qualidade_caminhos[k]
        delta_feromonio[caminhos[k][-1], caminhos[k][0]] += Q / qualidade_caminhos[k]

    feromonio = (1 - rho) * feromonio + delta_feromonio
    return feromonio

# Função principal do Ant System
def ant_system(matriz_distancias, num_formigas, max_iteracoes, alpha, beta, rho, Q):
    num_cidades = len(matriz_distancias)
    feromonio = inicializar_feromonio(num_cidades)
    melhor_caminho = None
    melhor_distancia = float('inf')

    for iteracao in range(max_iteracoes):
        formigas_caminhos = []
        qualidade_caminhos = []

        for ant in range(num_formigas):
            cidade_atual = np.random.randint(num_cidades)
            caminho = [cidade_atual]
            nao_visitadas = set(range(num_cidades))
            nao_visitadas.remove(cidade_atual)

            for _ in range(num_cidades - 1):
                visibilidade = 1 / matriz_distancias[cidade_atual, list(nao_visitadas)]
                probabilidade = calcular_probabilidade(feromonio[cidade_atual, list(nao_visitadas)], visibilidade, alpha, beta)
                proxima_cidade = np.random.choice(list(nao_visitadas), p=probabilidade / np.sum(probabilidade))
                caminho.append(proxima_cidade)
                cidade_atual = proxima_cidade
                nao_visitadas.remove(cidade_atual)

            formigas_caminhos.append(caminho)
            qualidade_caminhos.append(calcular_distancia(caminho, matriz_distancias))

            if qualidade_caminhos[-1] < melhor_distancia:
                melhor_caminho = caminho
                melhor_distancia = qualidade_caminhos[-1]

        feromonio = atualizar_feromonio(feromonio, formigas_caminhos, qualidade_caminhos, rho, Q)

    return melhor_caminho, melhor_distancia

# Exemplo de uso
if __name__ == "__main__":
    # Substitua a matriz de distâncias pelo seu conjunto de dados
    matriz_distancias = np.array([[0, 2, 9, 10],
                                  [1, 0, 6, 4],
                                  [15, 7, 0, 8],
                                  [6, 3, 12, 0]])

    num_formigas = 5
    max_iteracoes = 100
    alpha = 1
    beta = 5
    rho = 0.5
    Q = 100

    melhor_caminho, melhor_distancia = ant_system(matriz_distancias, num_formigas, max_iteracoes, alpha, beta, rho, Q)

    print("Melhor caminho:", melhor_caminho)
    print("Melhor distância:", melhor_distancia)
