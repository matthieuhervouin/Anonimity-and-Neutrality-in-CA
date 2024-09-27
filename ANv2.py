import numpy as np 
import itertools


#We set P={0,1, ... rho-1} without considering it to be a field
#Same for N and X
rho=3
n=5
m=4


def Cswap(C,l): #a permutation of P on a profile C, l is the list of size rho representing the permutation on P
	A=np.copy(C)
	for i in range(n):
		for j in range(m):
			A[i][j]=l[C[i][j]]
	return A

def Cswap2(a,l): #permutation of P on classif a
	return np.array([l[a[i]] for i in range(len(a))])


def Oswap(C,l):  #a permutation of X on a profile C, l is the list of size m representing the permutation (object x_{l[i]} is sent to x_i)
	A=np.copy(C)
	for i in range(n):
		for j in range(m):
			A[i][j]=C[i][l[j]]
	return A

def Oswap2(a,l): #permutation of X on classif a
	b=np.copy(a)
	for i in range(m):
		b[i]=a[l[i]]
	return b 

def Aswap(C,l):
	A=np.copy(C)
	for i in range(n):
		A[i]=C[l[i]]
	return A


def Aswaps(C,dico): 
	L=list(itertools.permutations([i for i in range(n)]))
	for li in L:
		A=Aswap(C,li)
		if (str(A) in dico) and np.all(dico[str(A)]!=dico[str(C)]):
			print("impossible")
			print(str(C),dico[str(C)])
			print(str(A), dico[str(A)])
			return False
		elif str(A) not in dico:
			dico[str(A)]=dico[str(C)]
	return True


def Oswaps(C,dico): 
	L=list(itertools.permutations([i for i in range(m)]))
	for li in L:
		A=Oswap(C,li)
		l=Oswap2(dico[str(C)],li)
		if (str(A) in dico) and np.all((dico[str(A)]!=l)):
			print("impossible")
			print(str(C),dico[str(C)])
			print(str(A), dico[str(A)])
			return False
		elif str(A) not in dico:
			dico[str(A)]=l
	return True

def Cswaps(C,dico): 
	L=list(itertools.permutations([i for i in range(rho)]))
	for li in L:
		A=Cswap(C,li)
		l=Cswap2(dico[str(C)],li)
		if (str(A) in dico) and np.all((dico[str(A)]!=l)):
			print("impossible")
			print(str(C),dico[str(C)])
			print(str(A), dico[str(A)])
			return False
		elif str(A) not in dico:
			dico[str(A)]=l
	return True

def surjective(c):
	for i in range(rho):
		if i not in c:
			return False
	return True

def list_classif(m,rho):
	l=list(itertools.combinations_with_replacement([i for i in range(rho)],m))
	l_classif=[]
	for c in l:
		if surjective(c):
			for c2 in list(itertools.permutations(c)):
				if c2 not in l_classif:
					l_classif.append(list(c2))
	return l_classif

L_classif=list_classif(m,rho)
print("List of classifications (surjective mappings): ",L_classif)
n_profiles=len(L_classif)**n
print("number of profiles: ",n_profiles)

def list_profiles(m,n,rho):
	l_classif=list_classif(m,rho)
	l_profile=[]
	return list(itertools.combinations_with_replacement(l_classif,n))


L_profile=list_profiles(m,n,rho)


def propagation(C,dico):
	i=0
	b=False
	l1=list(itertools.permutations([i for i in range(rho)]))
	l2=list(itertools.permutations([i for i in range(n)]))
	l3=list(itertools.permutations([i for i in range(m)]))
	count=0
	while i<len(L_classif) and (not b):
		ndic={}
		ndic[str(C)]=np.array(L_classif[i])
		b=True
		for a in l2:
			for pi in l3:
				for si in l1:
					c2=Cswap2(L_classif[i],si)
					C2=Cswap(C,si)
					C2=Aswap(C2,a)
					C2=Oswap(C2,pi)
					c2=Oswap2(c2,pi)
					if (str(C2) in ndic) and (np.any(ndic[str(C2)]!=c2)):
						b=False
						break
					elif str(C2) not in ndic:
						ndic[str(C2)]=c2
						count+=1
				if not b:
					break
			if not b:
				break
		i+=1
	if b:
		dico.update(ndic)
		return True
	else:
		return False

def test(m,n,rho):
	global dico
	dico={}
	b=True
	while len(dico)<n_profiles and b:
		i=0
		while (str(np.array(L_profile[i])) in dico):
			i+=1
		global C
		C=np.array(L_profile[i])
		b=propagation(C,dico)
		print(100*len(dico)/n_profiles,'%')
	return b

file_name=str((m,n,rho))
with open(file_name, 'w') as f:
	b=test(m,n,rho)
	print(b)
	if b:
		f.write(str(C)+str(dico[str(C)]))
	else:
		f.write(str(C))

	





