#Import Dependencies
import numpy as np
from rnn_utils import *

#RNN Cell
def rnn_cell_forward(xt, a_prev, parameters):
  Wax = parameters["Wax"]
  Waa = parameters["Waa"]
  Wya = parameters["Wya"]
  ba = parameters["ba"]
  by = parameters["by"]
  
  a_next = np.tanh(np.dot(Wax, xt) + np.dot(Waa, a_prev) + ba)
  yt_pred = softmax(np.dot(Wya, a_next) + by)
  
  cache = (a_next, a_prev, xt, parameters)
  
  return a_next, yt_pred, cache

xt = np.random.randn(3,10)
a_prev = np.random.randn(5,10)
Waa = np.random.randn(5,5)
Wax = np.random.randn(5,3)
Wya = np.random.randn(2,5)
ba = np.random.randn(5,1)
by = np.random.randn(2,1)
parameters = {"Waa": Waa, "Wax": Wax, "Wya": Wya, "ba": ba, "by": by}
a_next, yt_pred, cache = rnn_cell_forward(xt, a_prev, parameters)
print("a_next.shape = ", a_next.shape)
print("yt_pred.shape = ", yt_pred.shape)

#RNN Forward Porpagation
def rnn_forward(x, a0, parameters):
  caches = []
  n_x, m, T_x = x.shape
  n_y, n_a = parameters["Wya"].shape
  a = np.zeros((n_a, m, T_x))
  y_pred = np.zeros((n_y, m, T_x))
  a_next = a0
  
  for t in range(T_x):
    a_next, yt_pred, cache = rnn_cell_forward(x[:,:,t], a_next, parameters)
    a[:,:,t] = a_next
    y_pred[:,:,t] = yt_pred
    caches.append(cache)
  
  caches = (caches, x)
  
  return a, y_pred, caches

x = np.random.randn(3,10,4)
a0 = np.random.randn(5,10)
Waa = np.random.randn(5,5)
Wax = np.random.randn(5,3)
Wya = np.random.randn(2,5)
ba = np.random.randn(5,1)
by = np.random.randn(2,1)
parameters = {"Waa": Waa, "Wax": Wax, "Wya": Wya, "ba": ba, "by": by}
a, y_pred, caches = rnn_forward(x, a0, parameters)
print("a.shape = ", a.shape)
print("y_pred.shape = ", y_pred.shape)
print("len(caches) = ", len(caches))

#LSTM Cell Forward Propagation
def lstm_cell_forward(xt, a_prev, c_prev, parameters):
  Wf = parameters["Wf"]
  bf = parameters["bf"]
  Wi = parameters["Wi"]
  bi = parameters["bi"]
  Wc = parameters["Wc"]
  bc = parameters["bc"]
  Wo = parameters["Wo"]
  bo = parameters["bo"]
  Wy = parameters["Wy"]
  by = parameters["by"]
  
  n_x, m = xt.shape
  n_y, n_a = Wy.shape
    
  concat = np.zeros((n_a + n_x, m))
  concat[: n_a, :] = a_prev
  concat[n_a :, :] = xt
    
  ft = sigmoid(np.dot(Wf, concat) + bf)
  it = sigmoid(np.dot(Wi, concat) + bi)
  cct = np.tanh(np.dot(Wc, concat) + bc)
  c_next = ft * c_prev + it * cct
  ot = sigmoid(np.dot(Wo, concat) + bo)
  a_next = ot * np.tanh(c_next)
 
  yt_pred = softmax(np.dot(Wy, a_next) + by)
  
  cache = (a_next, c_next, a_prev, c_prev, ft, it, cct, ot, xt, parameters)
  
  return a_next, c_next, yt_pred, cache
  
xt = np.random.randn(3,10)
a_prev = np.random.randn(5,10)
c_prev = np.random.randn(5,10)
Wf = np.random.randn(5, 5+3)
bf = np.random.randn(5,1)
Wi = np.random.randn(5, 5+3)
bi = np.random.randn(5,1)
Wo = np.random.randn(5, 5+3)
bo = np.random.randn(5,1)
Wc = np.random.randn(5, 5+3)
bc = np.random.randn(5,1)
Wy = np.random.randn(2,5)
by = np.random.randn(2,1)
parameters = {"Wf": Wf, "Wi": Wi, "Wo": Wo, "Wc": Wc, "Wy": Wy, "bf": bf, "bi": bi, "bo": bo, "bc": bc, "by": by}
a_next, c_next, yt, cache = lstm_cell_forward(xt, a_prev, c_prev, parameters)
print("a_next.shape = ", a_next.shape)
print("c_next.shape = ", c_next.shape)
print("yt.shape = ", yt.shape)
print("len(cache) = ", len(cache))

#LSTM RNN Forward Propagation
def lstm_forward(x, a0, parameters):
  caches = []
  n_x, m, T_x = x.shape
  n_y, n_a = parameters["Wy"].shape
  a = np.zeros((n_a, m, T_x))
  c = np.zeros((n_a, m, T_x))
  y = np.zeros((n_y, m, T_x))
  a_next = a0
  c_next = np.zeros(a_next.shape)
  
  for t in range(T_x):
    a_next, c_next, yt, cache = lstm_cell_forward(x[:, :, t], a_next, c_next, parameters)
    a[:,:,t] = a_next
    y[:,:,t] = yt
    c[:,:,t]  = c_next
    caches.append(cache)
    
  caches = (caches, x)
  
  return a, y, c, caches

x = np.random.randn(3,10,7)
a0 = np.random.randn(5,10)
Wf = np.random.randn(5, 5+3)
bf = np.random.randn(5,1)
Wi = np.random.randn(5, 5+3)
bi = np.random.randn(5,1)
Wo = np.random.randn(5, 5+3)
bo = np.random.randn(5,1)
Wc = np.random.randn(5, 5+3)
bc = np.random.randn(5,1)
Wy = np.random.randn(2,5)
by = np.random.randn(2,1)
parameters = {"Wf": Wf, "Wi": Wi, "Wo": Wo, "Wc": Wc, "Wy": Wy, "bf": bf, "bi": bi, "bo": bo, "bc": bc, "by": by}
a, y, c, caches = lstm_forward(x, a0, parameters)
print("a.shape = ", a.shape)
print("y.shape = ", y.shape)
print("len(caches) = ", len(caches))
