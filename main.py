import random

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from torchvision import datasets, transforms

transform = transforms.ToTensor()
train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)

app = FastAPI()

@app.get("/image")
def image_get():
    index = random.randint(0, len(train_dataset) - 1)
    image, label = train_dataset[index]
    pixels = image.squeeze().tolist()
    return {"label": label, "image": pixels}


app.mount("/", StaticFiles(directory="static", html=True), name="static")