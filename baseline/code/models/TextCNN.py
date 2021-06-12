# coding: UTF-8
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd


class Config(object):


    def __init__(self, dataset, embedding):
        self.model_name = 'TextCNN'
        self.train_path = dataset + './../data/new_train.txt'
        self.dev_path = dataset + './../data/new_dev.txt'
        self.test_path = dataset + './../data/new_test.txt'
        # self.class_list = [x.strip() for x in open(
        #     dataset + '/data/class.txt', encoding='utf-8').readlines()]
        self.vocab_path =  "char_embeddings.word2id.pkl" #dataset + './../data/vocab.pkl' #
        self.save_path = dataset + './saved_dict/' + self.model_name + '.ckpt'
        self.log_path = dataset + './log/' + self.model_name
        self.embedding_pretrained = torch.tensor(
            np.array(pd.read_pickle("char_embeddings.embeddings.pkl")).astype('float32'))\
            if embedding != 'random' else None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.dropout = 0.5
        self.require_improvement = 1000
        self.num_classes = 2  # len(self.class_list)
        self.n_vocab = 0
        self.num_epochs = 10
        self.batch_size = 16
        self.pad_size = 150
        self.learning_rate = 1e-3
        self.embed = self.embedding_pretrained.size(1)\
            if self.embedding_pretrained is not None else 300
        self.filter_sizes = (2, 3, 4)
        self.num_filters = 256

'''Convolutional Neural Networks for Sentence Classification'''


class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        if config.embedding_pretrained is not None:
            self.embedding = nn.Embedding.from_pretrained(config.embedding_pretrained, freeze=False)
        else:
            self.embedding = nn.Embedding(config.n_vocab, config.embed, padding_idx=config.n_vocab - 1)
        # self.convs = nn.ModuleList(
        #     [nn.Conv2d(1, config.num_filters, (k, config.embed)) for k in config.filter_sizes])
        self.convs = nn.ModuleList(
            [nn.Conv1d(300, 300, kernel_size=3, padding=1),
             nn.Conv1d(300, 300, kernel_size=5, padding=2),
             nn.Conv1d(300, 300, kernel_size=7, padding=3)]
        )
        self.dropout = nn.Dropout(config.dropout)
        self.fc = nn.Linear(300, config.num_classes)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        out = self.embedding(x[0])
        out = out.permute(0, 2, 1)
        for conv in self.convs:
            out = conv(out)
            out = F.relu(out)
        out = F.max_pool1d(out, out.size(2)).squeeze(2)
        out = self.dropout(out)
        out = self.fc(out)
        return out
