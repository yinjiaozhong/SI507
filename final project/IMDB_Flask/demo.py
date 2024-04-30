import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphAttentionLayer(nn.Module):
    def __init__(self, in_features, out_features, dropout=0.6, alpha=0.2):
        super(GraphAttentionLayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.dropout = dropout
        self.alpha = alpha

        self.W = nn.Parameter(torch.FloatTensor(in_features, out_features))
        self.a = nn.Parameter(torch.FloatTensor(2*out_features, 1))

        self.leakyrelu = nn.LeakyReLU(self.alpha)
        self.dropout = nn.Dropout(self.dropout)

        self.init_weights()

    def init_weights(self):
        nn.init.xavier_uniform_(self.W.data, gain=1.414)
        nn.init.xavier_uniform_(self.a.data, gain=1.414)

    def forward(self, input, adj):
        h = torch.matmul(input, self.W)
        N = h.size(0)
        
        h_repeated = h.unsqueeze(1).repeat(1, N, 1)
        h_repeated_transposed = h.unsqueeze(0).repeat(N, 1, 1)
        a_input = torch.cat([h_repeated, h_repeated_transposed], dim=-1)
        
        e = self.leakyrelu(torch.matmul(a_input, self.a).squeeze(2))

        zero_vec = -9e15*torch.ones_like(e)
        attention = torch.where(adj > 0, e, zero_vec)

        attention = F.softmax(attention, dim=1)
        attention = self.dropout(attention)

        h_prime = torch.matmul(attention, h)
        return F.elu(h_prime)

class GATModel(nn.Module):
    def __init__(self, feature_dim, embed_dim, num_heads=4, dropout=0.6, alpha=0.2):
        super(GATModel, self).__init__()
        self.feature_dim = feature_dim
        self.embed_dim = embed_dim
        self.num_heads = num_heads

        self.embedding_layer = nn.Linear(feature_dim, embed_dim)
        self.gat_layer = nn.ModuleList([
            GraphAttentionLayer(embed_dim, embed_dim // num_heads, dropout, alpha)
            for _ in range(num_heads)
        ])

    def forward(self, features, adj):
        embedded_features = self.embedding_layer(features)
        head_outputs = [gat(embedded_features, adj) for gat in self.gat_layer]
        output = torch.cat(head_outputs, dim=-1).mean(dim=0)  # Combine outputs from all heads
        return output

def find_most_similar(embeddings, query_embedding, n=5):
    # 计算余弦相似度
    similarity_scores = F.cosine_similarity(embeddings, query_embedding.unsqueeze(0), dim=-1)
    # 获取最相关的n个嵌入的索引
    top_indices = similarity_scores.argsort(descending=True)[:n]
    return top_indices

# 初始化特征矩阵嵌入和预测特征嵌入
feature_matrix_embed = torch.randn(128, 2048)
prediction_feature_embed = torch.randn(128, 2048)

# 初始化邻接矩阵（这里假设是全连接图）
adj_matrix = torch.ones(feature_matrix_embed.size(0), feature_matrix_embed.size(0))

# 初始化GAT模型
gat_model = GATModel(2048, 128)

# 将特征矩阵嵌入和预测特征嵌入输入GAT模型
feature_matrix_output = gat_model(feature_matrix_embed, adj_matrix)
prediction_feature_output = gat_model(prediction_feature_embed, adj_matrix)

# 寻找最相关的嵌入索引
n_most_similar = 5
for i in range(prediction_feature_output.size(0)):
    most_similar_indices = find_most_similar(feature_matrix_output, prediction_feature_output[i], n_most_similar)
    print(f"For prediction feature {i}, most similar embeddings indices: {most_similar_indices}")
