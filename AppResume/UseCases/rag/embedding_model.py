from sentence_transformers import SentenceTransformer

model = None


def load_model():

    global model

    if model is None:

        model = SentenceTransformer(
            'all-MiniLM-L6-v2'
        )

    return model


def create_embedding(text):

    current_model = load_model()

    embedding = current_model.encode(text)

    return embedding