import streamlit as st

# Función para convertir cuota americana a decimal
def american_a_decimal(cuota_americana):
    if cuota_americana > 0:
        return (cuota_americana / 100) + 1
    else:
        return (100 / abs(cuota_americana)) + 1

st.set_page_config(page_title="Estrategia: Mayor probabilidad", layout="centered")

st.title("🎯 Estrategia de Apuesta por Probabilidad Alta Evelin")
st.markdown("Introduce las cuotas *americanas* de los 3 posibles resultados:")

# Entradas
cuota_a_usa = st.number_input("Cuota americana: Gana A", value=+120)
cuota_empate_usa = st.number_input("Cuota americana: Empate", value=+250)
cuota_b_usa = st.number_input("Cuota americana: Gana B", value=+180)
capital = st.number_input("💵 Monto total a apostar (MXN)", min_value=1.0, value=100.0)
recuperacion_pct = st.slider("Porcentaje de recuperación en las apuestas secundarias (%)", 0, 100, 70)

# Convertir cuotas
cuotas = {
    "A": american_a_decimal(cuota_a_usa),
    "Empate": american_a_decimal(cuota_empate_usa),
    "B": american_a_decimal(cuota_b_usa)
}

if st.button("Calcular estrategia"):
    # Buscar el resultado con mayor probabilidad (cuota más baja)
    resultado_probable = min(cuotas, key=cuotas.get)
    cuota_principal = cuotas[resultado_probable]

    # Calcular cuánto necesitamos apostar a los otros 2 resultados para recuperar un porcentaje
    recuperar = capital * (recuperacion_pct / 100)
    apuestas = {}
    for resultado, cuota in cuotas.items():
        if resultado == resultado_probable:
            continue
        apuestas[resultado] = recuperar / cuota

    # Asignar el resto a la apuesta principal
    restante = capital - sum(apuestas.values())
    apuestas[resultado_probable] = restante

    # Calcular ganancias posibles
    ganancias = {}
    for resultado in cuotas:
        ganancia = apuestas[resultado] * cuotas[resultado]
        ganancias[resultado] = ganancia

    # Mostrar resultados
    st.markdown("### 💰 Distribución sugerida de apuestas:")
    for resultado in cuotas:
        st.write(f"Apuesta a {resultado}: **${apuestas[resultado]:.2f}** (cuota: {cuotas[resultado]:.2f})")

    st.markdown("### 📈 Posibles ganancias:")
    for resultado in cuotas:
        ganancia_neta = ganancias[resultado] - capital
        st.write(f"Si gana {resultado}: **${ganancias[resultado]:.2f}** (neta: **${ganancia_neta:.2f}**)")

    st.markdown(f"🔍 Apuesta principal: **{resultado_probable}** (cuota más baja, más probable)")
