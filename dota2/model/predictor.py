import pyspark
from pyspark.ml.pipeline import PipelineModel
from dota2.api import opendota
from dota2.model import model_utils
from dota2.constants import model_constants


def predict(player):
    spark = pyspark.sql.SparkSession.builder.appName('Model Prep').getOrCreate()
    df = model_utils.prepare_player_df([player], spark)

    predicted_df = PipelineModel.load(model_constants.MODEL_LOCATION).transform(df)
    return opendota.heroes()[str(round(predicted_df.select("prediction").collect()[0][0]))]
