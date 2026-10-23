import random
import time
import matplotlib.pyplot as plt


def quicksort_hibrido(a, corte):

    a = a[:] 

    def insertion(lo, hi):
        for i in range(lo + 1, hi + 1):
            x = a[i]
            j = i - 1
            while j >= lo and a[j] > x:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x

    def qs(lo, hi):
        while lo < hi:
            if hi - lo + 1 <= corte:
                insertion(lo, hi)
                return

            pivo = a[random.randint(lo, hi)]

            # Partição de três vias:
            # a[lo:lt] < pivo
            # a[lt:i] == pivo
            # a[gt+1:hi+1] > pivo
            lt, i, gt = lo, lo, hi

            while i <= gt:
                if a[i] < pivo:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivo:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1

            # Recursiona primeiro na menor parte
            if lt - lo < hi - gt:
                qs(lo, lt - 1)
                lo = gt + 1
            else:
                qs(gt + 1, hi)
                hi = lt - 1

    qs(0, len(a) - 1)
    return a


def quicksort_pura(a):
    return quicksort_hibrido(a, corte=1)


def medir(dados, corte, repeticoes=5):
    tempos = []

    for _ in range(repeticoes):
        arr = dados[:]

        inicio = time.perf_counter()
        resultado = quicksort_hibrido(arr, corte)
        fim = time.perf_counter()

        assert resultado == sorted(dados)
        tempos.append(fim - inicio)

    return min(tempos)


def criar_relatorio(n, cortes, resultados, tempo_puro, melhor_corte, melhor_tempo, ganho):
    linhas = []

    linhas.append("# Relatório: Quicksort híbrido com insertion sort\n")

    linhas.append(
        f"Foram ordenados **{n}** números inteiros aleatórios. "
        "O algoritmo usa **pivô aleatório**, partição em **menores, iguais e maiores** "
        "e troca para **insertion sort** quando um bloco tem tamanho menor ou igual ao corte.\n"
    )

    linhas.append("Cada configuração foi executada 5 vezes; a tabela mostra o menor tempo observado.\n")

    linhas.append("## Tabela de tempos\n")
    linhas.append("| Corte | Tempo (s) | Ganho sobre a quicksort pura |")
    linhas.append("|---:|---:|---:|")

    for corte in cortes:
        tempo = resultados[corte]
        ganho_corte = (tempo_puro - tempo) / tempo_puro * 100
        linhas.append(f"| {corte} | {tempo:.5f} | {ganho_corte:+.2f}% |")

    linhas.append("")

    linhas.append("## Gráfico\n")
    linhas.append(
        "O gráfico mostra o tempo de execução para cada valor de corte. "
        "A linha vermelha representa a quicksort pura, equivalente ao corte igual a 1.\n"
    )
    linhas.append("![Gráfico do tempo em função do corte](grafico_corte.png)\n")

    linhas.append("## Melhor corte\n")
    linhas.append(
        f"O melhor tempo foi obtido com **corte = {melhor_corte}**, "
        f"levando **{melhor_tempo:.5f} segundos**.\n"
    )
    linhas.append(
        f"Em relação à quicksort pura, o ganho foi de **{ganho:.2f}%** "
        "de redução no tempo.\n"
    )

    linhas.append("## Cortes grandes demais\n")
    linhas.append(
        "Com cortes muito grandes, o insertion sort passa a ordenar blocos grandes. "
        "Como o insertion sort tem custo quadrático, ele faz muitas comparações e deslocamentos. "
        "Por isso, após certo ponto, o tempo volta a subir e o algoritmo pode ficar "
        "mais lento que a quicksort pura.\n"
    )

    linhas.append("## Confirmação do corte = 1\n")
    linhas.append(
        "Com **corte = 1**, o insertion sort só é chamado para blocos de tamanho 1, "
        "que já estão ordenados. Portanto, o algoritmo se comporta exatamente como a "
        "**quicksort pura** com pivô aleatório e partição em menores, iguais e maiores. "
        "Isso aparece na tabela: o corte 1 tem o mesmo tempo da quicksort pura.\n"
    )

    with open("relatorio.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))


def main():
    random.seed(42)

    n = 20000
    cortes = [1, 5, 10, 16, 20, 32, 50, 100, 200]

    dados = [random.randint(0, 10**9) for _ in range(n)]

    resultados = {}
    for corte in cortes:
        resultados[corte] = medir(dados, corte)

    tempo_puro = resultados[1]
    melhor_corte = min(resultados, key=resultados.get)
    melhor_tempo = resultados[melhor_corte]
    ganho = (tempo_puro - melhor_tempo) / tempo_puro * 100

    # Gráfico
    plt.figure(figsize=(9, 5))
    plt.plot(
        cortes,
        [resultados[corte] * 1000 for corte in cortes],
        "o-",
        label="Quicksort híbrido"
    )

    plt.axhline(
        tempo_puro * 1000,
        color="red",
        linestyle="--",
        label="Quicksort pura (corte = 1)"
    )

    plt.xlabel("Corte (tamanho máximo do bloco para insertion sort)")
    plt.ylabel("Tempo (ms)")
    plt.title(f"Tempo de ordenação em função do corte — {n} elementos")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig("grafico_corte.png", dpi=150, bbox_inches="tight")
    plt.close()

    criar_relatorio(
        n=n,
        cortes=cortes,
        resultados=resultados,
        tempo_puro=tempo_puro,
        melhor_corte=melhor_corte,
        melhor_tempo=melhor_tempo,
        ganho=ganho
    )

    print("Arquivo 'relatorio.md' criado.")
    print(f"Melhor corte: {melhor_corte} ({melhor_tempo:.5f} s)")
    print(f"Ganho sobre a quicksort pura: {ganho:.2f}%")


if __name__ == "__main__":
    main()