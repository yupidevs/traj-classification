from yuca import Featurizer, LangevinDataset, RandomForestModel, features

SEED = 0  # Random seed for reproducibility

# Load Dataset
dataset = LangevinDataset()

# Select the desired features to be extracted from the trajectories
featurizer = Featurizer(selected=features.ALL)

# Defining models
model = RandomForestModel(
    featurizer=featurizer,
    max_features=16,
    n_estimators=200,
    bootstrap=False,
    random_state=SEED,
    warm_start=True,
    n_jobs=6,
)

# Spliting dataset
train, test = dataset.split(0.8, random_state=SEED)

# Train the model
model.train(data=train, cross_validation=5)

# Evaluate the model on a test dataset
evaluation = model.evaluate(test)

# Print the evaluation
evaluation.show()
