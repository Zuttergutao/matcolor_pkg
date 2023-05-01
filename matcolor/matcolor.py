import matplotlib.pyplot as plt
import yaml
from matplotlib.colors import ListedColormap
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from PIL import Image

class extract_feature_colors:
    """
    提取图片的特征颜色，包括构建颜色映射和绘制颜色映射。
    """
    def __init__(self,img_path,num_colors=25):
        """
        初始化函数。

        参数：
        - img_path: str 图片路径
        - num_colors: int 需要提取的特征颜色数量，默认值为 25
        """
        self.imgpath=img_path
        self.numcolors=num_colors
    
    def RGB_to_Hex(self,rgb):
        """
        将 RGB 格式的颜色转换为十六进制格式。

        参数：
        - rgb: tuple 包含三个整数的 RGB 颜色元组

        返回值：
        - color: str 十六进制格式的颜色代码
        """
        color = '#'
        for i in rgb:
            num = int(i)
            color += str(hex(num))[-2:].replace('x', '0').upper()
        return color
    
    def draw_cm(self,savefig=True,cmname="colormap.png"):
        """
        绘制颜色映射，并将结果保存到 colormap.png 文件中。

        参数：
        - savefig: bool 是否保存图像，True 表示保存，False 表示不保存，默认值为 True
        - cmname: str 保存的图像名称，仅在 savefig 为 True 时生效，默认值为 "colormap.png"
        """
        fig,axes=plt.subplots(figsize=(1*self.numcolors,2))
        axes.imshow([np.arange(len(self.colormap()))],cmap=ListedColormap(self.colormap()),aspect="auto")
        axes.set_xticks(np.arange(len(self.colormap())),self.colormap())
        axes.set_yticks([])
        axes.grid(False)
        axes.spines["top"].set_visible(False)
        axes.spines["bottom"].set_visible(False)
        axes.spines["left"].set_visible(False)
        axes.spines["right"].set_visible(False)
        axes.tick_params(axis='both',which='both',length=0)
        if savefig== True:
            fig.savefig(cmname,dpi=600)

    def rgb_sort(self,x):
        """
        对颜色排序，将十六进制数转换为整数进行排序。

        参数：
        - x: str 十六进制格式的颜色代码

        返回值：
        - int(x[1:], 16): int 十六进制数转换后的整数
        """
        return int(x[1:], 16)

    def colormap(self):
        """
        构建颜色映射。

        返回值：
        - colormap: list 包含 num_colors 种颜色代码的字符串列表，按顺序排列（从深到浅）
        """
        image = Image.open(self.imgpath)
        small_image = image
        result = small_image.convert('P', palette=Image.Palette.ADAPTIVE, colors=self.numcolors)   # image with 5 dominating colors
        result = result.convert('RGB')
        main_colors = result.getcolors()
        colormap=[]
        for i in range(len(main_colors)):
            colormap.append(self.RGB_to_Hex(main_colors[i][1]))
            
        colormap=sorted(colormap,key=self.rgb_sort)
        colormap.reverse()
        return colormap
    

