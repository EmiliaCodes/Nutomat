from keras.layers import Bidirectional, Input, LSTM, Dense, Embedding, Dropout, Concatenate, Lambda, Reshape, \
    Activation, Permute, Multiply, RepeatVector
from keras.models import Model
from keras.optimizers import RMSprop
import keras.backend as K


def create_model(rhythm_dict, pitch_dict, path):
    # Parameters
    embedding_size = 125
    rnn_units = 315

    # Useful training set variables
    rhythm_size = len(rhythm_dict)
    pitch_size = len(pitch_dict)

    # Building the architecture
    pitch_in = Input(shape=(None,), name='pitch_input')
    rhythm_in = Input(shape=(None,), name='rhythm_input')

    pitch_embed = Embedding(pitch_size, embedding_size, name='pitch_embedded')(pitch_in)
    rhythm_embed = Embedding(rhythm_size, embedding_size, name='rhythm_embedded')(rhythm_in)

    x = Concatenate()([pitch_embed, rhythm_embed])

    x = Bidirectional(LSTM(rnn_units, return_sequences=True), name='bidirectional_lstm')(x)  # Second layer - BiLSTM
    x = LSTM(rnn_units, return_sequences=False, name='lstm_forward')(x)  # Second LSTM layer

    # Attention
    e = Dense(1, activation='tanh')(x)
    e = Reshape([-1])(e)

    weights = Activation('softmax')(e)
    weights_repeat = Permute([2, 1])(RepeatVector(rnn_units)(weights))

    c = Multiply()([x, weights_repeat])
    c = Lambda(lambda xin: K.sum(xin, axis=1), output_shape=(rnn_units,))(c)
    c = Reshape([-1])(c)

    pitch_out = Dense(pitch_size, activation='softmax', name='pitch_output')(c)
    rhythm_out = Dense(rhythm_size, activation='softmax', name='rhythm_output')(c)

    model = Model([pitch_in, rhythm_in], [pitch_out, rhythm_out])

    opti = RMSprop(learning_rate=0.001)
    model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], optimizer=opti)

    # Loading previously saved weights from .h5 file
    model.load_weights(path)

    return model
