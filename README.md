# Brain Tumor Detection

During the 2025 summer [PFE](https://pfe.rs/) camp, I, Luka Marković, and my partner Elena Anđelković worked on identifying brain Tumors in MRI scans. We used the [Figshare Brain Tumor dataset](https://www.kaggle.com/datasets/nikhilroxtomar/brain-tumor-segmentation/data). Our mentors were Novak Stijepić and Vladan Bašić.

## Early Approaches
One of the first steps we took was processing the images to make it easier to analyse. We tested various ways to do so, the most significant of which were the [Canny edge detector algorithm](https://en.wikipedia.org/wiki/Canny_edge_detector), and [Otsu's method](https://en.wikipedia.org/wiki/Otsu%27s_method). We ended up proceeding with Otsu's method, along with applying dilation and erosion filters on the image. This processing, along with a crude algorithim, resulted in 10.2% accuracy in identifying the brain tumors.

## Machine Learning
The next step was to look into choosing a type of Machine Learning suitable for this, as well as the model. After thorough consideration we chose to take a pre-trained [U-Net](https://en.wikipedia.org/wiki/U-Net) model, [resnet34](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.resnet34.html), which is trained on the [ImageNet](https://www.image-net.org/) database, and fine-tuned it using the Figshare Brain tumor dataset previously mentioned. With this approach we were able to reach an accuracy as high as 93.15%, and a loss of 0.39 before hitting a soft-cap.

## Results
![Image 1. We see the training accuracy by Epochs](https://i.postimg.cc/cCpgJW3n/accuracy.png)
![Image 2. We see the loss by Epochs](https://i.postimg.cc/Vspbgqhk/loss.png)