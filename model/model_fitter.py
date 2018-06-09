import pyspark
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.pipeline import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from constants import model_constants
from model import model_utils


def train_model(training_size, mode):
    print('Training model with records: ' + str(training_size))
    spark = pyspark.sql.SparkSession.builder.appName('Model Prep').getOrCreate()
    data_df = model_utils.get_player_df(spark, training_size, mode)

    pipeline = Pipeline().setStages(transform_stages())
    model = pipeline.fit(data_df)

    model.write().overwrite().save(model_constants.MODEL_LOCATION)


def transform_stages():
    features_list = ['kda', 'gold_per_min', 'xp_per_min', 'last_hits', 'denies',
                     'lane_efficiency_pct', 'hero_damage', 'tower_damage', 'hero_healing',
                     'stuns', 'tower_kills', 'neutral_kills', 'courier_kills', 'actions_per_min']

    assembler = VectorAssembler().setInputCols(features_list).setOutputCol("assembled_features")
    std_scaler = StandardScaler().setInputCol("assembled_features").setOutputCol("features")

    return [assembler, std_scaler, model_fitter()]


def model_fitter():
    return RandomForestRegressor(labelCol="best_hero", featuresCol="features")


def model_evaluator(predictions):
    # Select (prediction, true label) and compute test error
    evaluator = MulticlassClassificationEvaluator(
        labelCol="best_hero", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print("Test Error = %g " % (1.0 - accuracy))
