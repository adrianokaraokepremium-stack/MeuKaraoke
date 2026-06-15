# Projeto MeuKaraoke

Sistema de automação para processamento de catálogo de karaokê. 

## 🚀 Sobre o projeto
Este projeto foi desenvolvido para organizar catálogos de karaokê de forma automatizada. Ele realiza a limpeza de nomes de artistas, gerencia duplas musicais através de uma lista de exceções e converte imagens de capa para o formato WebP, otimizando o desempenho do seu aplicativo.

## 🛠 Funcionalidades
- **Processamento de Lista:** Lê arquivos `.txt` e organiza em um banco de dados JSON.
- **Lógica Inteligente de Artistas:** Identifica participações especiais e nomes longos, mantendo apenas o nome principal, exceto para duplas cadastradas.
- **Otimização de Imagens:** Converte e redimensiona automaticamente as capas para o formato `.webp`.
- **Relatório de Erros:** Gera um log (`erros.txt`) caso alguma imagem não seja encontrada.

## ⚙️ Como usar
1. Coloque sua lista de músicas no arquivo `lista original.txt`.
2. Certifique-se de que as imagens dos cantores estejam na pasta `./assets/cantores`.
3. Execute o script principal:
   ```bash
   python gerador.py