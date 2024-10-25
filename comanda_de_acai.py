import streamlit as st

# Preços dos tamanhos e adicionais
PRECOS_TAMANHO = {
    '200ml - R$ 4,00': 4.00,
    '300ml - R$ 6,00': 6.00,
    '400ml - R$ 7,00': 7.00,
    '500ml - R$ 8,00': 8.00
}
PRECO_ADICIONAL_ACOMP2 = 0.50

# Inicializa o estado da sessão se necessário
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []
if 'subtotal' not in st.session_state:
    st.session_state.subtotal = 0.0

# Função para calcular o subtotal
def calcular_subtotal(tamanho, acomp2):
    subtotal = PRECOS_TAMANHO.get(tamanho, 0.0)
    for quantidade in acomp2.values():
        subtotal += quantidade * PRECO_ADICIONAL_ACOMP2  # Corrigido: cada unidade custa R$ 0,50
    return subtotal

# Função para adicionar pedido ao carrinho
def adicionar_no_carrinho(tamanho, cobertura, acomp1, acomp2):
    pedido_atual = f"""
    Tamanho: {tamanho} 
    Cobertura: {cobertura}, 
     {'; '.join(acomp1) if acomp1 else "Nenhum"},
     {', '.join([f"{k}: {v}" for k, v in acomp2.items()]) if acomp2 else "Nenhum"}
    """
    st.session_state.carrinho.append(pedido_atual)
    st.session_state.subtotal += calcular_subtotal(tamanho, acomp2)

# Layout principal
st.title("Montagem de Pedido")

# Seleção de tamanho e cobertura
tamanho = st.selectbox("Selecione o TAMANHO:", ['Nenhum'] + list(PRECOS_TAMANHO.keys()))
cobertura = st.selectbox("Selecione a COBERTURA:", 
                         ['Sem Cobertura', 'Chocolate', 'Morango', 'Leite Cond.', 'Menta', 
                          'Uva', 'Mel', 'Doce de Leite', 'Café'])

# Acompanhamentos 1
st.markdown("### ACOMPANHAMENTOS 1")
acomp1_opcoes = [
    'Leite em pó', 'Aveia', 'Granola', 'Paçoca', 'Amendoim',
    'Flocos de Arroz', 'Confete', 'Granulado', 'Chocoball',
    'Jujuba', 'Maxmallow', 'Sucrilhos', 'Gotas de Chocolate', 'Canudinho'
]
acomp1 = [op for op in acomp1_opcoes if st.checkbox(op)]

# Acompanhamentos 2
st.markdown("### ACOMPANHAMENTOS 2")
acomp2 = {}
for opcao in ['Creme ninho', 'Creme nutella', 'Mousse de Morango', 'Mousse de Maracujá']:
    quantidade = st.number_input(f"{opcao}", min_value=0, max_value=5, value=0, step=1)
    if quantidade > 0:
        acomp2[opcao] = quantidade

# Botões para adicionar ao carrinho e continuar pedindo
col1, col2 = st.columns(2)
with col1:
    if st.button("Adicionar no Carrinho"):
        adicionar_no_carrinho(tamanho, cobertura, acomp1, acomp2)

with col2:
    if st.button("Continuar Pedindo"):
        st.success("Você pode continuar pedindo!")
        # Atualiza a visualização dos itens no carrinho sem reiniciar o script
        st.write("Carrinho atual:")
        for i, pedido in enumerate(st.session_state.carrinho, start=1):
            st.write(f"#{i} {pedido}")

# Exibir subtotal atualizado
st.metric("Subtotal", f"R$ {st.session_state.subtotal:.2f}")

# Exibir pedidos no carrinho e permitir envio
if st.button(f"Enviar Pedido ({len(st.session_state.carrinho)} itens)"):

    st.write("### Resumo do Pedido")
    for i, pedido in enumerate(st.session_state.carrinho, start=1):
        st.write(f"#### Pedido #{i}")
        st.write(pedido)

    confirmar = st.button("Confirmar Pedido")
    cancelar = st.button("Cancelar")

    if confirmar:
        st.success("Pedido confirmado!")
        st.session_state.carrinho = []
        st.session_state.subtotal = 0.0
        # Não é necessário reiniciar; o estado é limpo
    elif cancelar:
        st.warning("Pedido cancelado.")