class matcolor:
    
    def __init__(self):
        self.register_schemes(yamlpath='../colorschemes/dcolor.yaml')
        self.cmn,self.cm=self.return_cm()
    
    # 单色
    def scolor(self):
        pass
    
    # 渐变色
    # 如何解决连续颜色colorbar以及对应的数值映射
    def ccolor(self,name="",useimg=False,numcolors=5,imgpath=None,N=256):
        if useimg==True:
            cm.register_cmap(name=name, cmap=ListedColormap(extract_feature_colors(imgpath,numcolors).colormap()))
            cmap=cm.get_cmap(name)
            return mcolors.LinearSegmentedColormap.from_list(name,colors=cmap(np.linspace(0,1,cmap.N)),N=N)
        else:
            cmap=cm.get_cmap(name)
            return mcolors.LinearSegmentedColormap.from_list(name, colors=cmap(np.linspace(0,1,cmap.N)),N=N)
            
    
    # 离散色
    def dcolor(self,name="",useimg=False,numcolors=5,imgpath=None):
        if useimg==True:
            return extract_feature_colors(imgpath,numcolors).colormap()
        else:
            cmap=cm.get_cmap(name)
            return cmap(np.linspace(0, 1, cmap.N))
        
    # 注册colormap   
    def register_schemes(self,yamlpath):
        with open(yamlpath) as f:
            schemes = yaml.safe_load(f)

        for scheme in schemes:
            name = scheme['name']
            colors = scheme['colors']
            if name in plt.colormaps:
                pass
            else:
                if int(mpl.__version__.split(".")[1])> 7:
                    cm.register(name=name, cmap=ListedColormap(colors))
                else:
                    cm.register_cmap(name=name, cmap=ListedColormap(colors))

    def add_colormap(self,name,img_path=[],num_colors=5,cmap=[]):
        if name in self.cmn:
           print("colormap name existed")
        else:
            name="{}".format(name)
            if img_path:
                colors=extract_feature_colors(img_path,num_colors).colormap()
                cmData = {'name': name, 'colors': colors}
            else:
                cmData={'name': name, 'colors': cmap}

            with open("../colorschemes/dcolor.yaml", 'a', encoding='utf-8') as f:
                yaml.dump(data=[cmData], stream=f, sort_keys=False,allow_unicode=True)  

            self.register_schemes(yamlpath='../colorschemes/dcolor.yaml')
        self.return_cm()

    def del_colormap(self,name):
        if name in plt.colormaps():
            if int(mpl.__version__.split(".")[1])> 7:
                cm.unregister(name=name)
            else:
                cm.unregister_cmap(name=name)
                
        if name in self.cmn:
           with open("../colorschemes/dcolor.yaml") as f:
               schemes = yaml.safe_load(f)
               for i,n in enumerate(self.cmn):
                   if name == n:
                       tmp=i
               schemes.pop(i)

           with open("../colorschemes/dcolor.yaml","w") as f:
                yaml.dump(data=schemes, stream=f, sort_keys=False,allow_unicode=True)
        else:
           print("colormap name not existed in dcolor.yaml") 

        self.return_cm() 
      
    def return_cm(self):
        cmnarr=[]
        cmlarr=[]
        with open('../colorschemes/dcolor.yaml') as f:
            schemes = yaml.safe_load(f)

        for scheme in schemes: 
            cmnarr.append(scheme['name'])
            cmlarr.append(scheme['colors'])

        return cmnarr,cmlarr
    
    def draw_cm(self,show=""):
        if show:
            try:
                return cm.get_cmap(show)
            except:
                print("colormap name not existed")
        else:
            cmlen=len(self.cmn)
            fig,axes=plt.subplots(cmlen,1,figsize=(12,2.5*cmlen))                                       
            plt.rcParams["figure.subplot.hspace"]=0.5                 
            plt.rcParams["font.family"]="Times New Roman"               
            plt.rcParams["font.style"]="normal"                         
            plt.rcParams["font.weight"]=400                             
            plt.rcParams["font.size"]=12                               
            for i in range(cmlen):
                cmap=mpl.cm.get_cmap(self.cmn[i])
                axes[i].imshow([np.arange(cmap.N)],cmap=cmap,aspect="auto")
                axes[i].set_xticks(np.arange(cmap.N),self.cm[i],font="Arial",fontsize=12,fontweight="bold")
                axes[i].set_xlabel(self.cmn[i],font="Arial",fontsize=16,fontweight="bold")
                axes[i].set_yticks([])
                axes[i].grid(False)
                axes[i].spines["top"].set_visible(False)
                axes[i].spines["bottom"].set_visible(False)
                axes[i].spines["left"].set_visible(False)
                axes[i].spines["right"].set_visible(False)
                axes[i].tick_params(axis='both',which='both',length=0)