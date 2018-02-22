import json

shape_size_factor = {
    'cube': (1., .95),
    'sphere': (.75, .75),
    'cylinder': (0.95, .8),
}


def get_bbox(obj, scale=360.):
    x, y, z = obj['pixel_coords']
    size = 2. if obj['size'] == 'large' else 1.
    shape = obj['shape']

    scaled_size = size * scale / z
    hs, ws = shape_size_factor[shape]
    h, w = scaled_size * hs, scaled_size * ws
    x1 = int(round(x - w / 2.))
    y1 = int(round(y - h / 2.))
    x2 = int(round(x + w / 2.))
    y2 = int(round(y + h / 2.))
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    bbox = [x1, y1, w, h]
    return bbox


question_file = '/home/ronghang/workspace/DATASETS/CLEVR_loc/questions/CLEVR_%s_questions.json'
save_question_file = '/home/ronghang/workspace/DATASETS/CLEVR_loc/questions/CLEVR_%s_questions_with_bbox.json'
scene_file = '/home/ronghang/workspace/DATASETS/CLEVR_loc/scenes/CLEVR_%s_scenes.json'
for split in ['loc_train', 'loc_val', 'loc_test']:
    with open(question_file % split) as f:
        questions = json.load(f)
    with open(scene_file % split) as f:
        scenes = json.load(f)

    print('loaded %d questions in %d scenes in %s' %
          (len(questions['questions']), len(scenes['scenes']), split))
    for q in questions['questions']:
        s = scenes['scenes'][q['image_index']]
        assert q['image_index'] == s['image_index']
        q_refexp_obj = s['objects'][q['refexp_obj']]
        q['bbox'] = get_bbox(q_refexp_obj)
    with open(save_question_file % split, 'w') as f:
        json.dump(questions, f)
