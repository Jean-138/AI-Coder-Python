import os
##modulo para interagir com o sistemma operacional / nao e neccessario
import streamlit as st #interface web
from groq import Groq #importa a classe groq para se conectar a api da plataforma groq e acessar llm


st.set_page_config(
    page_title="AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o " AI Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é auxiliar iniciantes.

REGRAS DE OPERAÇÃO:
1. **Foco em Programação**: Responda apenas a perguntas relacionadas à programação, algoritmos, estruturas de dados e Python.
2. **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
   **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
   **Exemplo de Código**: Forneça um exemplo de código em Python com a sintaxe correta. O código deve ser funcional.
   **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando linha por linha.
   **Documentação de Referência**: Inclua uma seção chamada "📘 Documentação de Referência" com um link oficial ou fonte confiável.
3. **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser técnicas, mas acessíveis.
"""

# barra lateral no Streamlit
with st.sidebar:
    # Define o título da barra lateral
    st.title("🤖 AI Coder")

    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em programação na linguagem Python para ajudar programadores iniciantes.")

    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )


    st.markdown("---")
    
    # Como usar
    st.markdown("## Como Usar")
    st.markdown("""
1. 🔑 Insira sua **API Key Groq** acima.  
2. 💬 Faça perguntas sobre Python na caixa de chat principal.  
3. ⏳ Aguarde a AI Coder analisar e gerar a resposta com explicação detalhada e exemplos de código.  
4. ✅ AI Coder pode cometer erros, sempre revise e teste os códigos fornecidos.
    """)




    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas de programação com Linguagem Python. IA pode cometer erros. verifique as respostas.")
    st.markdown("---")
    st.markdown("💡 Dica: Pergunte qualquer coisa sobre Python, e eu explico passo a passo.")
    st.markdown("📚 Aprenda conceitos de programação e veja exemplos de código funcionais.")

    st.markdown("---")
    st.markdown("[🌐 Visite meu GitHub](https://github.com/Jean-138)")



#titulo principal do app
st.title("AI CODER - PYTHON")
#subtitulo adcional
st.title("assistente de programação com Linguagem Python  ")

st.caption("Faça a sua pergunta sobre Python")

# inicializa o historico de mensagens caso ainda nao tenha
if "messages" not in st.session_state:
    st.session_state.messages = []

# exibe todas as mensagens anteriores guardadas no session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# inicializa a variavel do client groq como none
client = None

# verifica se o usuario forneceu a chave api
if groq_api_key:
    
    try:

        #cria o client com a chave api fornecida
        client = Groq(api_key = groq_api_key)

    except Exception as e:
    # exibe erro caso haja problema ao inicializar o cliente groq
        st.sidebar.error(f"erro ao inicializar o cliente: {e}")
        st.stop()

#se nao iver a chave mas ja existam messagens, mostra o aviso
elif st.session_state.messages:
    st.warning("Por favor, insira a sua API gloq para continuar.")
    st.stop()

#captura a entrada do usuario no chat
if prompt := st.chat_input("Qual a sua duvida sobre Python ? "):

    #se nao houver cliente valido
    if not client:
        st.warning("Por favor, insira a sua APi gloq.")
        st.stop()

#armazena a msg do usuario no estado da sessao  
    st.session_state.messages.append({"role": "user","content": prompt})

    #exibe a msg do usuario no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    #prepara a msg para enviar a api, incluindo o prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:

        messages_for_api.append(msg)

    #cria a resposta no chat
    with st.chat_message("assistant"):

        with st.spinner("Analisando pergunta..."):
            
            try:

                #chama a api
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b",
                    temperature = 0.7,
                    max_tokens = 2048,
                )


                    # extrai a resposta gerada pela api
                coder_ai_resposta = chat_completion.choices[0].message.content
                #exibe a respostta no streamlit
                st.markdown(coder_ai_resposta)

                #armazena a resposta no estado da sessao
                st.session_state.messages.append({"role": "assistant", "content": coder_ai_resposta})

            #caso ocora erro de comunicacao da api, exibe o erro
            except Exception as e:
                st.error(f"ocorreu um erro ao se comunicar com a API")


