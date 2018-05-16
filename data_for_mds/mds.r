#!/usr/bin/enb Rscript
#data<-read.table("assasination.dat")
data<-read.table("random_wiki.dat")
labels<-read.table("keywords")
dist<-dist(data, method="canberra")
fit<-cmdscale(dist, eig=TRUE, k=2)
x<-fit$points[,1]
y<-fit$points[,2]
plot(x,y, type="n")
text(x,y, labels=labels[,1])
