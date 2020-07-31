import sys
import bisect
import math
def read_file(filename):
	fileHandler=open(filename,"r")  #open file
	commands=[]
	for line in fileHandler:
		commands.append(line.strip().split())
	fileHandler.close()
	return commands
		# As each line (except last one) will contain new line character, so strip that
		#split() method returns a list of strings after breaking the given string by the 
		#specified separator.
class Node:
	def __init__(self):
		self.keys=[]
		self.children=[]    
		self.is_leaf=True
		self.next=None#if it is a leaf node then this indicates the pointer to the right
	def splitNode(self):
		newNode=Node()
		if self.is_leaf is True:
			newNode.is_leaf=True
			mid=math.ceil(len(self.keys)/2)
			#mid=int(len(self.keys)/2)
			#split such that newNode will have floor(n+1/2) key-pointer pairs
			midkey=self.keys[mid]
			newNode.keys=self.keys[mid:]
			newNode.children=self.children[mid:]
			self.keys=self.keys[:mid]
			#adjust the pointers of the newNode and the oldNode
			self.children=self.children[:mid]
			newNode.next=self.next
			self.next=newNode
		else:
			newNode.is_leaf = False

			mid = int(len(self.keys)/2)#this gives the floor value
			midkey = self.keys[mid]

			newNode.keys = self.keys[mid+1:]
			newNode.children = self.children[mid+1:]

			self.keys = self.keys[:mid]
			self.children = self.children[:mid + 1]
		return midkey,newNode

class Bplustree:
	def __init__(self,order):
		self.order=order
		self.root=Node()
	def insert(self,key,node):
		if node.is_leaf is True:
			index=bisect.bisect(node.keys,key)
			node.keys.insert(index,key)
			node.children.insert(index,key)
			if len(node.keys)>self.order and node==self.root:
				newRoot=Node()
				newRoot_value,newNode=node.splitNode()
				newRoot.is_leaf = False
				newRoot.keys = [newRoot_value]
				newRoot.children = [self.root, newNode]
				self.root = newRoot
				return newRoot_value,newNode#This statement is not needed
				#node and self.root are same so changes in node in splitnode() function are 
				#reflected in self.root also.
			elif len(node.keys)>self.order and node!=self.root:
				newChild,newNode=node.splitNode()#newChild indicates the returned midkey value
				return newChild,newNode
			else:
				return None,None				
		else:
			if key<node.keys[0]:
				newChild,newNode=self.insert(key,node.children[0])

			for i in range(len(node.keys)-1):
				if key >= node.keys[i] and key < node.keys[i + 1]:
					newChild,newNode=self.insert(key, node.children[i+1])

			if key >= node.keys[-1]:
				newChild,newNode=self.insert(key, node.children[-1])

			if newChild:
				index = bisect.bisect(node.keys, newChild)
				node.keys.insert(index,newChild)
				node.children.insert(index+1,newNode)
				if len(node.keys) <= self.order:
					return None,None
				elif len(node.keys)>self.order and node!=self.root:
					midKey, newNode = node.splitNode()
					return midKey, newNode
				elif len(node.keys)>self.order and node==self.root:
					newRoot=Node()
					newRoot_value,newNode=node.splitNode()
					newRoot.is_leaf = False
					newRoot.keys = [newRoot_value]
					newRoot.children = [self.root, newNode]
					self.root = newRoot
					return newRoot_value,newNode#This is not needed
			else:
				return None, None
	def find(self,key,node):
		if node.is_leaf is True:
			if key in node.keys:
				return 1
			else:
				return 0
		else:
			ans=0
			ans1=0
			ans2=0
			ans3=0
			ans4=0
			ans6=0
			if key<node.keys[0]:
				ans=self.find(key,node.children[0])

			for i in range(len(node.keys)-1):
				if key>=node.keys[i]:
					ans1=self.find(key,node.children[i])
					ans2=self.find(key, node.children[i+1])
					ans6=ans6+ans1+ans2
			if key >= node.keys[-1]:
				ans3=self.find(key,node.children[-2])
				ans4=self.find(key, node.children[-1])
			final_ans=ans+ans6+ans3+ans4
			return final_ans
	def count1(self,key,node):
		if node.is_leaf is True:
			flag1=0
			count2=0
			while node!=None:
				for k in range(len(node.keys)):
					if node.keys[k]==key:
						count2=count2+1
					elif node.keys[k]>key:
						flag1=1
						break
				if flag1==1:
					break
				node=node.next
			return count2
		else:
			ans=0
			ans1=0
			ans3=0
			if key<node.keys[0]:
				ans=self.count1(key,node.children[0])
				final_ans=ans
				return final_ans
			for i in range(len(node.keys)-1):
				if key>=node.keys[i]:
					ans1=self.count1(key,node.children[i])
					final_ans=ans1
					return final_ans
			if key >= node.keys[-1]:
			 	ans3=self.count1(key,node.children[-2])
			 	final_ans=ans3
			 	return final_ans
	def range1(self,key1,key2,node):
		if node.is_leaf is True:
			flag1=0
			count2=0
			while node!=None:
				for k in range(len(node.keys)):
					if node.keys[k]>=key1 and node.keys[k]<=key2:
						count2=count2+1
					elif node.keys[k]>key2:
						flag1=1
						break
				if flag1==1:
					break
				node=node.next
			return count2
		else:
			ans=0
			ans1=0
			ans3=0
			if key1<node.keys[0]:
				ans=self.range1(key1,key2,node.children[0])
				final_ans=ans
				return final_ans
			for i in range(len(node.keys)-1):
				if key1>=node.keys[i]:
					ans1=self.range1(key1,key2,node.children[i])
					final_ans=ans1
					return final_ans
			if key1 >= node.keys[-1]:
			 	ans3=self.range1(key1,key2,node.children[-2])
			 	final_ans=ans3
			 	return final_ans
#I didn't put the function names as count and range because range is keyword and count is a
#function in python
tree=Bplustree(3)
#The above statement creates a root node with keys,children,is_leaf and next attributes.
filename=sys.argv[1]
commands=read_file(filename)
f1=open("file_output.txt","w")
for command in commands:
	if command[0]=="INSERT":
		tree.insert(int(command[1]),tree.root)
	elif command[0]=="FIND":
		final_ans=tree.find(int(command[1]),tree.root)
		if final_ans>=1:
			#print("YES")
			f1.write("YES\n")
		else:
			#print("NO")
			f1.write("NO\n")
	elif command[0]=="COUNT":
		final_ans=tree.count1(int(command[1]),tree.root)
		f1.write(str(final_ans))
		f1.write("\n")
		#print(final_ans)
	elif command[0]=="RANGE":
		final_ans=tree.range1(int(command[1]),int(command[2]),tree.root)
		f1.write(str(final_ans))
		f1.write("\n")
f1.close()
		#print(final_ans)
# list1=[tree.root]
# node=list1[0]
# while node.is_leaf!=True:
# 	for k in range(len(node.keys)):
# 		print("print")
# 		print(node.keys[k])
# 	print("\n")
# 	list1.pop(0)
# 	for s in range(len(node.children)):
# 		print("I am child")
# 		list1.append(node.children[s])
# 	print("Length----")
# 	print(len(list1))
# 	print("-------")
# 	node=list1[0]
# for i in range(len(list1)):
# 	for k in range(len(list1[i].keys)):
# 		print(list1[i].keys[k])
# 	print("\n")