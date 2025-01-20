import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

BATCH_SIZE = 128
EPOCHS = 10
LEARNING_RATE = 0.001

# for a module, a constructor describing layers and forward specifies data flow are required
class FeedForwardNet(nn.Module): #inherit module
    def __init__(self):
        super().__init__()
        # first layer
        self.flatten = nn.Flatten()
        # dense layers
        self.dense_layers = nn.Sequential( # allows us to pack together multiple layers
            # data will flow sequentially from one layer to the next
            nn.Linear(28*28,256), # first layer (input features, output features) 28x28px
            nn.ReLU(),
            nn.Linear(256, 10) # 10 class outputs
        )
        # softargmax or normalized exponential function,
        # converts a vector of K real numbers into a probability distribution of K possible outcomes.
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_data):
        flattened_data = self.flatten(input_data) # transform a multi-dimensional input_data into a 1D tensor.
        logits = self.dense_layers(flattened_data)
        predictions = self.softmax(logits)
        return predictions

# Download torch_module dataset class
def download_mnist_datasets():
    train_dataset = datasets.MNIST(
        root="data", # Where to store the dataset we are downloading
        download=True, # If dataset is not downloaded yet, do so
        train=True, # We are interested in the trainset part of the dataset
        transform=ToTensor() # allows to apply a T to the dataset
    )

    validation_dataset = datasets.MNIST(
        root="data",  # Where to store the dataset we are downloading
        download=True,  # If dataset is not downloaded yet, do so
        train=False,  # We are interested in the trainset part of the dataset
        transform=ToTensor()  # allows to apply a T to the dataset
    )
    return train_dataset, validation_dataset

def train_one_epoch(model, data_loader, loss_fn, optimiser, device):
    for inputs, targets in data_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # calculate loss
        predictions = model(inputs)
        loss = loss_fn(predictions, targets)

        # back propagate loss, update weights
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()

    print(f"loss : {loss.item()}")

def train(model, data_loader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f"epoch {i+1}")
        train_one_epoch(model, data_loader, loss_fn, optimiser, device)
        print("-------------------------------")
    print("training is done")


if __name__ == "__main__":
    train_data,_ = download_mnist_datasets() # Only download training set
    print("MNIST training dataset downloaded.")

    # Create data loader
    train_data_loader = DataLoader(train_data, batch_size=BATCH_SIZE) # from torch.utils.data!

    # Build model
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device ="cpu"

    print(f"using device: {device}")
    feed_forward_net = FeedForwardNet().to(device)

    # Loss function & Optimiser setup
    loss_fn = nn.CrossEntropyLoss()
    optimiser =  torch.optim.Adam(feed_forward_net.parameters(), LEARNING_RATE)


    # Train model
    train(feed_forward_net, train_data_loader, loss_fn, optimiser, device, EPOCHS)

    torch.save(feed_forward_net.state_dict(), "feedforwardnet.pth")
    print("model trained and stored at feedforwardnet.pth")
