
from os.path import join
from PIL import Image
from torchvision import transforms
import torch
from tqdm import tqdm

def preprocess(data_dir, split):

    print("Process {} dataset...".format(split))

    images_dir = join(data_dir, "formula_images_processed")

    formulas_file = join(data_dir, "im2latex_formulas.norm.lst")
    with open(formulas_file, 'r') as f:
        formulas = [formula.strip('\n') for formula in f.readlines()]
    split_file = join(data_dir, "im2latex_{}_filter.lst".format(split))
    pairs = []
    transform = transforms.ToTensor()
    with open(split_file, 'r') as f:
        for line in tqdm(f):
            img_name, formula_id = line.strip('\n').split()
            img_path = join(images_dir, img_name)
            try:
                img = Image.open(img_path)
                img_tensor = transform(img)
                formula = '$' + formulas[int(formula_id)] + '$'
                pair = (img_tensor, formula)
                pairs.append(pair)
            except:
                pass
        pairs.sort(key=img_size)

    out_file = join(data_dir, "{}.pkl".format(split))
    torch.save(pairs, out_file)
    print("Save {} dataset to {}".format(split, out_file))


def img_size(pair):
    img, formula = pair
    return tuple(img.size())


if __name__ == "__main__":
    splits = ["validate", "test", "train"]
    for s in splits:
        preprocess('data/', s)
