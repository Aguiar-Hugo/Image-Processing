import cv2
import numpy as np
import matplotlib.pyplot as plt


def converter_para_cinza(imagem):
    if imagem is None:
        return None

    if len(imagem.shape) == 2:
        return imagem

    canal_azul, canal_verde, canal_vermelho = cv2.split(imagem)

    imagem_cinza = (
        0.114 * canal_azul +
        0.587 * canal_verde +
        0.299 * canal_vermelho
    )

    return imagem_cinza.astype(np.uint8)


def binarizar_imagem(imagem, limiar=127):
    _, imagem_binaria = cv2.threshold(
        imagem,
        limiar,
        255,
        cv2.THRESH_BINARY
    )
    return imagem_binaria


def erosao(imagem, elemento_estruturante):
    altura, largura = imagem.shape
    altura_kernel, largura_kernel = elemento_estruturante.shape

    margem_vertical = altura_kernel // 2
    margem_horizontal = largura_kernel // 2

    imagem_expandida = np.pad(
        imagem,
        (
            (margem_vertical, margem_vertical),
            (margem_horizontal, margem_horizontal)
        ),
        mode="constant",
        constant_values=0
    )

    resultado = np.zeros_like(imagem)

    for linha in range(altura):
        for coluna in range(largura):
            regiao = imagem_expandida[
                linha:linha + altura_kernel,
                coluna:coluna + largura_kernel
            ]

            if np.all(regiao[elemento_estruturante == 1] == 255):
                resultado[linha, coluna] = 255

    return resultado


def dilatacao(imagem, elemento_estruturante):
    altura, largura = imagem.shape
    altura_kernel, largura_kernel = elemento_estruturante.shape

    margem_vertical = altura_kernel // 2
    margem_horizontal = largura_kernel // 2

    imagem_expandida = np.pad(
        imagem,
        (
            (margem_vertical, margem_vertical),
            (margem_horizontal, margem_horizontal)
        ),
        mode="constant",
        constant_values=0
    )

    resultado = np.zeros_like(imagem)

    for linha in range(altura):
        for coluna in range(largura):
            regiao = imagem_expandida[
                linha:linha + altura_kernel,
                coluna:coluna + largura_kernel
            ]

            if np.any(regiao[elemento_estruturante == 1] == 255):
                resultado[linha, coluna] = 255

    return resultado


def abertura(imagem, elemento_estruturante):
    return dilatacao(
        erosao(imagem, elemento_estruturante),
        elemento_estruturante
    )


def esqueletizacao(imagem, elemento_estruturante):
    imagem_atual = imagem.copy()
    esqueleto = np.zeros_like(imagem)

    while np.any(imagem_atual == 255):
        imagem_aberta = abertura(
            imagem_atual,
            elemento_estruturante
        )

        camada_esqueleto = cv2.subtract(
            imagem_atual,
            imagem_aberta
        )

        esqueleto = cv2.bitwise_or(
            esqueleto,
            camada_esqueleto
        )

        imagem_atual = erosao(
            imagem_atual,
            elemento_estruturante
        )

    return esqueleto


def executar_demo():
    caminho_imagem = "foto.jpg"

    print(f"Tentando abrir: {caminho_imagem}")

    imagem_original = cv2.imread(caminho_imagem)

    if imagem_original is None:
        print("Imagem não encontrada. Criando imagem sintética.")

        imagem_original = np.zeros(
            (100, 100, 3),
            dtype=np.uint8
        )

        imagem_original[20:80, 20:80] = (
            255,
            255,
            255
        )

        imagem_original[40:60, 40:60] = (
            0,
            0,
            0
        )

    imagem_cinza = converter_para_cinza(imagem_original)
    imagem_binaria = binarizar_imagem(imagem_cinza)

    kernel_cruz = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        dtype=np.uint8
    )

    print(f"Processando imagem {imagem_cinza.shape}")

    imagem_esqueleto = esqueletizacao(
        imagem_binaria,
        kernel_cruz
    )

    plt.figure(figsize=(6, 6))
    plt.imshow(imagem_esqueleto, cmap="gray")
    plt.title("Esqueleto")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("esqueleto.png")

    try:
        plt.show()
    except Exception as erro:
        print(f"Erro ao exibir gráfico: {erro}")


if __name__ == "__main__":
    executar_demo()