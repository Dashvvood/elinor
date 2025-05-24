### PHOENIX-2014-T

**Install**

- [官网下载](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/): 官网网速慢（~1MiB/s）, 文件不完整， 写的是tar.gz其实是tar. 能解压出手语图片， 但是无annotation部分

  >sha256sum: N/A

- [PaddlePaddle下载](https://aistudio.baidu.com/datasetdetail/158937): 这个速度这个链接到Apr 3 2025还没发现什么问题

  >sha256sum(locally computed): e47fec2d460ed2ea5d19198df46a231781f2abc7a8aa14132184af4a8166f90d

**数据集结构(PaddlePaddle)**

```shell
PHOENIX-2014-T-release-v3/
└── PHOENIX-2014-T
    ├── annotations
    │   └── manual
    ├── evaluation
    │   ├── sign-recognition
    │   └── sign-translation
    ├── features
    │   └── fullFrame-210x260px
    │       ├── dev
    │       ├── test
    │       └── train
    └── models
        └── languagemodels
```

**补充说明**

- 图像都是png格式， 每个片段放到一个文件夹中， 按照帧时间顺序编号

---