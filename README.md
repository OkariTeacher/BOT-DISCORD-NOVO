# 🤖 Bot de Discord com Imagens — Projeto da Turma

Projeto feito em **Python (discord.py)** para preparar o nosso bot de startup: ele vai aprender a **receber imagens enviadas pelo usuário** e, nas próximas aulas, a **classificá-las com IA**.

Este README ajuda você a **preparar o ambiente**, **rodar o bot** e **completar a atividade**.

---

## ✅ O que você precisa ter

1. **Python 3** instalado — [baixe aqui](https://www.python.org/downloads/) se ainda não tiver.
2. **VS Code** com o projeto aberto.
3. Uma **conta no Discord** e um servidor seu para testar.

---

## 📦 Bibliotecas do projeto

| Biblioteca | Para que serve |
|---|---|
| `discord.py` | Cria o bot e seus comandos |
| `numpy` | Trabalha com números e matrizes |
| `keras` | Usa modelos de inteligência artificial |
| `tensorflow` | O "motor" por trás do Keras |
| `requests` | Faz requisições na internet |
| `pillow` | Abre e manipula imagens |

---

## 🚀 Instalando as bibliotecas

Escolha **um** dos dois métodos. Os dois usam o **ambiente virtual do `pipenv`**.

### 🅰️ Método 1 — Uma a uma, e conectando o ambiente pelo VS Code

**1. Abra o terminal** do VS Code (menu *Terminal → Novo Terminal*) e instale cada biblioteca, uma por vez, esperando terminar antes de passar para a próxima:
```bash
pipenv install discord.py
pipenv install numpy
pipenv install keras
pipenv install tensorflow
pipenv install requests
pipenv install pillow
```

**2. Conecte o ambiente ao VS Code:**
1. Aperte `Ctrl + Shift + P`
2. Digite **Python: Select Interpreter** e clique na opção
3. Escolha o interpretador que tem o nome da sua pasta com **Pipenv** (algo como `Python 3.x ('nome-do-projeto-...': pipenv)`)

Pronto! Agora o VS Code usa o ambiente onde você instalou tudo. ✅

### 🅱️ Método 2 — Todas de uma vez, pelo `Pipfile`

O `Pipfile` já tem a lista de todas as bibliotecas. No terminal do VS Code, dentro da pasta do projeto, rode:
```bash
pipenv install
```
Espere terminar (☕ o TensorFlow demora um pouco). Depois, faça o mesmo passo do Método 1 para conectar o ambiente: `Ctrl + Shift + P` → **Python: Select Interpreter** → escolha o interpretador **Pipenv** do projeto.

> 💡 Se o `pipenv` não for reconhecido, instale ele primeiro com `pip install pipenv`.

---

## 🔑 Colocando o token do bot

O token é a "senha" do bot para entrar no Discord.

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications) e crie uma **New Application**.
2. No menu **Bot**, clique em **Reset Token** e copie o token.
3. Na mesma página, ligue a opção **Message Content Intent** (sem ela o bot não lê os comandos!).
4. No `main.py`, troque `"TOKEN"` no final do arquivo pelo seu token:
   ```python
   bot.run("seu_token_aqui")
   ```

> 🚨 **Nunca compartilhe seu token!** Quem tem o token controla o seu bot.

---

## ▶️ Rodando o bot

Com o `main.py` aberto, clique no botão ▶️ (canto superior direito do VS Code) ou rode no terminal:
```bash
python main.py
```
Se der certo, aparece no terminal:
```
We have logged in as NomeDoSeuBot#1234
```
Para parar, aperte `Ctrl + C` no terminal.

---

## 🖱️ Comandos que já existem

| Comando | O que faz |
|---|---|
| `$hello` | O bot se apresenta |
| `$heh 10` | O bot responde "he" repetido 10 vezes (sem número, usa 5) |

Todo comando segue o mesmo molde:
```python
@bot.command()
async def nome_do_comando(ctx):
    await ctx.send("alguma resposta")
```
- `ctx` guarda tudo sobre a mensagem recebida (quem mandou, o texto, os anexos...)
- `await ctx.send(...)` faz o bot responder

---

## 📝 Atividade — O bot que recebe imagens

**Objetivo:** criar o comando `check`. O usuário anexa uma imagem e escreve `$check` na mensagem. O bot deve **salvar a imagem** e **avisar**; se não houver imagem, deve **avisar que faltou**.

Vamos montar o comando **por etapas**, testando a cada uma. Assim você nunca fica perdido: cada etapa é pequena e usa só uma ideia nova. 🧩

> 💡 Escreva o código no `main.py`, **antes** da linha `bot.run(...)`.

---

### 🪜 Etapa 1 — Criar o comando e fazer ele responder

Copie o molde de `hello` e troque o nome do comando para `check`:

```python
@bot.command()
async def ____(ctx):
    await ctx.send("Recebi o comando!")
```
👉 Preencha o espaço com o nome do comando.

**Teste:** rode o bot e mande `$check` no Discord. Se ele responder "Recebi o comando!", você já tem a base. ✅

---

### 🪜 Etapa 2 — Descobrir se a pessoa mandou uma imagem

