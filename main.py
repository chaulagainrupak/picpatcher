import os
from PIL import Image

def load_and_sort_images(folderPath):
    """Load images from a folder and sort by creation time."""
    images = []
    for filename in os.listdir(folderPath):
        filePath = os.path.join(folderPath, filename)
        if os.path.isfile(filePath) and filename.lower().endswith(('png', 'jpg', 'jpeg')):
            images.append((filePath, os.path.getmtime(filePath)))
    # Sort images by creation time
    images.sort(key=lambda x: x[1])
    return [Image.open(img[0]) for img in images], [img[0] for img in images]

def center_align_images(images):
    """Center-align images and fill transparent areas with white."""
    maxWidth = max(img.width for img in images)
    alignedImages = []

    for img in images:
        # Create a new image with maxWidth, height of current image, and white background
        newImage = Image.new('RGB', (maxWidth, img.height), (255, 255, 255))
        offsetX = (maxWidth - img.width) // 2
        newImage.paste(img, (offsetX, 0))
        alignedImages.append(newImage)

    return alignedImages

def concatenate_images(images, padding=20):
    """Concatenate images vertically with padding."""
    totalHeight = sum(img.height for img in images) + padding * (len(images) - 1)
    maxWidth = max(img.width for img in images)

    # Create a new canvas for the final image
    finalImage = Image.new('RGB', (maxWidth, totalHeight), (255, 255, 255))

    yOffset = 0
    for img in images:
        finalImage.paste(img, (0, yOffset))
        yOffset += img.height + padding

    return finalImage

def process_folder(folderPath, outputFileName):
    """Process a folder of images and save the concatenated result."""
    images, filePaths = load_and_sort_images(folderPath)
    if not images:
        print(f"No images found in {folderPath}")
        return

    alignedImages = center_align_images(images)
    finalImage = concatenate_images(alignedImages)

    # Save the final image, overwriting if it exists
    finalImage.save(outputFileName)
    print(f"Saved {outputFileName}")

    # Remove original images
    for filePath in filePaths:
        os.remove(filePath)
    print(f"Removed images from {folderPath}")

def main():
    # Folders and output files
    questionFolder = "questions"
    solutionFolder = "solutions"

    questionOutput = "question.png"
    solutionOutput = "solution.png"

    if not os.path.exists(questionFolder):
        print(f"Folder '{questionFolder}' not found!")
        return

    if not os.path.exists(solutionFolder):
        print(f"Folder '{solutionFolder}' not found!")
        return

    # Process each folder
    process_folder(questionFolder, questionOutput)
    process_folder(solutionFolder, solutionOutput)

if __name__ == "__main__":
    main()
