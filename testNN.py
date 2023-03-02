test_path = r"C:\Users\David\Desktop\Pramakon\test"
train_path = r"C:\Users\David\Desktop\Pramakon\train"
import torch
import torchvision.models as models
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms

# Load the pre-trained ResNet50 model
model = models.resnet50(pretrained=True)

# Modify the final layer to output only two classes
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)

# Define the loss function (e.g., cross-entropy)
criterion = torch.nn.CrossEntropyLoss()

# Define the optimizer (e.g., stochastic gradient descent)
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# Define the transforms for the dataset
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Load the dataset
train_dataset = datasets.ImageFolder(train_path, transform=transform)

# Create a data loader for the training data
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# Train the model for several epochs
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Accumulate the loss
        running_loss += loss.item()

    # Print statistics after every epoch
    print('Epoch %d loss: %.3f' % (epoch+1, running_loss/len(train_loader)))
    running_loss = 0.0


# Save the model to a file
torch.save(model.state_dict(), 'fine_tuned_resnet50.pth')
