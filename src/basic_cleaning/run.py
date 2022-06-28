#!/usr/bin/env python
"""
example of step using mlflow and W&B
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Getting the data...")

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact


    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)

    min_price = args.min_price
    max_price = args.max_price

    logger.info(f"Filtering data by min_price {min_price} and max_price {max_price}")

    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    local_file =  "clean_sample.csv"
    df.to_csv(local_file, index=False)

    logger.info(f"Saving and uploading cleaned data....")

    artifact = wandb.Artifact(
    args.output_artifact,
    type=args.output_type,
    description=args.output_description,
 )
    artifact.add_file(local_file)
    run.log_artifact(artifact)

    logger.info(f"Finished cleaning process!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="this step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type = str,
        help = "name and version of input artifact",
        required = True
    )

    parser.add_argument(
        "--output_artifact", 
        type = str,
        help = "name of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type = str,
        help = "type of the data",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type = str,
        help = "type of the data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type = float,
        help = "min price to filter by",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type = float,
        help = "max price to filter by",
        required=True
    )




    args = parser.parse_args()

    go(args)