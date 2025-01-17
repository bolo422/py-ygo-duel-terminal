# py-ygo-duel-terminal

 
- converter o banco de cartas para mongo
- criar interface para buscar infos na api do ygo pro e salvar as infos da carta atualizadas no banco de cartas. Seria bom criar um atributo q indica se a carta já foi atualizada
- cada carta vai ter o id do ygo pro, image id (id atual do banco original), e object id do mongo
- obter imagens deste repo (com image id)
- users e login
- ler ydk ou semelhante
- trunk abastecido pelo login de adm
- deck (side e extra junto)
- main (40 a 60), side (0 a 15), extra (0 a 15)
- usuário deve poder mover cartas entre deck e trunk
- exportador de ydk para levar o deck para o YGO Omega
- implementar banlists (começando com edison)
- implementar presets
- implemtnar import de ydk para preset


# Como configurar o projeto e o ambiente de desenvolvimento



Aqui está um **passo a passo** simples e objetivo para ajustar o ambiente de desenvolvimento Python, com instruções para **Windows** e **Ubuntu**. Pode ser usado diretamente em markdown.

# Passo a Passo: Ajustando o Ambiente de Desenvolvimento Python

Este guia ajuda você a configurar seu ambiente Python de desenvolvimento em **Windows** e **Ubuntu**.

## 1. Instalando o Python

### No **Windows**:
1. Baixe o Python em: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Durante a instalação, marque a opção **Add Python to PATH**.
3. Verifique a instalação no terminal:
   ```bash
   python --version
   pip --version
   ```

### No **Ubuntu**:
1. Atualize o repositório de pacotes:
   ```bash
   sudo apt update
   ```
2. Instale o Python e o `pip`:
   ```bash
   sudo apt install python3 python3-pip
   ```
3. Verifique a instalação:
   ```bash
   python3 --version
   pip3 --version
   ```

## 2. Instalando o `virtualenv`

### No **Windows**:
1. Instale o `virtualenv` globalmente:
   ```bash
   pip install virtualenv
   ```

### No **Ubuntu**:
1. Instale o `virtualenv`:
   ```bash
   sudo apt install python3-virtualenv
   ```

## 3. Criando o Ambiente Virtual

1. Navegue até o diretório do seu projeto:
   ```bash
   cd caminho/para/seu/projeto
   ```

2. Crie o ambiente virtual:
   - **No Windows**:
     ```bash
     python -m venv myenv
     ```
   - **No Ubuntu**:
     ```bash
     python3 -m venv myenv
     ```

## 4. Ativando o Ambiente Virtual

### No **Windows**:
1. Ative o ambiente virtual:
   ```bash
   .\myenv\Scripts\activate
   ```

### No **Ubuntu**:
1. Ative o ambiente virtual:
   ```bash
   source myenv/bin/activate
   ```

Após a ativação, o terminal exibirá `(myenv)` no prompt, indicando que o ambiente virtual está ativo.

## 5. Instalando Dependências

1. Com o ambiente virtual ativado, instale as dependências do seu projeto, geralmente listadas em um arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

Se não houver um `requirements.txt`, instale as dependências manualmente, por exemplo:
```bash
pip install numpy pandas
```

## 6. Desativando o Ambiente Virtual

Quando terminar de trabalhar no ambiente, desative-o com o comando:
```bash
deactivate
```

---

### Dicas:
- Sempre ative o ambiente virtual antes de rodar o seu projeto.
- Se o ambiente não estiver ativado, os pacotes poderão ser instalados globalmente, ao invés de no ambiente virtual.
- Para gerar um `requirements.txt`, use:
  ```bash
  pip freeze > requirements.txt
  ```
