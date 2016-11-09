# coding:utf-8
# author： ou
#-coding:UTF8-*-
import os,os.path
import zipfile
class AndroidTest(object):
    def __init__(self):
        self.urlhome="http://m.sfacg.com"
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}
        # zip_dir(r'E:/python/learning',r'E:/python/learning/zip.zip')
        # unzip_file(r'E:/python/learning/zip.zip',r'E:/python/learning2')
    #压缩
    def zip_dir(dirname,zipfilename):
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else :
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar,arcname)
        zf.close()

    #解压
    def unzip_file(zipfilename, unziptodir):
        if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0o777)
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\','/')

            if name.endswith('/'):
                os.mkdir(os.path.join(unziptodir, name))
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0o777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()