"""
CN:
这是一个用于总结模型结构和参数的工具。代码非常孱弱， 是当初为了了解模型结构和参数而写的。
EN:
This is a tool for summarizing model structures and parameters. 
The code is very weak, and was written at the time to understand 
the model structure and parameters.
"""
from collections import defaultdict, OrderedDict, namedtuple
import io
import os
import uuid
import torch

def get_input_output_per_layer(model, model_input):
    features = OrderedDict()
    handles = OrderedDict()
    HookData = namedtuple("HookData", ["type", "input", "output"])
    
    def hook(name):
        def hook_fn(module, input, output):
            features[name] = HookData(type(module), input, output)
        return hook_fn
    
    for name, module in model.named_modules():
        handles[name] = module.register_forward_hook(hook(name))
    
    with torch.no_grad():
        model(**model_input)
        
    for name, h in handles.items():
        h.remove()
        
    return features

def get_mapping_f2p(features, parameters):
    """
    Get a mapping from feature to parameter.
    """
    def get_main_key(key):
        return key.rsplit(".", 1)[0]  # 删除最后一个 '.'后的部分（即 .weight, .bias）

    # 建立映射关系
    mapping = defaultdict(list)
    for p_key in parameters.keys():
        main_key = get_main_key(p_key)
        for f_key in features.keys():
            if f_key.startswith(main_key):
                mapping[f_key].append(p_key)
        
    return mapping

def summary(model, model_input, output_path=None):
    from .. import o_d

    if output_path is None:
        output_path = "model_summary"

    if os.path.isdir(output_path) or output_path.endswith((os.sep, "/")):
        os.makedirs(output_path, exist_ok=True)
        output_path = os.path.join(
            output_path.rstrip(os.sep),
            f"summary_{o_d().strftime('%Y%m%d%H%M%S')}.txt",
        )
    else:
        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    buf = io.StringIO()

    features = get_input_output_per_layer(model, model_input)
    parameters = {}
    for k, v in model.named_parameters():
        parameters[k] = v
    mapping = get_mapping_f2p(features, parameters)

    header = [
        "Model: " + type(model).__name__,
        "Input: " + str(model_input.keys()),
    ]
    sections = []
    for f_key, io_data in features.items():
        input_shape = [*io_data.input[0].shape] \
            if len(io_data.input) > 0 else None

        output_shape = [*io_data.output[0].shape] \
            if len(io_data.output) > 0 else None

        module_type = io_data.type.__name__
        section = [
            f"{f_key}: --- {module_type}",
            " " * 4 + f"I/O: {input_shape} --> {output_shape}",
        ]
        for p_key in mapping[f_key]:
            section.append(
                " "*4 
                + f"{p_key}: {[*parameters[p_key].shape]}"
                + " " * 1
                + f"<{str(parameters[p_key].dtype).removeprefix("torch.")}>"
            )
        sections.append(section)

    # all_lines = header + [line for section in sections for line in section]
    all_lines = [line for section in sections for line in section]
    sep_len = max(80, max(map(len, all_lines), default=0))

    buf.write("\n".join(header) + "\n")
    buf.write("=" * sep_len + "\n")
    for section in sections:
        buf.write("\n".join(section) + "\n")
        buf.write("-" * sep_len + "\n")
    buf.write("=" * sep_len + "\n")

    with open(output_path, "w") as fp:
        fp.write(buf.getvalue())

    return features, parameters, mapping
