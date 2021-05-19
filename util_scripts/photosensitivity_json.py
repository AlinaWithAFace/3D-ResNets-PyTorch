import argparse
import json
from pathlib import Path

import pandas as pd

# from .utils import get_n_frames
# See https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
from utils import get_n_frames


def convert_csv_to_dict(csv_path, subset):
    data = pd.read_csv(csv_path, delimiter=',')
    keys = []
    key_labels = []
    for i in range(data.shape[0]):
        row = data.iloc[i, :]
        # print(row)
        slash_rows = data.iloc[i, 0].split('/')
        # print(slash_rows)
        # class_name = slash_rows[0]
        class_name = row[4]
        # basename = slash_rows[1].split('.')[0]
        basename = row[0]

        keys.append(basename)
        key_labels.append(class_name)

    database = {}
    for i in range(len(keys)):
        key = keys[i]
        database[key] = {}
        database[key]['subset'] = subset
        label = key_labels[i]
        database[key]['annotations'] = {'label': label}

    print(database)
    return database


def load_labels(label_csv_path):
    data = pd.read_csv(label_csv_path, delimiter=' ', header=None)
    labels = []
    for i in range(data.shape[0]):
        # labels.append(data.iloc[i, 1])
        labels.append(data.iloc[i, 1])
    print(labels)
    return labels


def convert_photosensitivity_csv_to_json(label_csv_path, annotation_csv_path, video_dir_path, dst_json_path):
    labels = load_labels(label_csv_path)
    train_database = convert_csv_to_dict(annotation_csv_path, 'training')
    # val_database = convert_csv_to_dict(val_csv_path, 'validation')

    dst_data = {}
    dst_data['labels'] = labels
    dst_data['database'] = {}
    dst_data['database'].update(train_database)
    # dst_data['database'].update(val_database)

    for k, v in dst_data['database'].items():
        if v['annotations'] is not None:
            label = v['annotations']['label']
        else:
            label = 'test'

        video_path = video_dir_path / label / k
        # print(video_path)
        n_frames = get_n_frames(video_path)
        # print(n_frames)
        v['annotations']['segment'] = (1, n_frames + 1)

    with dst_json_path.open('w') as dst_file:
        json.dump(dst_data, dst_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path',
                        default=None,
                        type=Path,
                        help=('Directory path including '
                              'labels.txt'))
    parser.add_argument('video_path',
                        default=None,
                        type=Path,
                        help=('Path of video directory (jpg).'
                              'Using to get n_frames of each video.'))
    parser.add_argument('dst_path',
                        default=None,
                        type=Path,
                        help='Directory path of dst json file.')

    args = parser.parse_args()

    label_csv_path = args.dir_path / 'labels.txt'
    annotation_csv_path = args.dir_path / 'social-media-study.txt'
    dst_json_path = args.dst_path / 'photosensitivity_0.json'

    convert_photosensitivity_csv_to_json(label_csv_path, annotation_csv_path, args.video_path, dst_json_path)
