import gradio as gr
import numpy as np

def greet1(name):
    return f'Hello {name}!'

def greet2(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

# Interface 类可以用用户接口包装任意的Python函数, 核心三参数：
# - fn      : 被 UI 包装的函数
# - inputs  : 输入组件 (如："text", "image" or "audio")
# - outputs : 输出组件 (如："text", "image" or "label")
demo1 = gr.Interface(
    fn=greet1,
    inputs=gr.Textbox(lines=1, placeholder="Name Here..."),
    outputs="text",
)
demo2 = gr.Interface(
    fn=greet2,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
)
# 图像示例
demo3 = gr.Interface(sepia, gr.Image(), "image")

with gr.Blocks() as demo4:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet1, inputs=name, outputs=output)

def flip_text(x):
    return x[::-1]

def flip_image(x):
    return np.fliplr(x)

with gr.Blocks() as demo5:
    gr.Markdown("Flip text or image files using this demo.")
    with gr.Tabs():
        with gr.TabItem("Flip Text"):
            text_input = gr.Textbox()
            text_output = gr.Textbox()
            text_button = gr.Button("Flip")
        with gr.TabItem("Flip Image"):
            with gr.Row():
                image_input = gr.Image()
                image_output = gr.Image()
            image_button = gr.Button("Flip")

    text_button.click(flip_text, inputs=text_input, outputs=text_output)
    image_button.click(flip_image, inputs=image_input, outputs=image_output)

demo5.launch()