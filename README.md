# 🤖 Bot do Discord com Inteligência Artificial

Neste projeto você vai integrar um **modelo de IA treinado no Teachable Machine** a um **bot do Discord**. O bot recebe uma imagem, analisa com o modelo e responde no chat qual é a classe (por exemplo, **Pardal** ou **Pombo**) e o quão confiante ele está. 🐦

No final, você também vai enviar o projeto para o **GitHub** e deixá-lo com cara de projeto profissional.

---

## 📚 O que você vai aprender

- ✅ Adicionar um modelo de IA treinado ao seu projeto
- ✅ O que é **inferência** e como implementá-la
- ✅ Receber arquivos (imagens) enviados no Discord
- ✅ Enviar um projeto para o GitHub usando a IDE
- ✅ Escrever um README bonito e organizado

> 💡 **Inferência** é o momento em que o modelo, já treinado, recebe um dado novo (uma foto que ele nunca viu) e dá o seu "palpite". Treinar é aprender; inferir é usar o que aprendeu.

---

## 📁 Estrutura do projeto

```
📦 meu-bot-ia
 ┣ 📜 main.py              # O bot do Discord e seus comandos
 ┣ 📜 model.py             # O "cérebro": carrega o modelo e faz a inferência
 ┣ 🧠 model_unquant.tflite # O modelo exportado do Teachable Machine
 ┗🏷️ labels.txt           # Os nomes das classes (ex: 0 Pardal / 1 Pombo)

```

---

## ⚙️ Passo 0: Preparando o ambiente

### 1. Instale as bibliotecas do projeto

O projeto já vem com o arquivo `Pipfile.lock`, que guarda a lista de todas as bibliotecas necessárias. Você não precisa instalar uma por uma!

1. Abra a pasta do projeto no VS Code e abra o terminal (`Ctrl + '`)
2. Instale o pipenv:
   ```bash
   pip install pipenv
   ```
3. Instale as bibliotecas do projeto:
   ```bash
   pipenv install
   ```

### 2. Ative o ambiente virtual

> ❗ Sempre use o ambiente virtual para não misturar as bibliotecas do projeto com as do computador.

1. No terminal, ative o ambiente:
   ```bash
   pipenv shell
   ```
2. Escolha o interpretador correto na IDE:
   - Pressione `Ctrl + Shift + P`
   - Digite **Python: Select Interpreter** e pressione `Enter`
   - Escolha o interpretador que tem **Pipenv** no nome

> 💡 Quando o ambiente estiver ativo, o terminal mostra o nome do projeto entre parênteses no começo da linha, algo como `(meu-bot-ia)`. Se não aparecer, rode `pipenv shell` de novo.

### 3. Crie seu bot e pegue o token 🔑

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em **New Application** e dê um nome
3. Vá em **Bot** → ative a opção **Message Content Intent**
4. Clique em **Reset Token** e copie o token
5. Em **OAuth2 → URL Generator**, marque `bot`, dê as permissões de enviar mensagens e ler mensagens, e use o link gerado para convidar o bot ao seu servidor

### 4. Guarde o token com segurança 🔒

> ⚠️ **NUNCA o envie para o GitHub!** Quem tiver o token controla o seu bot. Se vazar, o Discord pode invalidá-lo e você terá que gerar outro.


## 🚀 Como rodar o bot

Rode o main.py a partir do botão executar no VScode.

Se tudo deu certo, aparecerá no terminal a mensagem `LOGAMOS COMO: nome_do_bot`. No Discord, teste:

| Comando | O que faz |
|---|---|
| `$hello` | O bot se apresenta |
| `$heh 10` | O bot responde `HEHEHE...` com o número de "HE" que você pedir |
| `$check` + imagem anexada | O bot diz a classe da imagem e a confiança 🎯 |

---

## 🧩 Atividade 1: Enviando o modelo para o projeto

**Objetivos:** adicionar o modelo e o arquivo de rótulos ao projeto e descobrir como o modelo funciona nele.

### Passo a passo

1. No **Teachable Machine**, depois de treinar o modelo, clique em **Export Model**
2. Escolha a aba **TensorFlow Lite** e baixe o modelo (formato *Floating point*)
3. Extraia o `.zip`. Dentro dele há dois arquivos importantes:
   - `model_unquant.tflite` → o modelo 🧠
   - `labels.txt` → os nomes das classes 🏷️
4. **Copie os dois arquivos para a pasta do projeto**, junto do `main.py`

