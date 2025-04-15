import os
import torch
import torchvision
import torchvision.transforms as transforms
from torch import nn, optim
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision.models import resnet18

# === Config ===
DATA_DIR = "../data/asl_alphabet_train"
BATCH_SIZE = 32
EPOCHS = 1
MODEL_PATH = "../models/asl_cnn_model.pt"
NUM_CLASSES = 29  # A-Z + space + delete + nothing

# === Transforms ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# === Dataset ===
dataset = ImageFolder(DATA_DIR, transform=transform)

# TEST MODE: only train on 2000 images for now
dataset = torch.utils.data.Subset(dataset, range(2000))
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# === Model ===
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# === Training Loop ===
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        print(f"🟢 Training batch of size {images.shape}")

    print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {total_loss:.4f}")

# === Save Model ===
os.makedirs("../models", exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
