应用场景:
	1. 样本汇总(root):
		- 文件类型/平台
		- 恶意家族
		-
	2. 单独样本内容展示:
		- 基本信息
		- 扩展信息
		- 不同类型的样本显示方式自然是不同的:
			- PE/ELF
			- OLE/Office/...
			- VB
	3. 搜索类似:
		- 手动收入字符串搜索类似
		- 点击样本的xx项搜索类似
		-
需求:
	x. 抽取一些脚本接口, 使用户可以访问数据库中的资源, 用户可以上传/编辑自己的脚本, 并将脚本作为任务来执行
		- 当然, 任务可以操作
		-
	x. 用户可以在本地部署, 并与服务器的内容同步
		- 毕竟服务器上的计算资源是有限的, 数据资源是受保护的, 在本地可以更自由/大胆些
		-
	x. idb 文件可以多人查看/合作编辑
		- 服务器上可以保存多个用户的编辑内容
		- 用户 IDA 端插件, 可以查看所有用户的编辑内容, 并进行选择性同步
		- 用户可以选择性的将某些内容通过插件同步到服务器
		-
	x. twitter也有样本来源
		-
	1. 处理脚本更新后, 用新样本批量处理所有脚本, 用新内容覆盖原本的数据库内容
		- 是否要区分哪些字段是手动输入的, 哪些字段是脚本生成的, 然后新脚本在覆盖时, 可以有选择的覆盖??
			- 否!
		-
	2. 能够自动从 vt/malwr/hybrid-analysis/reverse-it/xxx 等多个网站获取恶意代码的分析结果
		- 用网站的 api, 不是解析 html, 因为 html 会变
		- 多个网站结果交叉对比，与用户输入进行对比等
		- IDA有现有插件, Github有Python脚本
		-
	3. 能够自动从 vt/malwr/hybrid-analysis/reverse-it/xxx 等多个网站下载样本
		- 用我们自己的自动化分析脚本进行分析, 以及分析结果对比, 从中筛选有价值的样本
		- IDA有现有插件, Github有Python脚本
		-
	4. 用户只能对自己的样本进行修改
		-
	5. 与cuckoo(windows/android)对接
		-
	6. repo:
		- https://github.com/MISP/MISP
			- 恶意代码信息/威胁信息分享平台
			- 维护中
			- keyword: MISP - Malware Information Sharing Platform
			- http://www.misp-project.org/features.html
			- https://github.com/MISP/misp-modules
			- https://github.com/MISP/PyMISP
			- https://github.com/MISP/misp-book
		- https://github.com/yeti-platform/yeti
			- Your everyday threat intelligence
		- [Thread Hunting]  (CyberEverything)
			- https://github.com/Cyb3rWard0g/ThreatHunter-Playbook
			- https://github.com/ThreatHuntingProject/ThreatHunting
	7. 能够从 pcap 文件中选择 packet, 作为显示界面的内容
		-
	8. 字符串相似性比较:
		- https://stackoverflow.com/questions/6690739/fuzzy-string-comparison-in-python-confused-with-which-library-to-use
		- https://github.com/seatgeek/fuzzywuzzy
			- 介绍: http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
			- 需求:
				- difflib:
					- 标准库
					- https://docs.python.org/2/library/difflib.html
					- 本身不止比较字符串
				- python-Levenshtein:
					- 包
					- https://github.com/ztane/python-Levenshtein/
					- https://pypi.python.org/pypi/python-Levenshtein/0.12.0
	9. 数据库
		- [No]pymongo
			- http://api.mongodb.com/python/current/api/pymongo/collection.html
		- [OK]mongoengine
			- https://github.com/MongoEngine/mongoengine
		- [NO]mongokit
			- https://github.com/namlook/mongokit
			- 好久不更新了
	10. 提交特定的txt文档, 服务器解析, 根据内容挨个儿调用相应的接口
		-
	11. 文件类型
		- magic - https://github.com/KoreLogicSecurity/mastiff/blob/master/mastiff/filetype.py
		- yara - 没干这个的rule
		- trid -
	12. 壳/编译器信息
		- pefile.py 自带功能，需要 peid 的 signature, 但是都比较老了
			- 1个结果: 扫描ep
			- N个结果: 扫描所有二进制
		- yara 有 peid 的 signature, 方便添加新的. 默认是扫描所有二进制, 所以会有多个结果
		- pestudio 的 signatures.xml
	13. 字符串提取
		- strings
			- 算了...
		- idb-string
			- https://github.com/williballenthin/python-idb
			- https://github.com/nlitsme/pyidbutil  # Python
			- https://github.com/nlitsme/idbutil    # C
		- floss
			- https://github.com/fireeye/flare-floss
		- yarGen
			- https://github.com/Neo23x0/yarGen
			- good-strings.db
			- good-opcodes.db
		- pestudio 的 strings.xml
	14. ida signature
		- 自己创建
		- 现有的
			- https://github.com/push0ebp/sig-database
				- VC12
				- openssl(0.9.8/1.0.2)
			- https://github.com/Maktm/FLIRTDB
				- boost/cmt/cpmt/intel/openssl/vcruntime
				- 每一个版本都非常多
			- https://github.com/LetsUnlockiPhone/iPhone-Baseband-IDA-Pro-Signature-Files
				- RVCT_RTL
	15. 函数的相似性比较
		- https://reverseengineering.stackexchange.com/questions/1879/how-can-i-diff-two-x86-binaries-at-assembly-code-level
		- BinDiff
			- https://github.com/icewall/BinDiffFilter
		- FIRST
			- https://github.com/vrtadmin/FIRST
			- https://first-plugin-ida.readthedocs.io/en/latest/
			- 需求 IDA 6.9 SP1??
			- Python + web, 10月前更新, 54星
		- BinSim
			- https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/ming
				- BinSim: Trace-based Semantic Binary Diffing via System Call Sliced Segment Equivalence Checking
			- http://www.binsim.com/
				- http://www.binsim.com/pdf/esh-paper.pdf
					- Statistical Similarity of Binaries
			- 无源码
		- diaphora
			- https://github.com/joxeankoret/diaphora
			- Python, 更新中, 不频繁, 668星
			- http://diaphora.re/
			- https://github.com/radare/diaphora # fork版, 无星
		- DarunGrim
			- https://github.com/ohjeongwook/DarunGrim
			- C语言, 3年前了
			- http://darungrim.org/
		- turbodiff
			- https://github.com/nihilus/turbodiff
			- C++, 3年前了
		- radare -d -g
			- http://rada.re/r/
		- patchdiff2
			- https://github.com/filcab/patchdiff2
			- C++, 4年前了
		- kdiff
			- https://sourceforge.net/projects/kdiff3/files/
			- http://kdiff3.sourceforge.net/
			- 3年前了
		- Relyze
			- https://www.relyze.com/overview.html
			- 要钱的
		- eEye Binary Diffing Suite
			- https://www.blackhat.com/presentations/bh-usa-09/OH/BHUSA09-Oh-DiffingBinaries-PAPER.pdf
			- 太老了
		- IDACompare
			- https://github.com/dzzie/IDACompare
			- VB, 更新中
		- ?? IDAEye
			- http://www.mfmokbel.com/Down/RCE/IDAEye.zip
			- https://tuts4you.com/download.php?view.3625
		- BinClone
			- https://github.com/BinSigma/BinClone
			- C++, 3年前
			- 检测克隆代码

	x.wget:
		- https://github.com/jakubroztocil/httpie



1. 是否有必要用mongo实现一套界面?
	* 对于界面的把控
	* 练习django
	* 某些想法不一定能审过

2. PE文件的基本信息:
	* pefile.py
	* 参照下
		- viper - pe.py
		- AnalyzePE - pescanner.py

3. misc:
	* stateless
	* pestudio xml 目录下得各种 xx.xml
	* inlined-library(ssl)
	* 签名解析
		-