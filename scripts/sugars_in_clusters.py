
import pandas as pd
from PIL import Image
import sys
import numpy as np
import matplotlib.pyplot as plt

cluster_df = pd.read_csv("clusters_ssns/clusters_1e-30_150.tsv", sep = '\t', header=None, names=['acc', 'cluster'])

info_df = pd.read_csv("polymerase_data/wzy_with_csdb_and_taxonomy.tsv", sep = '\t')

image_folder = "data/cluster_csdb_images/"

combined_image_paths = list()
# Make cluster images
for cluster in cluster_df.cluster.unique():
    members = cluster_df.loc[cluster_df.cluster == cluster, 'acc']
    combined_image_path = image_folder + str(cluster).zfill(3) + '.jpg'
    combined_image_paths.append(combined_image_path)
    # single_image_paths = list()
    # fs = []
    # largest_x = 0
    # largest_y = 0
    # for member in members:
    #     rows = info_df.loc[info_df.protein_accession == member]
    #     if len(rows) > 0:
    #         if pd.isnull(rows.iloc[0]['csdb_image_path']):
    #             continue
    #         else:
    #             single_image_path = rows.iloc[0]['csdb_image_path'].replace('https://raw.githubusercontent.com/idameitil/wzy_polymerases/main/', '')
    #             if single_image_path == 'csdb/snfg/3/.gif':
    #                 continue
    #             single_image_paths.append(single_image_path)
    #             im = Image.open(single_image_path,'r')
    #             fs.append(im)
    #             # Get size
    #             x,y = im.size
    #             if x > largest_x:
    #                 largest_x = x
    #             if y > largest_y:
    #                 largest_y = y
    # # Make cluster image
    # if len(single_image_paths) > 0:
    #     images = [Image.open(x) for x in single_image_paths]

    #     widths, heights = zip(*(i.size for i in images))

    #     #max_width = max(widths)
    #     max_width = 1176
    #     total_height = 1176
    #     #total_height = sum(heights)
    #     new_im_no_border = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

    #     y_offset = 0
    #     for im in images:
    #         new_im_no_border.paste(im, (0, y_offset))
    #         y_offset += im.size[1]

    #         #new_im.save(combined_image_path)

    #     # add black border
    #     old_size = (1176, 1176)
    #     new_size = (1200, 1200)
    #     new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
    #     new_im.paste(new_im_no_border, ((new_size[0]-old_size[0])//2,
    #                   (new_size[1]-old_size[1])//2))
    #     new_im.save(combined_image_path)

    # # Make empty image, if no sugars
    # if len(single_image_paths) == 0:
    #     new_im_no_border = Image.new('RGB', (1176, 1176), color=(255, 255, 255))
    #     #new_im.save(combined_image_path)

    #     # add black border
    #     old_size = (1176, 1176)
    #     new_size = (1200, 1200)
    #     new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
    #     new_im.paste(new_im_no_border, ((new_size[0]-old_size[0])//2,
    #                   (new_size[1]-old_size[1])//2))
    #     new_im.save(combined_image_path)

# Make combined image
def gallery(array, ncols=10):
    print(array.shape)
    nindex, height, width, intensity = array.shape
    nrows = nindex//ncols
    assert nindex == nrows*ncols # make sure to have a number dividable by 10 (add empty ones below)
    result = (array.reshape(nrows, ncols, height, width, intensity)
              .swapaxes(1,2)
              .reshape(height*nrows, width*ncols, intensity))
    return result
def make_array():
    from PIL import Image
    return np.array([np.asarray(Image.open(combined_image_paths[0]).convert('RGB'))]*12)
print(np.asarray(Image.open(combined_image_paths[0]).convert('RGB')).shape)
array = make_array()

combined_image_paths.sort()
combined_image_paths.append(combined_image_paths[221]) # put an empty one in the end so there are 230
data = []
for i in combined_image_paths:
    data.append(np.asarray(Image.open(i).convert('RGB')))

array = np.array(data)
result = gallery(array)
im = Image.fromarray(result)
im.save('data/sugars_in_clusters.jpeg')