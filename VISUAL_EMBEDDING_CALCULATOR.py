from  Default_interfaces import Default_node_interface
import torch
import torch.nn as nn
import timm
from torch.nn.functional import cosine_similarity
import csv

class VISUAL_EMBEDDING_CALCULATOR(nn.Module):
    def __init__(self, params=None):
        super().__init__()

        self.first = None
        self.ctr = 0

        self.csv_path = params[0]
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])

        self.vit = timm.create_model(
            'vit_tiny_patch16_224',
            pretrained=True,
            num_classes=0,  # отключаем head → возвращается [CLS] токен (768-D)
            img_size=224
        )

        self.resize = torch.nn.AdaptiveAvgPool2d((224, 224))

    def forward(self, x):

        x = self.resize(x)  # адаптивно масштабируем без искажений
        emb = self.vit(x)  # (B, D), D = 192 (для tiny)
        emb = torch.nn.functional.normalize(emb, p=2, dim=1)
        return emb

    def __call__(self, Simulation_loop_handler):
        if not Simulation_loop_handler.loop_memory_dict.get('Unprocessed_cords_from_TR'):
            return None

        x = Simulation_loop_handler.loop_memory_dict.get('last_gotten_image')
        if x is None:
            return None
        if x.ndim == 2:
            x = x[:, :, None]

        x = torch.from_numpy(x.transpose(2, 0, 1)).float().unsqueeze(0)

        if x.max() > 1.0:
            x = x / 255.0

        emb = self.forward(x)

        self.ctr += 1
        if self.ctr == 3:
            self.first = emb.detach().clone()
        elif self.ctr < 3:
            return None

        if self.first is not None:
            sim = cosine_similarity(emb, self.first, dim=1).item()
            print(f"Loop Similarity: {sim:.4f}")

        Simulation_loop_handler.loop_memory_dict['last_frame_embedding'] = emb.detach().clone()

        with open(self.csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            pos = list(emb.detach().clone().numpy())
            pos.insert(0, round(Simulation_loop_handler.sim.getSimulationTime(), 2))
            writer.writerows([pos])
            Simulation_loop_handler.loop_memory_dict['Unprocessed_cords_from_TR'] = False