> 🤔 **Pense:** o que acontece se o `labels.txt` estiver em outra pasta? E se você trocar o nome do modelo? Os caminhos que passamos no código precisam bater com os nomes reais dos arquivos!

### 📄 Como é o `labels.txt`

```
0 NOME DA CLASSE
1 NOME DA CLASSE

```

A ordem das linhas é a mesma ordem das saídas do modelo. Por isso, no `model.py`, usamos o número da posição para descobrir o nome da classe.

> 💡 **Dica:** se você exportou o modelo no formato **Keras** (`keras_model.h5`), o nome do arquivo e a forma de carregar são diferentes. Este projeto usa o formato **TensorFlow Lite** (`.tflite`).

---

## 🧩 Atividade 2: Implementando a inferência

**Objetivo:** fazer o bot responder a uma imagem anexada com a saída do modelo.

### Como o `model.py` funciona

O `model.py` tem a função `get_class`, que faz todo o trabalho pesado:

```
imagem → abre e converte para RGB → redimensiona para 224x224
       → normaliza (valores entre -1 e 1) → entrega ao modelo
       → o modelo devolve probabilidades → pega a maior → devolve o texto
```

Para usar, basta chamar:

```python
from model import get_class

resultado = get_class(
    model_path="./model_unquant.tflite",
    labels_path="labels.txt",
    image_path="./foto.jpg"
)
print(resultado)  # Classe: Pardal | Confiança: 97.31%
```

### Como funciona o comando `$check` no `main.py`

```python
@bot.command()
async def check(ctx):
    # 1. Confere se a mensagem veio com algum anexo
    if ctx.message.attachments:

        # 2. Pode vir mais de uma imagem, então analisamos uma por uma
        for attachment in ctx.message.attachments:

            # 3. Baixa a imagem para a pasta do projeto
            await attachment.save(f"./{attachment.filename}")

            # 4. Manda para o modelo e responde no chat
            await ctx.send(get_class(
                model_path="./model_unquant.tflite",
                labels_path="labels.txt",
                image_path=f"./{attachment.filename}"
            ))
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")
```

### 💡 Dicas para criar a sua própria lógica

Agora é a sua vez de **personalizar o bot com as suas ideias!** Algumas sugestões:

**1. Responder só se o modelo estiver confiante**

Altere o `return` da função `get_class` (no `model.py`) para devolver também os valores separados:

```python
return name, confidence
```

E no `main.py`:

```python
nome, confianca = get_class(
    model_path="./model_unquant.tflite",
    labels_path="labels.txt",
    image_path=f"./{attachment.filename}"
)

if confianca < 0.70:
    await ctx.send("Hmm, não tenho certeza... Tente outra foto! 🤔")
else:
    await ctx.send(f"Isso é um **{nome}**! ({confianca:.0%} de certeza)")
```

**2. Respostas diferentes para cada classe**

```python
if nome == "Pardal":
    await ctx.send("🐦 Um pardalzinho! Eles vivem em bandos.")
elif nome == "Pombo":
    await ctx.send("🕊️ Um pombo! Eles são ótimos em encontrar o caminho de casa.")
```

**3. Verificar se o arquivo é mesmo uma imagem**

```python
if not attachment.filename.lower().endswith((".png", ".jpg", ".jpeg")):
    await ctx.send("Esse arquivo não é uma imagem válida :(")
    continue
```

**4. Apagar a imagem depois de analisar** (para não lotar a pasta)

```python
import os

# ... depois de enviar o resultado:
os.remove(f"./{attachment.filename}")
```

**5. Usar embeds para uma resposta mais bonita**

```python
embed = discord.Embed(title="Resultado da análise 🔍", color=discord.Color.blue())
embed.add_field(name="Classe", value=nome)
embed.add_field(name="Confiança", value=f"{confianca:.2%}")
embed.set_thumbnail(url=attachment.url)
await ctx.send(embed=embed)
```

**6. Seus próprios comandos**

```python
@bot.command()
async def ajuda(ctx):
    await ctx.send("Use `$check` e anexe uma foto para eu identificar! 📸")
```

---

## 🧩 Atividade 3: Enviando o projeto para o GitHub

**Objetivo:** consolidar a habilidade de enviar projetos para o Git pela IDE e publicar na sua conta do GitHub.

### Pelo VS Code (interface gráfica)

