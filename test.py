#coding=utf-8
#!/usr/bin/env python



from xsegment.ZooSegment import FMM



if __name__ == '__main__':
	segment = FMM()

	for word in segment.segment('我爱中国'):
		print word