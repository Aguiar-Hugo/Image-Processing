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


def aplicar_convolucao(imagem, mascara):
    altura, largura = imagem.shape
    altura_mascara, largura_mascara = mascara.shape

    margem_vertical = altura_mascara // 2
    margem_horizontal = largura_mascara // 2

    imagem_expandida = np.zeros(
        (
            altura + 2 * margem_vertical,
            largura + 2 * margem_horizontal
        )
    )

    imagem_expandida[
        margem_vertical:margem_vertical + altura,
        margem_horizontal:margem_horizontal + largura
    ] = imagem

    resultado = np.zeros((altura, largura))

    for linha in range(altura):
        for coluna in range(largura):
            soma = 0.0

            for i in range(altura_mascara):
                for j in range(largura_mascara):
                    valor_pixel = imagem_expandida[linha + i, coluna + j]
                    peso = mascara[i, j]
                    soma += valor_pixel * peso

            resultado[linha, coluna] = min(max(soma, 0), 255)

    return resultado.astype(np.uint8)


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

    kernel_laplaciano = np.array(
        [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ],
        dtype=float
    )

    print(f"Processando imagem {imagem_cinza.shape}")

    imagem_bordas = aplicar_convolucao(
        imagem_cinza,
        kernel_laplaciano
    )

    plt.figure(figsize=(6, 6))
    plt.imshow(imagem_bordas, cmap="gray")
    plt.title("Conv. Laplaciano")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("conv_laplaciano.png")

    try:
        plt.show()
    except Exception as erro:
        print(f"Erro ao exibir gráfico: {erro}")


if __name__ == "__main__":
    executar_demo()