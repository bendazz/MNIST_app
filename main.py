from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from torchvision import datasets, transforms

# Download MNIST dataset to ./data and load test set into memory
transform = transforms.ToTensor()
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")