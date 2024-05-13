import numpy as np

class HopfildNeurone:

    @staticmethod
    def f(net, pred_net):
        if net==0:
            return pred_net
        return 1 if net>0 else -1

    # pred_net: float
    def __init__(self, N, memorized_samples):
        self.N = N
        self.W = [[0]*self.N for i in range(self.N)]
        self.memorized_samples = memorized_samples
        self.prev_output = [0]*self.N
        self.cur_output = [0]*self.N

    def init_weights(self):
        # print(len(self.memorized_samples))
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    self.W[i][j]=0
                else:
                    for k in range(len(self.memorized_samples)):
                        self.W[i][j]+=self.memorized_samples[k][i]*self.memorized_samples[k][j]  
            
    def is_changed(self):
        for i in range(self.N):
            if self.cur_output[i] != self.prev_output[i]:
                return False
        return True

    def precess_net(self, y_cur, y_prev, k):
        # self.a.transpose()
        net = 0
        for i in range(self.N):
            if i<k:
                net += self.W[i][k]*y_cur[i]
            if k==i:
                continue
        # for i in range(k+1, self.N):
            net += self.W[i][k]*y_prev[i]
        return (net, y_prev[k])
    
    def recognition(self, X):
        self.prev_output = X
        self.cur_output = [0]*self.N
        changed = False
        while not changed:
            for i in range(self.N):
                self.cur_output[i] = self.f(*self.precess_net(self.cur_output, self.prev_output, i))
            changed = self.is_changed()
            self.prev_output = self.cur_output
            self.cur_output = [0]*self.N
        return self.prev_output
    
    @staticmethod
    def print_pattern(N, sample):
        M = int(len(sample)/N)
        for i in range(N):
            row = []
            j = i
            while j<len(sample):
                # print(j)
                if sample[j]==1:
                    row.append('#')
                else:
                    row.append(' ')
                j+=N
                # print(row)
            print(' '.join(row))
            # row.clear()

        

def test(right_out, cur_out):
    err = 0
    for i in range(len(right_out)):
        if right_out[i]!=cur_out[i]:
            err += 1
    return err


if __name__ == "__main__":
    '''
        [[-1, 1, -1],
        [1, 1, -1],
    1=  [-1, 1, -1],
        [-1, 1, -1],
        [1, 1, 1]]


        [[1, 1, 1],
        [-1, -1, 1],
    3=  [1, 1, 1],
        [-1, -1, 1],
        [1, 1, 1]]

        
        [[1, 1, 1],
        [-1, -1, 1],
    7=  [-1, 1, -1],
        [1, -1, -1],
        [1, -1, -1]]

    '''
    sample_1 = [-1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1]
    sample_3 = [1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1,1,1]
    sample_7 = [1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1]

    samples = [sample_1, sample_3, sample_7]
    hn = HopfildNeurone(3*5, samples)
    hn.init_weights()
 
    W = hn.W
    for i in range(len(W)):
        print(W[i])
    

    sample_1_inv_0 = [1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1]
    sample_1_inv_0_3 = [1, 1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1]
    sample_1_inv_6 = [-1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1]
    destr_1 = [sample_1_inv_0, sample_1_inv_0_3, sample_1_inv_6]
    for i in destr_1:
        hn.print_pattern(5, i)
        print(test(sample_1, hn.recognition(i)))

    sample_3_inv_12 = [1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, -1,1,1]
    sample_3_inv_12_13 = [1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, -1,-1,1]
    sample_3_inv_0 = [-1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1,1,1]
    destr_3 = [sample_3_inv_12, sample_3_inv_12_13, sample_3_inv_0]
    for i in destr_3:
        hn.print_pattern(5, i)
        print(test(sample_3, hn.recognition(i)))

    
    sample_7_inv_1 = [1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1]
    sample_7_inv_2_3 = [1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1]
    sample_7_inv_0 = [-1, -1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1]
    destr_7 = [sample_7_inv_1, sample_7_inv_2_3, sample_7_inv_0]
    for i in destr_7:
        hn.print_pattern(5, i)
        print()
        print(test(sample_7, hn.recognition(i)))    
        # hn.print_pattern(5, hn.recognition(i))