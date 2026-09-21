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

    print(f"Processando imagem {imagem_cinza.shape}")

    plt.figure(figsize=(6, 6))
    plt.imshow(imagem_cinza, cmap="gray")
    plt.title("Cinza Original")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("cinza_original.png")

    try:
        plt.show()
    except Exception as erro:
        print(f"Erro ao exibir gráfico: {erro}")


if __name__ == "__main__":
    executar_demo()