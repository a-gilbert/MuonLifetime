import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


#get data
f = open("muon.data")

t_all = []
d_all = []
d_valid = []
t_valid = []


for l in f.readlines():
    l = l.split()
    d_all.append(int(l[0].strip()))
    t_all.append(int(l[1].strip()))
    if d_all[-1] < 40000:
        d_valid.append(d_all[-1])
    
f.close()

t_all = np.array(t_all)
d_all = np.array(d_all)
d_valid = np.array(d_valid)
d_valid = d_valid * 1e-3


#Plot and get stats.
nb1 = 200
nb2= 2000

n1, dvals1 = np.histogram(d_valid, bins=nb1)
n2, dvals2 = np.histogram(d_valid, bins=nb2)
plt.close('all')
plt.figure()
#plt.semilogy(dvals[0:-1], n, 'o', markerfacecolor='None')
plt.semilogy(dvals1[0:-1], n1, 'o', label="b=200", markersize=1)
plt.semilogy(dvals2[0:-1], n2, 'o', label="b=2000", markersize=1)
plt.xlabel(r"t ($\mu s$)")
plt.ylabel("N")
plt.legend()
plt.savefig('bboth.eps')

l1 = int((2.0/200)*nb1)
m1 = int((98.0/200)*nb1)

l2 = int((1.0/200)*nb2)
m2 = int((98.0/200)*nb2)

cdvals1 = dvals1[l1:m1]
cnvals1 = n1[l1:m1]
norm_vals1 = cnvals1 / np.sum(cnvals1)

cdvals2 = dvals2[l2:m2]
cnvals2 = n2[l2:m2]
norm_vals2 = cnvals2 / np.sum(cnvals2)

plt.close('all')
plt.figure()
plt.semilogy(cdvals1, norm_vals1, 'o', label="b=200", markersize=1)
plt.semilogy(cdvals2, norm_vals2, 'o', label="b=2000", markersize=1)
plt.xlabel(r"t ($\mu s$)")
plt.ylabel("N")
plt.legend()
plt.savefig('ensembleBoth.eps')

s1, i, r, p, e = stats.linregress(cdvals1[norm_vals1!=0], np.log(norm_vals1[norm_vals1!=0]))
s2, i, r, p, e = stats.linregress(cdvals2[norm_vals2!=0], np.log(norm_vals2[norm_vals2!=0]))

tau1 = -1/s1
tau2 = -1/s2
tau_ans = 2.1969811

err1 = 100*abs(tau_ans- tau1)/tau_ans
err2 = 100*abs(tau_ans - tau2)/tau_ans
print("Mean tau for nb=200 is tau=%f micro seconds.\n" % tau1)
print("Error for nb=200: %f\n" % err1)
print("Mean tau for nb=2000 is tau=%f micro seconds.\n" % tau2)
print("Error for nb=2000: %f\n" % err2)

dt = t_all[-1] - t_all[0]
dt = dt*(1/60)*(1/60)*(1/24.0)
print("Data collection for this trial took %f days.\n" % dt)
quit()
