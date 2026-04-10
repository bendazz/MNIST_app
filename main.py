import random

import torch
from torch import nn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from torchvision import datasets, transforms

CIFAR_LABELS = [
    "Airplane", "Automobile", "Bird", "Cat", "Deer",
    "Dog", "Frog", "Horse", "Ship", "Truck",
]

transform = transforms.ToTensor()
train_dataset = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
test_dataset = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)

model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(3072, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10),
)
model.load_state_dict(torch.load("CIFAR.pth", map_location="cpu"))
model.eval()

app = FastAPI()

@app.get("/image")
def image_get():
    index = random.randint(0, len(test_dataset) - 1)
    image, label = test_dataset[index]
    pixels = image.tolist()  # shape: [3, 32, 32]
    return {"index": index, "label": CIFAR_LABELS[label], "image": pixels}

@app.get("/predict")
def predict(index: int):
    image, label = test_dataset[index]
    with torch.no_grad():
        logits = model(image.unsqueeze(0))
        prediction = int(logits.argmax(dim=1).item())
    return {"label": CIFAR_LABELS[label], "prediction": CIFAR_LABELS[prediction]}


app.mount("/", StaticFiles(directory="static", html=True), name="static")