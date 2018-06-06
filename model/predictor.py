import pyspark
from constants import model_constants
from model import model_utils
from pyspark.ml.pipeline import PipelineModel

from api import opendota


def predict(player):
    spark = pyspark.sql.SparkSession.builder.appName('Model Prep').getOrCreate()
    df = model_utils.prepare_player_df([player], spark)

    predicted_df = PipelineModel.load(model_constants.MODEL_LOCATION).transform(df)
    return opendota.heroes()[str(round(predicted_df.select("prediction").collect()[0][0]))]
