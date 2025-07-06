import streamlit as st import plotly.graph_objects as go

st.set_page_config(page_title="積込シミュレーター（複数荷物対応）") st.title("📦 荷物積込シミュレーター（3D + 複数種類対応）")

st.markdown("最大10種類までの荷物を登録できます。体積の大きい順に下から積みます。")

truck_length = st.number_input("トラック奥行 (mm)", value=9400) truck_width = st.number_input("トラック幅 (mm)", value=2350) truck_height = st.number_input("トラック高さ (mm)", value=2000)

セッションで荷物管理

if "boxes" not in st.session_state: st.session_state.boxes = []

st.subheader("📦 荷物の追加") with st.form("box_form"): col1, col2, col3 = st.columns(3) with col1: length = st.number_input("長さ", key="len", value=5024) width = st.number_input("幅", key="wid", value=460) with col2: height = st.number_input("高さ", key="hei", value=355) count = st.number_input("個数", key="cnt", min_value=1, value=3, step=1) with col3: color = st.color_picker("色", key="col", value="#87CEEB")

submitted = st.form_submit_button("＋ この荷物を追加")
if submitted and len(st.session_state.boxes) < 10:
    volume = length * width * height
    st.session_state.boxes.append({
        "length": length,
        "width": width,
        "height": height,
        "count": count,
        "volume": volume,
        "color": color
    })

荷物リスト表示

if st.session_state.boxes: st.markdown("### 現在の荷物リスト") for i, box in enumerate(st.session_state.boxes): st.write(f"荷物{i+1}: {box['length']}×{box['width']}×{box['height']}mm, {box['count']}個, 色: {box['color']}")

if st.button("🚀 シミュレーション開始"):
    fig = go.Figure()
    max_height_at_pos = {}  # 配置位置ごとの高さ記録

    # 体積順に並べる
    sorted_boxes = sorted(st.session_state.boxes, key=lambda x: x["volume"], reverse=True)

    for box in sorted_boxes:
        for i in range(int(box["count"])):
            placed = False
            for x in range(0, int(truck_width), int(box["width"])):
                for y in range(0, int(truck_length), int(box["length"])):
                    key = (x, y)
                    z = max_height_at_pos.get(key, 0)
                    if z + box["height"] <= truck_height:
                        fig.add_trace(go.Mesh3d(
                            x=[x, x+box["width"], x+box["width"], x, x, x+box["width"], x+box["width"], x],
                            y=[y, y, y+box["length"], y+box["length"], y, y, y+box["length"], y+box["length"]],
                            z=[z, z, z, z, z+box["height"], z+box["height"], z+box["height"], z+box["height"]],
                            color=box["color"],
                            opacity=0.7,
                            alphahull=0
                        ))
                        max_height_at_pos[key] = z + box["height"]
                        placed = True
                        break
                if placed:
                    break

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="幅", range=[0, truck_width]),
            yaxis=dict(title="奥行", range=[0, truck_length]),
            zaxis=dict(title="高さ", range=[0, truck_height])
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700
    )

    st.success("✨ シミュレーション完了！")
    st.plotly_chart(fig, use_container_width=True)

else: st.info("まずは少なくとも1種類の荷物を追加してください。")

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

    st.plotly_chart(fig, use_container_width=True)import streamlit as st import plotly.graph_objects as go

st.set_page_config(page_title="積込シミュレーター（複数荷物対応）") st.title("📦 荷物積込シミュレーター（3D + 複数種類対応）")

st.markdown("最大10種類までの荷物を登録できます。体積の大きい順に下から積みます。")

truck_length = st.number_input("トラック奥行 (mm)", value=9400) truck_width = st.number_input("トラック幅 (mm)", value=2350) truck_height = st.number_input("トラック高さ (mm)", value=2000)

num_boxes = st.slider("荷物の種類数", 1, 10, 2)

box_list = [] colors = ["skyblue", "salmon", "lightgreen", "orange", "violet", "gold", "deepskyblue", "pink", "gray", "lightcoral"]

st.subheader("📦 荷物情報入力") for i in range(num_boxes): with st.expander(f"荷物 {i+1}"): length = st.number_input(f"荷物 {i+1} 長さ", key=f"len_{i}", value=5024) width = st.number_input(f"荷物 {i+1} 幅", key=f"wid_{i}", value=460) height = st.number_input(f"荷物 {i+1} 高さ", key=f"hei_{i}", value=355) count = st.number_input(f"荷物 {i+1} 個数", key=f"cnt_{i}", value=3, step=1)

volume = length * width * height
    box_list.append({
        "length": length,
        "width": width,
        "height": height,
        "count": count,
        "volume": volume,
        "color": colors[i % len(colors)]
    })

if st.button("🚀 シミュレーション開始"): # 体積の大きい順にソート box_list.sort(key=lambda x: x["volume"], reverse=True)

fig = go.Figure()
x_cursor = 0
y_cursor = 0
z_cursor = 0
max_height_at_pos = {}  # (x,y)位置ごとの高さ記録

for box in box_list:
    for i in range(int(box["count"])):
        placed = False
        for x in range(0, int(truck_width), int(box["width"])):
            for y in range(0, int(truck_length), int(box["length"])):
                key = (x, y)
                z = max_height_at_pos.get(key, 0)
                if z + box["height"] <= truck_height:
                    fig.add_trace(go.Mesh3d(
                        x=[x, x+box["width"], x+box["width"], x, x, x+box["width"], x+box["width"], x],
                        y=[y, y, y+box["length"], y+box["length"], y, y, y+box["length"], y+box["length"]],
                        z=[z, z, z, z, z+box["height"], z+box["height"], z+box["height"], z+box["height"]],
                        color=box["color"],
                        opacity=0.6
                    ))
                    max_height_at_pos[key] = z + box["height"]
                    placed = True
                    break
            if placed:
                break

fig.update_layout(
    scene=dict(
        xaxis=dict(title="幅", range=[0, truck_width]),
        yaxis=dict(title="奥行", range=[0, truck_length]),
        zaxis=dict(title="高さ", range=[0, truck_height])
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=700
)

st.success("✨ シミュレーション完了！")
st.plotly_chart(fig, use_container_width=True)

