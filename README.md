
# Face Detector App

Um aplicativo intuitivo para detectar e recortar rostos automaticamente em imagens. Este projeto foi desenvolvido para automatizar o processo de criação de crachás, tornando-o fácil de usar até mesmo por usuários leigos.

## 🖼️ Funcionalidades

- **Detecção de Rostos:** Identifica e recorta automaticamente rostos em imagens.
- **Interface Intuitiva:** A interface é simples, moderna e inspirada no design do Windows 11.
- **Recorte e Salvamento:** Recorte rápido e preciso, com opções de salvar imagens.
- **Timeline Interativa:** Acompanhe o progresso do processo em uma linha do tempo visual.

## 🚀 Começando

### Pré-requisitos

Python 3.9+ com Tkinter (já incluso no instalador oficial do Python no Windows e no macOS; no Linux, instale o pacote `python3-tk`). As dependências são o OpenCV e o Pillow:

```bash
pip install -r requirements.txt
```

### Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/dssiqueira/FaceDetector.git
    cd FaceDetector
    ```

2. Configure o ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

### 🎨 Estrutura do Projeto

    ```plaintext
    /app
      /controllers
        app_controller.py  # Controlador principal do app
      /views
        ui_components.py  # Componentes da interface de usuário
        horizontal_timeline.py  # Timeline interativa
      /models
        image_processor.py  # Lógica de processamento de imagens
    /assets
      /img  # Ícones e imagens do projeto
    /tests
      test_app_controller.py  # Testes do controlador
      test_ui_components.py  # Testes dos componentes da UI
      test_horizontal_timeline.py  # Testes da timeline
      test_image_processor.py  # Testes do processamento de imagens
    main.py  # Ponto de entrada do aplicativo
    requirements.txt  # Dependências do projeto
    ```

## 🎯 Como Usar

1. Execute o aplicativo:

    ```bash
    python main.py
    ```

2. Siga os passos na interface:
   - **Carregar:** Selecione uma imagem.
   - **Analisar:** O aplicativo detectará rostos automaticamente.
   - **Recortar:** Veja os recortes e salve-os conforme necessário.

## 📚 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

1. Faça um fork do projeto
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona minha feature'`
4. Envie sua branch: `git push origin feature/minha-feature`
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙌 Agradecimentos

Feito com 💖 por [Dsiqueira](https://dsiqueira.com) - Versão 1.1
