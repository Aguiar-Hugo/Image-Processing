 Image Processing — CEFET/RJ

Repository with implementations of classic image processing and analysis techniques, developed during the Image Processing course at CEFET-RJ.

Each technique was split into an independent script, which can be run on its own.

## Structure

| Script | Technique | Description |
|---|---|---|
| `01_grayscale.py` | Grayscale | Converts the color image to grayscale using a weighted combination of the BGR channels. |
| `02_laplacian_convolution.py` | Laplacian Convolution | Applies manual convolution with the Laplacian kernel to highlight edges. |
| `03_erosion.py` | Erosion | Applies morphological erosion to the binarized image, using a cross-shaped structuring element. |
| `04_dilation.py` | Dilation | Applies morphological dilation to the binarized image. |
| `05_contour.py` | Contour | Extracts the contour of the binary image as the difference between the original image and its eroded version. |
| `06_region_fill.py` | Region Filling | Fills a region starting from a seed pixel, using successive dilations restricted to the image's complement. |
| `07_skeletonization.py` | Skeletonization | Obtains the morphological skeleton of the image through successive openings and erosions. |

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy
- Matplotlib

Install dependencies:

```bash
pip install opencv-python numpy matplotlib
```

## Usage

1. Place an image named `foto.jpg` in the same folder as the script you want to run.
   - If the file is not found, the script itself generates a synthetic image (a white square with a black hole in the middle) for demonstration purposes.
2. Run the desired script:

```bash
python 01_grayscale.py
```

3. The result is displayed in a window and saved as a `.png` image in the same folder (e.g., `grayscale.png`, `erosion.png`, etc.).

## Notes

- All scripts reuse the exact same functions from the original code (`converter_para_cinza`, `binarizar_imagem`, `erosao`, `dilatacao`, `extrair_contorno`, `preencher_regiao`, `esqueletizacao`, `aplicar_convolucao`), only isolating each step into its own file. Internal function/variable names remain in Portuguese, as in the original implementation.
- The structuring element used in the morphological operations (erosion, dilation, contour, region filling, skeletonization) is a 3x3 cross-shaped kernel.
