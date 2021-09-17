from scipy.io import wavfile
import os

import numpy as np
from scipy.io import wavfile
from torch.utils.data import DataLoader
from tqdm import tqdm

from models.spleeter.separator import Separator
from scripts.audio.preparation.spleeter_dataset import SpleeterDataset


def main():
    src_dir = 'F:\\split\\joe_rogan'
    output_sample_rate=22050
    batch_size=16

    dl = DataLoader(SpleeterDataset(src_dir, output_sample_rate, skip=batch_size*33000), batch_size=batch_size, shuffle=False, num_workers=1, pin_memory=True)
    separator = Separator('pretrained_models/2stems', input_sr=output_sample_rate)
    unacceptable_files = open('unacceptable.txt', 'a')
    for batch in tqdm(dl):
        waves = batch['wave']
        paths = batch['path']
        durations = batch['duration']

        sep = separator.separate(waves)
        for j in range(sep['vocals'].shape[0]):
            vocals = sep['vocals'][j][:durations[j]]
            bg = sep['accompaniment'][j][:durations[j]]
            vmax = np.abs(vocals[output_sample_rate:-output_sample_rate]).mean()
            bmax = np.abs(bg[output_sample_rate:-output_sample_rate]).mean()

            # Only output to the "good" sample dir if the ratio of background noise to vocal noise is high enough.
            ratio = vmax / (bmax+.0000001)
            if ratio < 4:  # These values were derived empirically
                unacceptable_files.write(f'{paths[j]}\n')
        unacceptable_files.flush()
    unacceptable_files.close()


# Uses torch spleeter to divide audio clips into one of two bins:
# 1. Audio has little to no background noise, saved to "output_dir"
# 2. Audio has a lot of background noise, bg noise split off and saved to "output_dir_bg"
if __name__ == '__main__':
    main()
