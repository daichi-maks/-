import streamlit as st
import plotly.graph_objects as go

st.title("🛻 荷物積込シミュレーター")

# 入力フォーム
with st.form("input_form"):
    st.subheader("📦 トラックと荷物の情報を入力してください")

    truck_length = st.number_input("トラック奥行 (mm)", value=9400)
    truck_width = st.number_input("トラック幅 (mm)", value=2350)
    truck_height = st.number_input("トラック高さ (mm)", value=2000)

    box_length = st.number_input("荷物の奥行", value=5024)
    box_width = st.number_input("荷物の幅", value=460)
    box_height = st.number_input("荷物の高さ", value=355)
    box_count = st.number_input("荷物の個数", value=9, step=1)

    submitted = st.form_submit_button("シミュレーション開始")

# 積込シミュレーション表示
if submitted:
    st.success("シミュレーション結果：")

    fig = go.Figure()
    positions = []

    # 簡単に2段に分けて配置するロジック
    per_row = truck_width // box_width
    for i in range(int(box_count)):
        layer = i // int(per_row)
        col = i % int(per_row)
        x = col * box_width
        y = 0
        z = layer * box_height
        positions.append((x, y, z))

    for x, y, z in positions:
        fig.add_trace(go.Mesh3d(
            x=[x, x+box_width, x+box_width, x, x, x+box_width, x+box_width, x],
            y=[y, y, y+box_length, y+box_length, y, y, y+box_length, y+box_length],
            z=[z, z, z, z, z+box_height, z+box_height, z+box_height, z+box_height],
            color='skyblue',
            opacity=0.6,
            showscale=False
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, truck_width]),
            yaxis=dict(range=[0, truck_length]),
            zaxis=dict(range=[0, truck_height]),
        ),
        margin=dict(r=10, l=10, b=10, t=10)
    )

    st.plotly_chart(fig)