1. Abra a aba **Source Control** (ícone de ramificação) na barra lateral
2. Clique em **Initialize Repository**
3. Confira se o `.gitignore` está criado (o `.env` **não** pode aparecer na lista de arquivos!)
4. Escreva uma mensagem de commit (ex: `Primeira versão do bot`) e clique em **Commit**
5. Clique em **Publish Branch** e escolha criar o repositório no seu GitHub (público ou privado)

### Pelo navegador (alternativa)

1. Acesse [github.com](https://github.com) e entre na sua conta
2. Clique no **+** no canto superior direito e escolha **New repository**
3. Dê um nome ao repositório (ex: `meu-bot-ia`), escolha **Public** ou **Private** e clique em **Create repository**
4. Na página do repositório novo, clique em **uploading an existing file**
5. Abra a pasta do projeto no seu computador e **arraste os arquivos** para a página do GitHub:
   - ✅ Envie: `main.py`, `model.py`, `model_unquant.tflite`, `labels.txt`, `requirements.txt`, `.gitignore`
   - ❌ **Não envie:** `.env`, a pasta `venv/` e as imagens baixadas pelo bot
6. Escreva uma mensagem no campo **Commit changes** (ex: `Primeira versão do bot`)
7. Clique no botão verde **Commit changes**

> ⚠️ Quando você envia arquivos pelo navegador, o GitHub **não lê o `.gitignore`**. Ele envia tudo o que você arrastar, então escolha os arquivos com cuidado. Se o `.env` for enviado por engano, **gere um novo token** no Discord Developer Portal na hora.

## 🏠 Lição de casa: Embelezando o projeto

Deixe o repositório do seu bot com cara de projeto profissional! Seu **README.md** será avaliado:

| Critério | Pontos |
|---|---|
| Descrição do bot no README, mas o texto parece desestruturado | 20 |
| Descrição do bot no README, texto **estruturado**, com **emojis**, claro e bonito | 30 |
| Adicionou uma **imagem ou GIF** ⭐ | +5 extras |
| Adicionou um arquivo de **licença** ⭐ | +10 extras |

### ✍️ Dicas de Markdown

````markdown
# Título grande
## Subtítulo
**negrito**   *itálico*   `código`

- item de lista
1. item numerado

[texto do link](https://exemplo.com)

![descrição da imagem](imagens/print.png)

| Coluna A | Coluna B |
|---|---|
| valor 1  | valor 2  |
````

### O que um bom README do seu bot deve ter

- 🤖 **Nome e descrição** do que o bot faz
- ✨ **Funcionalidades** (lista de comandos)
- 🛠️ **Tecnologias usadas** (Python, discord.py, TensorFlow...)
- ▶️ **Como instalar e rodar**
- 📸 **Print ou GIF** do bot funcionando (tire um print da conversa no Discord!)
- 📄 **Licença**

### 📄 Como adicionar uma licença

1. No GitHub, abra seu repositório e clique em **Add file → Create new file**
2. Dê o nome `LICENSE`
3. Aparecerá o botão **Choose a license template**
4. Escolha uma (a **MIT License** é a mais comum para projetos de estudo) e faça o commit

---

## 🆘 Problemas comuns

| Problema | Provável causa e solução |
|---|---|
| `ModuleNotFoundError` | O ambiente virtual não está ativo ou faltou rodar `pip install -r requirements.txt` |
| O bot fica online mas **não responde aos comandos** | Ative a **Message Content Intent** no Developer Portal |
| `FileNotFoundError` no modelo ou labels | Confira se `model_unquant.tflite` e `labels.txt` estão na mesma pasta do `main.py` e se os nomes estão idênticos |
| `LoginFailure: Improper token` | Token errado, vazio ou o `.env` não foi lido. Confira o nome `DISCORD_TOKEN` |
| O bot sempre acerta "Pardal" mesmo para outras fotos | O modelo pode precisar de **mais imagens de treino** no Teachable Machine |
| Erro ao abrir a imagem | O arquivo enviado pode não ser uma imagem. Valide a extensão (dica 3) |
| `$check` não faz nada | Lembre de **anexar a imagem na mesma mensagem** do comando |

---

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- [Pillow](https://python-pillow.org/) e [NumPy](https://numpy.org/)

---

## 🚀 Próximos passos

Na próxima aula vamos aprimorar uma das suas aplicações web adicionando um toque de inteligência artificial! 🧠✨

Não precisa esperar a aula para discutir as tarefas: use o grupo de chat para trocar ideias com os colegas.
