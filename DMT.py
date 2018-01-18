#coding=utf-8
from math import log
import operator
#计算香浓熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet) #求数据集的长度
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]#提取标签
        if currentLabel not in labelCounts.keys():labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries #计算每种结果出现的可能性
        shannonEnt -= prob * log(prob,2) #计算出的熵的结果，再进行累加
    return shannonEnt

#按照给定特征划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[ : axis]
            reduceFeatVec.extend(featVec[axis+1 : ]) #函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
            #上面两步实际上是选择了这个属性的某个值筛选出来然后去除了axis这一列
            retDataSet.append(reduceFeatVec)
    return retDataSet

#选择最好的数据集划分方式
'''
数据要求
（1）数据必须是一种有列表元素组成的列表，而且所有的列表元素都要具有相同的数据长度
（2）数据的最后一列或者每个实例的最后一个元素是当前实例的类别标签
'''
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1 #判断数据集有多少特征属性
    baseEntropy = calcShannonEnt(dataSet) #计算原始的香浓熵 用于划分数据集后比较
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):#用于遍历数据集中所有的属性
        #下面使用列表推导式创建新的列表
        featList = [example[i] for example in dataSet]#将每一个属性的值都提取出来 第i个特征所有可能的值
        uniqueList = set(featList)#去重 搞清楚属性的值
        newEntropy = 0.0
        for value in uniqueList:#使用该属性划分数据集 最后一个属性就是标签 就是原始香浓熵 相减为零
            subDataSet = splitDataSet(dataSet,i,value)#用该属性的一个值划分数据集
            prob = len(subDataSet) / float(len(dataSet))#发生的概率
            newEntropy += prob * calcShannonEnt(subDataSet)#发生的概率乘以数据集的香浓熵 全概率公式
        infoGain = baseEntropy - newEntropy#计算信息增益 该信息增益就是去掉的属性的香浓熵
        if (infoGain > bestInfoGain):#香浓熵的值越大说明包含的信息越多 应该选择其为最好的特征
            bestInfoGain =infoGain
            bestFeature = i
    return bestFeature

#基本工作已经做好了 现在需要递归迭代构造decision-making tree
#选取最好的划分特征 划分数据集（不一定是两个，可能有很多个）再使用划分算法划分数据集
#递归结束的条件是：程序遍历完所有划分数据集的属性，或者每个分支下的所有实例都具有相同的分类
#到最后一个节点还存在多种分类的话使用多数表决方法决定到该节点的样例的类别
def majorityCnt(classlist):
    classCount = {}#设置一个字典 键为存在的类别 值为键出现的次数
    for vote in classlist:
        if (vote not in classCount.key):classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse = True)#从大到小排序
    return sortedClassCount[0][0] #[[key,value]...]返回的是其键的值 就是出现次数最多的类别

#创建树的代码
def creatTree(dataSet,labels):
    classList = [example[-1] for example in dataSet] #取出标签
    if (classList.count(classList[0]) == len(classList)):return classList[0] #类别完全相同就不用再划分了 返回所属的种类
    if (len(dataSet[0]) == 1):return majorityCnt(classList) #只剩分类，当使用完所有的属性还不能得到完全的结论时使用多数表决的算法
    bestFeat = chooseBestFeatureToSplit(dataSet) #如果既没有出现相同的划分 又没有出现所有属性用完的情况 说明递归还未结束 第一步找出最好的划分的依据
    bestFeatLabel = labels[bestFeat]
    mytree = {bestFeatLabel:{}}
    del(labels[bestFeat])#del删除的是变量而不是数据对象 删除列表中的那个元素
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        mytree[bestFeatLabel][value] = creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return mytree


def creatDataSet():
    dataset = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing','flippers']
    return dataset,labels





