import numpy as np
from scipy import ndimage


class heuristic():
    def __init__(self,rules):
        self.rules=rules
        self.dim=None


class naive(heuristic):
    def __init__(self,rules):
        self.rules=rules
        self.dim=1
    def __call__(self,board):
        white_score=np.count_nonzero(board.matrix == 1)/np.sum(np.abs(board.matrix))
        if board.current_color=='White':
            return white_score
        else :
            return 1-white_score

class positions(heuristic):
    def __init__(self,rules):
        self.rules=rules
        self.n=rules.N//2
        self.dim=self.n*(self.n+1)//2

    def __call__(self,board):
        n=self.n
        matrix=board.matrix
        matrix_sym=matrix[0:n,0:n]+np.flip(matrix[n:,0:n],axis=0)+np.flip(matrix[0:n,n:],axis=1)+np.flip(matrix[n:,n:],axis=(0,1))
        matrix_sym_copy=matrix_sym.copy()
        np.fill_diagonal(matrix_sym_copy, 0)
        matrix_sym=matrix_sym+matrix_sym_copy.T
        features=[matrix_sym[i,j] for i in range(n) for j in range(i,n)]
        return features

class mobility(heuristic):
    def __init__(self,rules):
        self.rules=rules
        self.dim=1

    def __call__(self,board):
        if board.current_color=='Black':
            black_mobility=len(board.valid_moves)
            board_white=board.copy()
            board_white.current_color='White'
            white_mobility=len(self.rules.list_valid_moves(board_white))
        else:
            white_mobility=len(board.valid_moves)
            board_black=board.copy()
            board_black.current_color='Black'
            black_mobility=len(self.rules.list_valid_moves(board_black))
        return (white_mobility-black_mobility)/(white_mobility+black_mobility+1e-6)



class potential_mobility(heuristic):
    def __init__(self,rules):
        self.dim=1
        self.neighbors_kernel=np.zeros((3,3))+1
        self.neighbors_kernel[1,1]=0

    def __call__(self,board):
       
        matrix=board.matrix
        empty=(matrix==0)

        black_matrix=np.where(matrix==-1,1,0)
        black_adj=ndimage.convolve(black_matrix, self.neighbors_kernel, mode='constant', cval=0)
        white_potential=(black_adj*empty>0).sum()

        white_matrix=np.where(matrix==1,1,0)
        white_adj=ndimage.convolve(white_matrix, self.neighbors_kernel, mode='constant', cval=0)
        black_potential=(white_adj*empty>0).sum()

        return (white_potential-black_potential)/(white_potential+black_potential)


class corner_count(heuristic):

    def __init__(self,rules):
        self.dim=1
    
    def __call__(self,board):
        matrix=board.matrix
        corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])/4
        return corners

class precorners_count(heuristic):

    def __init__(self,rules):
        self.dim=1
    
    def __call__(self,board):
        matrix=board.matrix
        precorners=0
        precorners+=(matrix[1,1]+matrix[1,0]+matrix[0,1])*(1-np.abs(matrix[0,0]))
        precorners+=(matrix[-2,-2]+matrix[-1,-2]+matrix[-2,-1])*(1-np.abs(matrix[-1,-1]))
        precorners+=(matrix[0,-2]+matrix[1,-2]+matrix[1,-1])*(1-np.abs(matrix[0,-1]))
        precorners+=(matrix[-2,0]+matrix[-2,1]+matrix[-1,1])*(1-np.abs(matrix[-1,0]))
        return precorners

    
class corner_stability(heuristic):
    def __init__(self,rules):
        self.N=rules.N
        self.dim=1

    def __call__(self,board):

        matrix=board.matrix
        N=self.N
        corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])/4

        line_min=0
        full=True
        while full and line_min<N:
            line=matrix[line_min,:]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                line_min+=1
            else:
                full=False
        
        line_max=N
        full=True
        while full:
            line=matrix[line_max-1,:]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                line_max-=1
            else:
                full=False

        col_min=0
        full=True
        while full:
            line=matrix[:,col_min]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                col_min+=1
            else:
                full=False

        col_max=N
        full=True
        while full:
            line=matrix[:,col_max-1]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                col_max-=1
            else:
                full=False

        # For each corner : if it is occupied, check if it induce other stable disc

        mini_matrix=matrix[line_min:line_max,col_min:col_max]
        mini_stable_matrix=np.zeros_like(mini_matrix)
        
        if mini_matrix[0,0]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[0,0]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[a,b]==color:
                    mini_stable_matrix[a,b]=1
                    a+=1
                limit=a
                b+=1


        if mini_matrix[-1,0]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[-1,0]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[-a-1,b]==color:
                    mini_stable_matrix[-a-1,b]=1
                    a+=1
                limit=a
                b+=1

        if mini_matrix[0,-1]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[0,-1]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[a,-b-1]==color:
                    mini_stable_matrix[a,-b-1]=1
                    a+=1
                limit=a
                b+=1

        if mini_matrix[-1,-1]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[-1,-1]

            while limit!=0:
                a=0

                while a<limit and mini_matrix[-a-1,-b-1]==color:
                    mini_stable_matrix[-a-1,-b-1]=1
                    a+=1
                
                limit=a
                b+=1

        stable_matrix=np.zeros_like(matrix)+1    # 1 for stable, 0 for instable 
        stable_matrix[line_min:line_max,col_min:col_max]=mini_stable_matrix

        corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])

        return np.sum(stable_matrix*matrix)-corners

