import PySimpleGUI as sg
from moviepy.editor import VideoFileClip
from os import path, environ

sg.theme('DarkGrey10')  #Define o tema da tela principal.

layout = [  #Define a organização do layout e seus paramêtros
    [sg.Text(size=(20, 1)), sg.Text('Bem vindo ao Conversor')],
    [sg.Text()],
    [sg.Text("Escolha o arquivo a converter:", size=(22, 1)), sg.Input(size=(27, 1), tooltip='Diretório do arquivo', key='-arquivo-', background_color='black'), sg.FileBrowse('Procurar', size=(10, 1))],
    [sg.Text(size=(10, 1)), sg.Checkbox('Renomear', key='-renomear-', enable_events=True), sg.InputText(size=(27, 1), disabled=True, key='-novonome-', background_color='black', disabled_readonly_background_color='grey')],
    [sg.Text(size=(10, 1)), sg.Checkbox('Salvar Em', key='-novodir-', enable_events=True), sg.Input(size=(27, 1), tooltip='Diretório do arquivo', disabled=True, key='-direct-', disabled_readonly_background_color='grey', background_color='black'), sg.FolderBrowse('Procurar', size=(10, 1), disabled=True, key='-browse2-')],
    [sg.T(size=(26, 1), key='-ajuste-'), sg.Text(size=(61, 1), key='-mensagem-', text_color='red', visible=False)],
    [sg.Text(size=(24, 1)), sg.Button('Salvar', size=(10, 1))]
]

window = sg.Window('Conversor', layout, size=(520, 230), element_justification='l')

while True:
    button, values = window.read()  #Lê os botões clicados e paramêtros informados.

    valido = bool

    if button in (sg.WIN_CLOSED, '_EXIT_', 'Close'):  #Evita erros ao fechar programa
        quit()

    if values['-renomear-']:  #Ativa campo renomear
        window['-novonome-'].update(disabled=False)

    elif not values['-renomear-']:  #Desativa campo renomear
        window['-novonome-'].update(disabled=True)

    if values['-novodir-']:  #Ativa campo diretório
        window['-direct-'].update(disabled=False)
        window['-browse2-'].update(disabled=False)

    elif not values['-novodir-']:  #Desativa campo diretório
        window['-direct-'].update(disabled=True)
        window['-browse2-'].update(disabled=True)

    if button == 'Salvar':  #Começa a cadeia de validação
        if values['-renomear-']:  #Caso o botão "renomear" ativado

            if window['-novonome-'].get() in '':  #Caso o usuário tenha marcado a opção renomear e não informou o nome
                nome = '/' + window['-arquivo-'].get().split('/')[-1]
                valido = True

            elif window['-novonome-'].get() in '\/|?<>*:“':  #Caso o usuarío preencha com caractéres inválidos
                valido = False
                window['-ajuste-'].set_size((8, 1))
                window['-mensagem-'].update(visible=True)
                window['-mensagem-'].update(text_color='red')
                window['-mensagem-'].update('O nome do seu arquivo possui algum caractér especial inválido')

            elif len(window['-novonome-'].get()) > 260:  #Caso o nome seja muito grande
                valido = False
                window['-mensagem-'].update(text_color='red')
                window['-mensagem-'].update(visible=True)
                window['-mensagem-'].update('O nome de seu arquivo possui mais de 260 caracteres')
            else:
                nome = '/' + window['-novonome-'].get()  #Caso o campo esteja preenchido corretamente
                valido = True
        else:
            nome = '/' + window['-arquivo-'].get().split('/')[-1]  #Caso o usuário não queira renomear
            valido = True

        if values['-novodir-']:
            if path.exists(window['-direct-'].get()):  #Verifica se o diretório existe
                local = window['-direct-'].get() + nome

            else:
                valido = False
                window['-ajuste-'].set_size((18, 1))
                window['-mensagem-'].update(visible=True)
                window['-mensagem-'].update(text_color='red')
                window['-mensagem-'].update('O diretório selecionado é inválido')
        else:  #Caso não queira informar diretório alternativo
            local = path.join(path.join(environ['USERPROFILE']), 'Desktop').replace('\\', '/') + nome

        if valido:
            try:  #Captura somente o audio do arquivo
                videoclip = VideoFileClip(window['-arquivo-'].get())
                audiosrc = videoclip.audio
                audiosrc.write_audiofile(local + '.mp3')

            except:  #Caso haja algum erro durante a conversão
                window['-ajuste-'].set_size((16, 1))
                window['-mensagem-'].update(text_color='red')
                window['-mensagem-'].update('Algo deu errado durante a conversão')
                window['-mensagem-'].update(visible=True)

            else:  #Mensagem de finalização
                window['-ajuste-'].set_size((26, 1))
                window['-mensagem-'].update('Concluído')
                window['-mensagem-'].update(text_color='green')
                window['-mensagem-'].update(visible=True)
        else:
            pass
quit()
