from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import PySimpleGUI as sg
lt=[
    [sg.Text('Informe o link do vídeo', size=(10, 0)),
    sg.InputText(size=(70, 0), key='link'), sg.Stretch()],
    [sg.Text('Local do arquivo:'), sg.InputText('c:/',key='caminho'),
    sg.FolderBrowse('Caminho...', size=(20, 1)), sg.Stretch()],
    [sg.Radio('Apenas Áudio', group_id='res',key='audio'),
     sg.Radio('Menor Resolução', group_id='res',key='menor', default=True),
     sg.Radio('Maior Resolução', group_id='res',key='maior'),
     sg.Checkbox('Lista',key='lista')],
    [sg.Button('Informações', size=(21, 2), key='info', disabled=False),
    sg.Button('Baixar', size=(21, 2), key='baixar', disabled=False),
    sg.Button('Sair', size=(21, 2), key='sair'), sg.Stretch()],
    [sg.Text('', key='final', size=(80, 1))],
    [sg.Output(size=(80,20), key='out'), sg.Stretch()]
]
janela = sg.Window('Downloader do Youtube',size=(600, 500), resizable=True).layout(lt)
def baixarArquivo(x):
    lk = YouTube(x, on_progress_callback=on_progress)
    lk = YouTube(x)
    print(f'Baixando:\nTítulo: {lk.title}')
    titulo = lk.title
    titulo = titulo.replace(r'/', ' ')
    titulo = titulo.replace(r'|', ' ')
    titulo = titulo.replace(r'?', ' ')
    titulo = titulo.replace(r'"', '')
    if valor['audio'] == True:
        baixar = lk.streams.get_audio_only()
        baixar.download(filename=f'{titulo}.mp3', output_path='baixados/audio')
    if valor['menor'] == True:
        baixar = lk.streams.get_lowest_resolution()
        baixar.download(filename=f'{titulo}.mp4', output_path='baixados/video/menor')
    if valor['maior'] == True:
        baixar = lk.streams.get_highest_resolution()
        baixar.download(filename=f'{titulo}.mp4', output_path='baixados/video/maior')
def baixarLista(link):
    lista = Playlist(link)
    for lnk in lista:
        baixarArquivo(lnk)
    print('Concluido')
def dadosLista(link):
    lista = Playlist(link)
    titulo=[]
    imagem=[]
    data=[]
    tamanho=[]
    for lnk in lista:
        try:
            lk = YouTube(lnk, on_progress_callback=on_progress)
            titulo.append(lk.title)
            imagem.append(lk.thumbnail_url)
            tamanho.append(lk.length)
            data.append(format(lk.publish_date,'%d/%m/%Y'))
            print(f'Título: {titulo[-1]}\n         Tempo em segundos: {tamanho[-1]} - Data de publicação: {data[-1]}')
        except:
            janela['final'].update("Existe um problema, favor tentar novamente")
    print(f'\nQuantidade de vídeos: {len(titulo)}')
def dadosArquivo(lnk):
    try:
        lk = YouTube(lnk, on_progress_callback=on_progress)
        titulo=lk.title
        imagem=lk.thumbnail_url
        tamanho=lk.length
        data=format(lk.publish_date, '%d/%m/%Y')
        print(f'Título: {titulo}\n         Tempo em segundos: {tamanho} - Data de publicação: {data}')
    except:
        janela['final'].update("Existe um problema, favor tentar novamente")
while True:
    evento, valor = janela.Read()
    if (evento == 'sair' or evento == sg.WINDOW_CLOSED):
        break
        quit()
    else:
        link = valor['link']
        if(evento == "info"):
            janela['final'].update("INFORMAÇÕES")
            print('INFORMAÇÕES')
            if (valor['lista'] == True):
                print('LINK É UMA LISTA')
                dadosLista(link)
            else:
                dadosArquivo(link)
        if(evento == "baixar"):
            janela['final'].update("BAIXAR")
            if (valor['lista'] == True):
                print('É UMA LISTA\n')
                baixarLista(link)
            else:
                print('É UM ARQUIVO\n')
                baixarArquivo(link)
    janela['final'].update('Concluído')
# pyinstaller --onefile -w youtube.py