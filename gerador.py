import os
import json
import shutil
import unicodedata
from PIL import Image

# Configurações
pasta_origem = './assets/cantores' 
pasta_destino = './assets/cantores_webp' 
arquivo_lista = 'lista original.txt' 
arquivo_json = 'musicas.json'
arquivo_log = 'erros.txt'
IMG_SEM_FOTO = 'sem_foto.jpg' 

# LISTA DE EXCEÇÕES: Duplas que devem aparecer completas no seu programa
EXCECOES = [
    "ADALBERTO E ADRIANO", "ADRYANA E A RAPAZIADA", "ALAN E ALADIM", "ALEX E RONALDO", 
    "ALISSON E NEIDE", "ANTONY E GABRIEL", "ANTONIO CARLOS E JOCAFI", "ATAIDE E ALEXANDRE",
    "BRUNINHO E DAVI", "BRUNO E BARRETO", "BRUNO E MARRONE", "CEZAR E PAULINHO", 
    "CHICO REY E PARANA", "CHITAOZINHO E XORORO", "CHRYSTIAN E RALF", "CLAUDINHO E BUCHECHA",
    "CLEBER E CAUAN", "CLEITON E CAMARGO", "CESAR MENOTTI E FABIANO", "DI PAULLO E PAULINO",
    "DIEGO E ARNALDO", "DINO E DENY", "DUDUCA E DALVAN", "FERNANDO E SOROCABA",
    "GIAN E GIOVANI", "GILBERTO E GILMAR", "GINO E GENO", "GUILHERME E SANTIAGO",
    "HENRIQUE E DIEGO", "HENRIQUE E JULIANO", "HUGO E TIAGO", "HUGO PENA E GABRIEL",
    "HUMBERTO E RONALDO", "JADS E JADSON", "JOAO MINEIRO E MARCIANO", "JOAO NETO E FREDERICO",
    "JOAO PAULO E DANIEL", "KLEITON E KLEDIR", "LEANDRO E LEONARDO", "LOURENCO E LOURIVAL",
    "LUIZ CLAUDIO E GIULIANO", "MAIARA E MARAISA", "MARCOS E BELUTTI", "MARIA CECILIA E RODOLFO",
    "MARLON E MAICON", "MATHEUS E KAUAN", "MATOGROSSO E MATHIAS", "MILIONARIO E JOSE RICO",
    "MUNHOZ E MARIANO", "PEDRO E THIAGO", "PEDRO PAULO E MATHEUS", "RICK E RENNER",
    "RIONEGRO E SOLIMOES", "SIMONE E SIMARIA", "SWING E SIMPATIA", "TEODORO E SAMPAIO",
    "THAEME E THIAGO", "TIAO CARREIRO E PARDINHO", "TONICO E TINOCO", "VICTOR E LEO",
    "ZE HENRIQUE E GABRIEL", "ZE NETO E CRISTIANO", "ZEZE DI CAMARGO E LUCIANO"
]

def limpar_texto(texto):
    """Remove acentos, converte para maiúsculas e remove espaços extras."""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return " ".join(texto.upper().split())

def processar_catalogo():
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    lista_musicas = []
    erros = []
    
    with open(arquivo_lista, 'r', encoding='utf-8') as f:
        for num_linha, linha in enumerate(f, 1):
            if ';' in linha:
                partes = linha.strip().split(';')
                if len(partes) >= 3:
                    artista_original = limpar_texto(partes[0])
                    codigo = limpar_texto(partes[1])
                    titulo = limpar_texto(partes[2])
                    
                    # Lógica de seleção: Mantém dupla da lista ou corta em participações
                    if artista_original in [limpar_texto(ex) for ex in EXCECOES]:
                        artista_final = artista_original
                    else:
                        separadores = [" E ", " & ", ","]
                        artista_final = artista_original
                        posicoes = [artista_original.find(sep) for sep in separadores if sep in artista_original]
                        if posicoes:
                            artista_final = artista_original[:min(posicoes)].strip()
                    
                    # Processamento de imagem e salvamento do JSON
                    nome_foto_final = f"{codigo}.webp"
                    caminho_destino = os.path.join(pasta_destino, nome_foto_final)
                    caminho_origem = os.path.join(pasta_origem, f"{artista_final}.jpg")
                    
                    if not os.path.exists(caminho_destino):
                        if os.path.exists(caminho_origem):
                            with Image.open(caminho_origem) as img:
                                img.convert('RGB').resize((200, 200), Image.Resampling.LANCZOS).save(caminho_destino, 'WEBP', quality=85)
                        else:
                            shutil.copy(IMG_SEM_FOTO, caminho_destino)
                            erros.append(f"LINHA {num_linha}: FOTO NÃO ENCONTRADA PARA '{artista_final}'")

                    lista_musicas.append({
                        "codigo": codigo,
                        "artista": artista_final,
                        "musica": titulo,
                        "foto": nome_foto_final
                    })

    # Salva o JSON final
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(lista_musicas, f, ensure_ascii=False, indent=4)
        
    # Garante que o arquivo de log sempre exista, mesmo que não haja erros
    with open(arquivo_log, 'w', encoding='utf-8') as f:
        if erros:
            for erro in erros:
                f.write(erro + "\n")
            print(f"Processamento concluído com {len(erros)} avisos (verifique o arquivo erros.txt).")
        else:
            f.write("Nenhum erro encontrado. Todas as fotos foram processadas com sucesso.")
            print("Processamento concluído com sucesso! (Log de erros vazio criado).")

if __name__ == "__main__":
    processar_catalogo()