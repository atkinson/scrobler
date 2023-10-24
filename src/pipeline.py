import apache_beam as beam


# 1. Stream into pubsub
# 2. Read from pubsub
# 3. Stream


# Create a PCollection to read the initial data from IOs (pubsub)
# Can replay the firestore data into pubsub for testing.
# Apply PTransforms to augment the data with spotify attributes

with beam.Pipeline() as pipeline:
    result = (
        pipeline
        | 'Get newly played tracks' >> beam.Create([1, 2, 3, 4])
        | 'Add spotify metadata' >> beam.Map(lambda x: x * 2)
        | 'Add to playlist' >> beam.CombineGlobally(sum)
        | 'Print results' >> beam.Map(print)
    )