Os arquivos anexados à mensagem ficam em uma **lista**:
```python
ctx.message.attachments
```
- Mandou anexo → a lista **tem itens** (o Python entende como `True`)
- Não mandou nada → a lista está **vazia** (o Python entende como `False`)

Isso permite usar o `if` direto na lista. Veja um exemplo parecido, com compras:
```python
if lista_de_compras:
    print("Tem coisa na lista!")
else:
    print("A lista está vazia.")
```

Agora adapte para o seu comando: troque a mensagem da Etapa 1 por um `if`/`else`:
```python
@bot.command()
async def check(ctx):
    if ____:
        await ctx.send("Você enviou algo!")
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")
```
👉 Preencha o espaço com a lista de anexos (está logo acima!).

**Teste:** mande `$check` **com** imagem e **sem** imagem. As respostas devem ser diferentes. ✅

---

### 🪜 Etapa 3 — Passar por cada imagem enviada

A pessoa pode mandar várias imagens de uma vez. Para tratar **uma de cada vez**, usamos o `for`. Exemplo parecido, com frutas:
```python
for fruta in lista_de_frutas:
    print(fruta)
```
Leia assim: "para cada `fruta` dentro da `lista_de_frutas`, faça isso".

Agora adapte no seu comando, dentro do `if`:
```python
    if ____:
        for ____ in ____:
            await ctx.send("Achei uma imagem!")
    else:
        ...
```
👉 O primeiro e o terceiro espaço são a **lista de anexos** (a mesma do `if`). No segundo, escolha um nome para cada item (por exemplo, `anexo`).

**Teste:** mande `$check` com 1 imagem (ele responde 1 vez). Se mandar 2 imagens juntas, ele responde 2 vezes. ✅

---

### 🪜 Etapa 4 — Salvar a imagem e avisar

Cada item da lista é um anexo, e ele sabe fazer algumas coisas:

| O que você quer | Como fazer |
|---|---|
| Pegar o **nome** do arquivo | `anexo.filename` |
| **Salvar** o arquivo | `await anexo.save(caminho)` |

*(se você chamou o item de outro nome na Etapa 3, use esse nome no lugar de `anexo`)*

O `caminho` é um texto dizendo **onde** salvar. Usamos um f-string: o `./` significa "aqui na pasta do projeto", e o que estiver entre `{ }` é trocado pelo valor real. Exemplo:
```python
nome = "gato.png"
print(f"./{nome}")     # mostra: ./gato.png
```
Para manter o nome original da imagem, o valor entre as chaves deve ser o **nome do arquivo** (veja a tabela acima).

Troque o "Achei uma imagem!" por duas ações: **salvar** e **avisar**:
```python
        for anexo in ____:
            await anexo.save(f"./{____}")
            await ctx.send(f"Imagem salva em ./{____}")
```
👉 Os três espaços do meio são o **nome do arquivo** (o mesmo valor nos três lugares).

---

### 🗺️ Conferindo — como o comando completo deve se parecer

Se você seguiu as etapas, o seu código deve ter este formato (os `____` são o que você descobriu):

```python
@bot.command()
async def ____(ctx):
    if ____:
        for ____ in ____:
            await ____.save(f"./{____}")
            await ctx.send(f"Imagem salva em ./{____}")
    else:
        await ctx.send("Você esqueceu de enviar a imagem :(")
```

> 🔎 **Dica final:** se ficar preso, volte nas etapas e leia os **exemplos parecidos** (compras e frutas). A estrutura é igual, só mudam os nomes!

### ✅ Como testar tudo
1. Pare o bot (`Ctrl + C`) e rode de novo.
2. No Discord, anexe uma imagem e escreva `$check`. → O bot avisa que salvou, e a imagem aparece na pasta do projeto. 🖼️
3. Mande `$check` **sem** imagem. → O bot avisa que faltou.

### 🚀 Desafio extra
Faça o bot salvar as imagens dentro de uma pasta chamada `imagens/`. Depois, explique sua solução para um colega!

---

## 🛠️ Problemas comuns

| Problema | Possível solução |
|---|---|
| `ModuleNotFoundError: No module named 'discord'` | O VS Code não está usando o ambiente certo. Refaça: `Ctrl + Shift + P` → **Python: Select Interpreter** → escolha o **Pipenv** |
| `pipenv` não é reconhecido | Rode `pip install pipenv` |
| `Unrecognized keyword arguments passed to DepthwiseConv2D: {'groups': 1}` | Incompatibilidade de versões. Rode `pipenv uninstall tensorflow` e depois `pipenv install tensorflow==2.15` |
| `LoginFailure: Improper token` | O token está errado. Copie de novo no portal |
| O bot fica online mas não responde | Confira se ligou a **Message Content Intent** e se usou o prefixo `$` |
| Mudei o código e nada mudou | Pare o bot (`Ctrl + C`) e rode de novo |
| Não acho a imagem salva | Procure na pasta do projeto |

---

## 📚 Aprendizados desse projeto

- Como usar o **ambiente virtual** com o `pipenv`
- Como instalar bibliotecas uma a uma ou todas de uma vez
- Como funcionam os **comandos** de um bot do Discord
- Como receber e **salvar anexos** enviados pelo usuário
- A base para o próximo passo: ensinar o bot a **classificar imagens** com IA 🧠
