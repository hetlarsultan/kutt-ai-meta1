#!/bin/bash
echo "Downloading SadTalker models..."
mkdir -p checkpoints
wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O checkpoints/mapping_00109-model.pth.tar
wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O checkpoints/SadTalker_V0.0.2_256.safetensors
echo "Downloading GFPGAN..."
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O gfpgan/weights/GFPGANv1.4.pth
echo "Done!"
