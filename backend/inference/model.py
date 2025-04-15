import torch
from torchvision import transforms
from torchvision.models import resnet18
from PIL import Image
from .hand_detector import detect_and_crop_hand  # if used

CLASS_LABELS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'del', 'nothing', 'space'
]

def load_model():
    model = resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_LABELS))
    model.load_state_dict(torch.load("models/asl_cnn_model.pt", map_location="cpu"))
    model.eval()
    print("✅ Model loaded successfully!")
    return model

def predict(model, image: Image.Image, confidence_threshold=0.7):
    image = detect_and_crop_hand(image)
    if image is None:
        print("🛑 No hand detected.")
        return None

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.softmax(output, dim=1)
        top1_prob, top1_idx = torch.max(probabilities, 1)

        predicted_label = CLASS_LABELS[top1_idx.item()]
        confidence = top1_prob.item()

        if predicted_label == "nothing" or confidence < confidence_threshold:
            print(f"🙈 Skipped: {predicted_label} ({confidence:.2%})")
            return None

        return {
            "prediction": predicted_label,
            "confidence": round(confidence * 100, 2)
        }
