import tkinter
import customtkinter as ctk
import requests
from pytube import YouTube
from PIL import Image, ImageTk
from tkinter import messagebox
from io import BytesIO


def fazer_dowload():
    try:
        # Pegar o vídeo que o usuário preencheu na busca
        youtube_link = link.get()
        ytObject = YouTube(youtube_link, on_progress_callback=progresso)
        video = ytObject.streams.get_highest_resolution()
        titulo = video.title

        # Mostrando o título do vídeo que o usuário vai baixar
        lbl2.configure(text=f'Título do vídeo: {titulo}', text_color='green')

        # Pegar a thumbnail
        thumbnail_url = ytObject.thumbnail_url
        thumbnail_imagem = Image.open(BytesIO(requests.get(thumbnail_url).content))

        # Mostrar a thumbnail
        thumbnail_imagem = thumbnail_imagem.resize((300,180))

        thumbnail_foto = ImageTk.PhotoImage(thumbnail_imagem)
        thumbnail_label.configure(image=thumbnail_foto)
        thumbnail_label.image = thumbnail_foto

        video.download()
        concluido.configure(text='Download Concluído')
    except:
        messagebox.showerror('Error', 'Link do vídeo é inválido')  # Mostra um erro se não for uma url válida



# Função que mede a porcentagem de download
def progresso(stream, chunk, bytes_restantes):
    tamanho_total = stream.filesize
    bytes_downloaded = tamanho_total - bytes_restantes
    porcentagem_completa = bytes_downloaded / tamanho_total * 100
    perc = str(int(porcentagem_completa))  # Converte float para int, depois converte para str para colocarmos na UI
    progresso_download.configure(text=perc + '%')
    progresso_download.update()

    progresso_barra.set(float(porcentagem_completa) / 100)


# Criando a janela
janela = ctk.CTk()
janela.geometry('720x550')
janela.title('Youtube Downloader')


lbl1 = ctk.CTkLabel(janela, text='Insira o link de um vídeo do Youtube')
lbl1.pack(padx=10, pady=10)


lbl2 = ctk.CTkLabel(janela, text='', font=('Roboto', 12))
lbl2.pack(padx=10, pady=10)


thumbnail_label = tkinter.Label(janela)
thumbnail_label.pack(padx=10, pady=10)


link = ctk.CTkEntry(janela, width=350, height=30, placeholder_text='Cole aqui o link do vídeo que deseja fazer o download')
link.pack(padx=10, pady=10)


# Criando barra de progresso
progresso_barra = ctk.CTkProgressBar(janela, width=400)
progresso_barra.set(0)
progresso_barra.pack(padx=10,pady=10)


# Criando medidor de porcentagem
progresso_download = ctk.CTkLabel(janela, text='0%')
progresso_download.pack(padx=10, pady=10)

concluido = ctk.CTkLabel(janela, text='', text_color='green')
concluido.pack(padx=10,pady=10)

botao = ctk.CTkButton(janela, command=fazer_dowload, text='Download')
botao.pack()

janela.mainloop()