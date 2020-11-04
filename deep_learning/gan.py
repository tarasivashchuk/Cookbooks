import torch
import torchvision
from torch import nn, optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets, transforms
from tqdm import tqdm


class Discriminator(nn.Module):
    def __init__(self, img_dim):
        super().__init__()
        self.disc = nn.Sequential(
            nn.Linear(img_dim, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.disc(x)


class Generator(nn.Module):
    def __init__(self, z_dim, img_dim):
        super().__init__()
        self.gen = nn.Sequential(
            nn.Linear(z_dim, 256),
            nn.LeakyReLU(0.1),
            nn.Linear(256, img_dim),
            nn.Tanh()  # to ensure pixel values are between -1 and 1
        )

    def forward(self, x):
        return self.gen(x)


device = "cuda"
lr = 3e-4
z_dim = 64  # 128, 256
img_dim = 28 * 28
batch_size = 32
epochs = 50

disc = Discriminator(img_dim).to(device)
gen = Generator(z_dim, img_dim).to(device)
fixed_noise = torch.randn((batch_size, z_dim)).to(device)
transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
dataset = datasets.MNIST(root="data/", transform=transforms, download=True)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
opti_d = optim.Adam(disc.parameters(), lr=lr)
opti_g = optim.Adam(gen.parameters(), lr=lr)
criterion = nn.BCELoss()

writer_fake = SummaryWriter("runs/fake")
writer_real = SummaryWriter("runs/real")
step = 0

for epoch in tqdm(range(epochs), total=epochs, desc="Epoch"):
    with tqdm(enumerate(loader), total=len(dataset) // batch_size, desc="0.000/0.000") as progress_datafeed:
        for batch_idx, (real, _) in progress_datafeed:
            real = real.view(-1, 784).to(device)
            batch_size = real.shape[0]

            noise = torch.randn(batch_size, z_dim).to(device)
            fake = gen(noise)

            # Train discriminator: max log(D(real) + log(1 - D(G(z))
            disc_real = disc(real).view(-1)
            loss_disc_real = criterion(disc_real, torch.ones_like(disc_real))
            disc_fake = disc(fake).view(-1)
            loss_disc_fake = criterion(fake, torch.zeros_like(disc_fake))
            loss_disc = (disc_real - disc_fake) / 2
            disc.zero_grad()
            loss_disc.backward(retain_graph=True)  # retain graph for reuse of fake matrix
            opti_d.step()

            # Train generator: min log(1 - D(G(z))) <-> max log(D(G(z))
            output = disc(fake).view(-1)
            loss_gen = criterion(output, torch.ones_like(output))
            gen.zero_grad()
            loss_gen.backward()
            opti_g.step()
            progress_datafeed.desc = f"D:{loss_disc:.3f} G:{loss_gen:.3f}"
            if batch_idx == 0:
                with torch.no_grad():
                    fake = gen(fixed_noise).reshape(-1, 1, 28, 28)
                    data = real.reshape(-1, 1, 28, 28)
                    img_grid_fake = torchvision.utils.make_grid(fake, normalize=True)
                    img_grid_real = torchvision.utils.make_grid(data, normalize=True)
                    writer_fake.add_image(
                        "Generated", img_grid_fake, global_step=step
                    )
                    writer_real.add_image(
                        "Generated", img_grid_real, global_step=step
                    )
                    step += 1
