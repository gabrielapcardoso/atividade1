import streamlit as st
import pandas as pd

COLUNAS = ["Nome", "Idade", "Convenio", "Prioridade", "Motivo"]

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=COLUNAS)

st.title("Cadastro de Pacientes — Consultório Médico")

with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do Paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "SUS"]
    )
    prioridade = st.slider(
        "Prioridade do Atendimento (1 = baixa, 5 = urgente)",
        min_value=1, max_value=5, value=3
    )
    motivo = st.text_area("Motivo da Consulta / Observações")

    enviado = st.form_submit_button("Cadastrar")

if enviado:
    if not nome:
        st.error("Erro: o nome do paciente é obrigatório.")
    else:
        novo_registro = pd.DataFrame(
            [[nome, idade, convenio, prioridade, motivo]],
            columns=COLUNAS
        )
        st.session_state.dados = pd.concat(
            [st.session_state.dados, novo_registro],
            ignore_index=True
        )
        st.success(f"Paciente '{nome}' cadastrado com sucesso.")

st.subheader("Pacientes Cadastrados")
st.dataframe(st.session_state.dados.iloc[::-1], use_container_width=True)

if not st.session_state.dados.empty:
    csv_bytes = st.session_state.dados.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar CSV",
        data=csv_bytes,
        file_name="pacientes.csv",
        mime="text/csv"
    )
