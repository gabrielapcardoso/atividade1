import gradio as gr
import pandas as pd
import os

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["Nome", "Idade", "Convenio", "Prioridade", "Motivo"]


def carregar_dados():
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome:
        return (
            "Erro: o nome do paciente é obrigatório.",
            carregar_dados(),
            nome, idade, convenio, prioridade, motivo  # mantém o que foi digitado
        )

    dados = carregar_dados()

    novo_registro = pd.DataFrame(
        [[nome, idade, convenio, prioridade, motivo]],
        columns=COLUNAS
    )

    dados = pd.concat([dados, novo_registro], ignore_index=True)
    dados.to_csv(ARQUIVO_CSV, index=False)

    mensagem = f"Paciente '{nome}' cadastrado com sucesso."
    ultimos_cadastros = dados.tail(10).iloc[::-1]

    # Retorna valores "zerados" para limpar os campos do formulário
    return (
        mensagem,
        ultimos_cadastros,
        "",      # limpa nome
        0,       # limpa idade
        None,    # limpa convênio (Dropdown volta ao estado vazio)
        3,       # reseta prioridade para o valor padrão (3)
        ""       # limpa motivo
    )


with gr.Blocks() as app:
    gr.Markdown("## Cadastro de Pacientes — Consultório Médico")

    with gr.Column():
        nome_input = gr.Textbox(label="Nome do Paciente")
        idade_input = gr.Number(label="Idade")
        convenio_input = gr.Dropdown(
            choices=["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "SUS"],
            label="Convênio"
        )
        prioridade_input = gr.Slider(
            minimum=1, maximum=5, step=1, value=3,
            label="Prioridade do Atendimento (1 = baixa, 5 = urgente)"
        )
        motivo_input = gr.Textbox(
            label="Motivo da Consulta / Observações", lines=3
        )

        botao_cadastrar = gr.Button("Cadastrar")

        resultado_output = gr.Textbox(label="Status", interactive=False)
        tabela_saida = gr.Dataframe(
            headers=COLUNAS,
            label="Últimos Cadastros"
        )

    botao_cadastrar.click(
    fn=cadastrar_paciente,
    inputs=[nome_input, idade_input, convenio_input, prioridade_input, motivo_input],
    outputs=[
        resultado_output,
        tabela_saida,
        nome_input,
        idade_input,
        convenio_input,
        prioridade_input,
        motivo_input
    ]
    )

    app.load(
        fn=lambda: ("", carregar_dados().tail(10).iloc[::-1]),
        outputs=[resultado_output, tabela_saida]
    )

app.launch()
