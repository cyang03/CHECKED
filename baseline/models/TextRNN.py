# coding: UTF-8
import torch
import torch.nn as nn
import numpy as np
import pandas as pd


class Config(object):

    """配置参数"""
    def __init__(self, dataset, embedding):
        self.model_name = 'TextRNN'
        self.train_path = dataset + '../../dataset/new_train.txt'                                 
        self.dev_path = dataset + '../../dataset/new_dev.txt'                                    
        self.test_path = dataset + '../../dataset/new_test.txt'                                  
        self.vocab_path = "char_embeddings.word2id.pkl"
        self.save_path = dataset + './saved_dict/' + self.model_name + '.ckpt'  
        self.log_path = dataset + './log/' + self.model_name
        self.embedding_pretrained = torch.tensor(
            np.array(pd.read_pickle("char_embeddings.embeddings.pkl")).astype('float32')) \
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
        self.hidden_size = 128                                          
        self.num_layers = 2                                             


'''Recurrent Neural Network for Text Classification with Multi-Task Learning'''


class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        if config.embedding_pretrained is not None:
            self.embedding = nn.Embedding.from_pretrained(config.embedding_pretrained, freeze=False)
        else:
            self.embedding = nn.Embedding(config.n_vocab, config.embed, padding_idx=config.n_vocab - 1)
        self.lstm = nn.LSTM(config.embed, config.hidden_size, config.num_layers,
                            bidirectional=True, batch_first=True, dropout=config.dropout)
        self.fc = nn.Linear(config.hidden_size * 2, config.num_classes)

    def forward(self, x):
        x, _ = x
        out = self.embedding(x)  # [batch_size, seq_len, embeding]=[128, 32, 300]
        out, _ = self.lstm(out)
        out = self.fc(out[:, -1, :])  
        return out

