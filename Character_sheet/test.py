import feats

feats_list = feats.get_feats()

for feat_name in feats_list:
    feat = (feats_list[feat_name])
    print(feat_name)
    print(feat.prereq())

print("Test Finished")