import h5py


def get_n_frames(video_path):
    print(video_path)
    frame_count = len([
        x for x in video_path.iterdir()
        # if 'image' in x.name and x.name[0] != '.'
        if '.jpg' in x.name and x.name[0] != '.'
    ])
    print(frame_count)
    return frame_count


def get_n_frames_hdf5(video_path):
    with h5py.File(video_path, 'r') as f:
        video_data = f['video']
        return len(video_data)
