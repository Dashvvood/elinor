import pytest
import os

def test_summary_unet2d(tmp_path, monkeypatch):
    torch = pytest.importorskip("torch")
    pytest.importorskip("diffusers")
    from diffusers import UNet2DModel

    from elinor.ai.model_summary import summary
    from elinor import o_d
    monkeypatch.chdir(tmp_path)

    model = UNet2DModel()
    model_input = {
        "sample": torch.randn(1, 3, 64, 64),
        "timestep": 1,
    }
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", f"summary_{o_d().strftime("%Y%m%d%_H%M%S")}.txt")
    features, parameters, mapping = summary(model, model_input, output_path)
    
    assert features
    assert parameters
    assert mapping is not None
    assert os.path.isfile(output_path)
    assert os.path.getsize(output_path) > 0
    