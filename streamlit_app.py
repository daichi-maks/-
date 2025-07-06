import streamlit as st
import plotly.graph_objects as go

st.title("📦 荷物積込シミュレーター（3D表示）")

# 入力フォーム
with st.form("input_form"):
    st.subheader("🚚 トラックと荷物の情報を入力してください")

    truck_length = st.number_input("トラック奥行 (mm)", value=9400)
    truck_width = st.number_input("トラック幅 (mm)", value=2350)
    truck_height = st.number_input("トラック高さ (mm)", value=2000)

    box_length = st.number_input("荷物の奥行", value=5024)
    box_width = st.number_input("荷物の幅", value=460)
    box_height = st.number_input("荷物の高さ", value=355)
    box_count = st.number_input("荷物の個数", value=9, step=1)

    submitted = st.form_submit_button("シミュレーション開始")

if submitted:
    st.success("3Dシミュレーション結果")

    fig = go.Figure()
    boxes_per_layer = truck_width // box_width
    layers = []

    for i in range(int(box_count)):
        layer = i // int(boxes_per_layer)
        col = i % int(boxes_per_layer)
        x = col * box_width
        y = 0
        z = layer * box_height
        layers.append((x, y, z))

    def make_box(x, y, z, w, d, h):
        return go.Mesh3d(
            x=[x, x+w, x+w, x, x, x+w, x+w, x],
            y=[y, y, y+d, y+d, y, y, y+d, y+d],
            z=[z, z, z, z, z+h, z+h, z+h, z+h],
            color='skyblue',
            opacity=0.6
        )

    for (x, y, z) in layers:
        fig.add_trace(make_box(x, y, z, box_width, box_length, box_height))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='幅', range=[0, truck_width]),
            yaxis=dict(title='奥行', range=[0, truck_length]),
            zaxis=dict(title='高さ', range=[0, truck_height]),
        ),
        margin=dict(l=10, r=10, b=10, t=10),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)