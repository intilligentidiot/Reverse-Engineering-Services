import os
import glob
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import torch

def load_model():
    print("Loading CLIP model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = SentenceTransformer('clip-ViT-B-32', device=device)
    return model

def find_images(directory, extensions=['*.jpg', '*.jpeg', '*.png', '*.webp']):
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(directory, '**', ext), recursive=True))
    return image_paths

def main():
    # Set directory to search (current directory)
    search_path = "."
    
    print(f"Scanning for images in {os.path.abspath(search_path)}...")
    image_paths = find_images(search_path)
    
    if not image_paths:
        print("No images found in the current directory or subdirectories.")
        return

    print(f"Found {len(image_paths)} images. generating embeddings...")
    
    model = load_model()
    
    # Load images and generate embeddings
    images = []
    valid_paths = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
            valid_paths.append(path)
        except Exception as e:
            print(f"Error loading {path}: {e}")

    if not valid_paths:
        print("No valid images could be loaded.")
        return

    # Encode images
    image_embeddings = model.encode(images, convert_to_tensor=True)
    
    print("\nSetup complete! You can now search for images by description.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("Enter search query: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        # Encode text query
        query_embedding = model.encode([query], convert_to_tensor=True)
        
        # Compute cosine similarities
        hits = util.semantic_search(query_embedding, image_embeddings, top_k=3)[0]
        
        print(f"\nTop 3 matches for '{query}':")
        for hit in hits:
            score = hit['score']
            idx = hit['corpus_id']
            path = valid_paths[idx]
            print(f"  Score: {score:.4f} | Path: {path}")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()
