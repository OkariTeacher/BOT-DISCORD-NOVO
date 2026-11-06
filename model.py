# ============================================================
# model.py - o "cérebro" do bot
# Aqui fica tudo que tem a ver com o modelo do Teachable Machine:
# carregar o arquivo .tflite, preparar a imagem e dar o palpite.
# ============================================================

import numpy as np                  # biblioteca de contas com números/matrizes (a imagem vira uma matriz)
import tensorflow as tf             # a gente só usa o tf.lite, o "leitor" de modelos .tflite
from PIL import Image, ImageOps     # Pillow: abrir, redimensionar e mexer em imagens

# Cache = "caderninho de memória".
# Carregar o modelo é lento, então carregamos UMA vez e guardamos aqui.
# Nas próximas imagens o bot só consulta o caderninho. Bem mais rápido!
_cache = {}


def _load(model_path, labels_path):
    """Carrega o modelo e os nomes das classes (só na primeira vez)."""
    key = (model_path, labels_path)  # a "etiqueta" que identifica esse par de arquivos no cache

    # Se ainda não está no caderninho, carrega agora
    if key not in _cache:
        # O Interpreter é quem "roda" o modelo .tflite
        interpreter = tf.lite.Interpreter(model_path=model_path)
        # Reserva a memória que o modelo vai precisar pra trabalhar
        interpreter.allocate_tensors()

        # Lê o labels.txt: uma linha por classe (ex: "0 Pardal", "1 Pombo")
        with open(labels_path, "r", encoding="utf-8") as f:
            class_names = [line.strip() for line in f.readlines()]  # strip tira espaços e quebras de linha

        # Guarda os dois no caderninho
        _cache[key] = (interpreter, class_names)

    return _cache[key]


def get_class(model_path, labels_path, image_path):
    """Recebe o caminho de uma imagem e devolve um texto com a classe e a confiança."""

    # Pega o modelo (carrega ou busca do cache)
    interpreter, class_names = _load(model_path, labels_path)

    # Detalhes de "por onde entra" e "por onde sai" a informação no modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # --- PREPARANDO A IMAGEM ---
    # O modelo é exigente: quer a foto num formato bem específico.

    # Abre a imagem e garante que ela é RGB (3 cores). Isso evita erro com PNG transparente, por exemplo.
    image = Image.open(image_path).convert("RGB")

    # Recorta e redimensiona pra 224x224, o tamanho que o Teachable Machine usa.
    # O "fit" mantém a proporção e corta o excesso, pra foto não ficar esticada.
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Transforma a imagem em números (cada pixel vira valores de 0 a 255)
    # e depois "normaliza" pra ficar entre -1 e 1, que é o que o modelo aprendeu a ler.
    data = (np.asarray(image).astype(np.float32) / 127.5) - 1

    # O modelo espera um LOTE de imagens, mesmo que seja uma só.
    # Esse expand_dims coloca a nossa foto dentro de um "lote de 1".
    data = np.expand_dims(data, axis=0)

    # --- HORA DO PALPITE ---
    interpreter.set_tensor(input_details[0]["index"], data)  # entrega a imagem pro modelo
    interpreter.invoke()                                      # manda o modelo pensar
    prediction = interpreter.get_tensor(output_details[0]["index"])[0]  # pega o resultado

    # "prediction" é uma lista de probabilidades, uma por classe (ex: [0.92, 0.08]).
    # O argmax descobre a posição da maior, ou seja, a classe mais provável.
    index = int(np.argmax(prediction))
    confidence = float(prediction[index])  # o quão "seguro" o modelo está (0 a 1)

    # O Teachable Machine escreve "0 Pardal". O split corta no primeiro espaço
    # e o [-1] fica só com o nome, sem o número.
    name = class_names[index].split(" ", 1)[-1]

    # Devolve a resposta já formatada. O :.2% transforma 0.9234 em "92.34%"
    return f"Classe: {name} | Confiança: {confidence:.2%}"
