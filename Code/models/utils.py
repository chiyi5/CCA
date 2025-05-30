import torch
import numpy as np

def get_ranks(probs, labels, filters=None):

    log_probs = torch.log(probs)
    if filters is not None:
        log_probs[filters[:, 0], filters[:, 1]] = -torch.inf
    sorted_idx = torch.argsort(log_probs, dim=-1, descending=True)
    labels = labels.unsqueeze(dim=-1)
    rank = torch.nonzero(torch.eq(sorted_idx, labels))[:, 1] + 1  # rank从1开始
    return rank.cpu().numpy().tolist()

def get_norms(parameters, norm_type=2.0):
    if isinstance(parameters, torch.Tensor):
        parameters = [parameters]
    parameters = [p for p in parameters if p.grad is not None]
    norm_type = float(norm_type)
    if len(parameters) == 0:
        return torch.tensor(0.)
    device = parameters[0].grad.device
    total_norm = torch.norm(torch.stack([torch.norm(p.grad.detach(), norm_type).to(device) for p in parameters]), norm_type)
    return total_norm

def get_scores(rank: list, loss=None):
    rank = np.array(rank)
    hits1 = round(np.mean(rank <= 1) * 100, 2)
    hits3 = round(np.mean(rank <= 3) * 100, 2)
    hits10 = round(np.mean(rank <= 10) * 100, 2)
    mrr = round(float(np.mean(1. / rank)), 4)
    # mr = round(float(np.mean(rank)), 2)
    loss = np.round(np.mean(loss), 2)
    return {'loss': loss, 'hits@1': hits1, 'hits@3': hits3, 'hits@10': hits10, 'MRR': mrr}
